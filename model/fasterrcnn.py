import cv2

from common.data_collector import DataCollector, DATA_TYPE_DETECTION
from database.weightsdb import get_weight
from keras import backend as K
from thirdparty.kerasfasterrcnn import config
from thirdparty.kerasfasterrcnn import resnet as nn
from keras.layers import Input
from keras.models import Model
from thirdparty.kerasfasterrcnn import roi_helpers
import numpy as np

NUM_FEATURES = 1024


def format_img_size(img, C):
    """ formats the image size based on config """
    img_min_side = float(C.im_size)
    (height, width ,_) = img.shape

    if width <= height:
        ratio = img_min_side/width
        new_height = int(ratio * height)
        new_width = int(img_min_side)
    else:
        ratio = img_min_side/height
        new_width = int(ratio * width)
        new_height = int(img_min_side)
    img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    return img, ratio


def format_img_channels(img, C):
    """ formats the image channels based on config """
    img = img[:, :, (2, 1, 0)]
    img = img.astype(np.float32)
    img[:, :, 0] -= C.img_channel_mean[0]
    img[:, :, 1] -= C.img_channel_mean[1]
    img[:, :, 2] -= C.img_channel_mean[2]
    img /= C.img_scaling_factor
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)
    return img


def format_img(img, C):
    """ formats an image for model prediction based on config """
    img, ratio = format_img_size(img, C)
    img = format_img_channels(img, C)
    return img, ratio


# Method to transform the coordinates of the bounding box to its original size
def get_real_coordinates(ratio, x1, y1, x2, y2):

    real_x1 = int(round(x1 // ratio))
    real_y1 = int(round(y1 // ratio))
    real_x2 = int(round(x2 // ratio))
    real_y2 = int(round(y2 // ratio))

    return real_x1, real_y1, real_x2 ,real_y2


def create_box_resp_field(label, score, xmax, xmin, ymax, ymin):
    resp_fields = dict()
    resp_fields['label'] = int(label)
    resp_fields['score'] = float(score)
    resp_fields['xmax'] = float(xmax)
    resp_fields['xmin'] = float(xmin)
    resp_fields['ymax'] = float(ymax)
    resp_fields['ymin'] = float(ymin)
    return resp_fields


class FasterRcnn(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.C = config.Config()
            img_input = Input(shape=(None, None, 3))
            roi_input = Input(shape=(cls.C.num_rois, 4))
            feature_map_input = Input(shape=(None, None, NUM_FEATURES))

            # define the base network (resnet here, can be VGG, Inception, etc)
            shared_layers = nn.nn_base(img_input, trainable=True)

            # define the RPN, built on the base layers
            num_anchors = len(cls.C.anchor_box_scales) * len(cls.C.anchor_box_ratios)
            rpn_layers = nn.rpn(shared_layers, num_anchors)

            cls.class_mapping = {0: 'tvmonitor', 1: 'train', 2: 'person', 3: 'boat', 4: 'horse', 5: 'cow', 6: 'bottle',
                                 7: 'dog', 8: 'aeroplane', 9: 'car', 10: 'bus', 11: 'bicycle', 12: 'chair',
                                 13: 'diningtable', 14: 'pottedplant', 15: 'bird', 16: 'cat', 17: 'motorbike',
                                 18: 'sheep', 19: 'sofa', 20: 'bg'}
            cls.class_mapping_rev = {v: k for k, v in cls.class_mapping.items()}
            print(cls.class_mapping)
            
            classifier = nn.classifier(feature_map_input, roi_input, cls.C.num_rois, nb_classes=len(cls.class_mapping),
                                       trainable=True)

            cls.model_rpn = Model(img_input, rpn_layers)
            cls.model_classifier_only = Model([feature_map_input, roi_input], classifier)

            cls.model_classifier = Model([feature_map_input, roi_input], classifier)

            weights_loc = get_weight('model_frcnn.hdf5')

            print('Loading weights from {}'.format(weights_loc))
            cls.model_rpn.load_weights(weights_loc, by_name=True)
            cls.model_classifier.load_weights(weights_loc, by_name=True)

            cls.model_rpn.compile(optimizer='sgd', loss='mse')
            cls.model_classifier.compile(optimizer='sgd', loss='mse')

        return cls._instance

    def train(self, train_imgs, valid_imgs):
        """ Currently trained using third party code. """
        pass

    def predict(self, image):
        class_to_color = {self.class_mapping[v]: np.random.randint(0, 255, 3) for v in self.class_mapping}
        bbox_threshold = 0.8
        X, ratio = format_img(image, self.C)
        X = np.transpose(X, (0, 2, 3, 1))
        [Y1, Y2, F] = self.model_rpn.predict(X)
        R = roi_helpers.rpn_to_roi(Y1, Y2, K.image_dim_ordering(), overlap_thresh=0.7)
        R[:, 2] -= R[:, 0]
        R[:, 3] -= R[:, 1]

        # apply the spatial pyramid pooling to the proposed regions
        bboxes = {}
        probs = {}

        for jk in range(R.shape[0] // self.C.num_rois + 1):
            ROIs = np.expand_dims(R[self.C.num_rois * jk:self.C.num_rois * (jk + 1), :], axis=0)
            if ROIs.shape[1] == 0:
                break

            if jk == R.shape[0] // self.C.num_rois:
                # pad R
                curr_shape = ROIs.shape
                target_shape = (curr_shape[0], self.C.num_rois, curr_shape[2])
                ROIs_padded = np.zeros(target_shape).astype(ROIs.dtype)
                ROIs_padded[:, :curr_shape[1], :] = ROIs
                ROIs_padded[0, curr_shape[1]:, :] = ROIs[0, 0, :]
                ROIs = ROIs_padded

            [P_cls, P_regr] = self.model_classifier_only.predict([F, ROIs])

            for ii in range(P_cls.shape[1]):

                if np.max(P_cls[0, ii, :]) < bbox_threshold or np.argmax(P_cls[0, ii, :]) == (P_cls.shape[2] - 1):
                    continue

                cls_name = self.class_mapping[np.argmax(P_cls[0, ii, :])]

                if cls_name not in bboxes:
                    bboxes[cls_name] = []
                    probs[cls_name] = []

                (x, y, w, h) = ROIs[0, ii, :]

                cls_num = np.argmax(P_cls[0, ii, :])
                try:
                    (tx, ty, tw, th) = P_regr[0, ii, 4 * cls_num:4 * (cls_num + 1)]
                    tx /= self.C.classifier_regr_std[0]
                    ty /= self.C.classifier_regr_std[1]
                    tw /= self.C.classifier_regr_std[2]
                    th /= self.C.classifier_regr_std[3]
                    x, y, w, h = roi_helpers.apply_regr(x, y, w, h, tx, ty, tw, th)
                except:
                    pass
                bboxes[cls_name].append(
                    [self.C.rpn_stride * x, self.C.rpn_stride * y, self.C.rpn_stride * (x + w), self.C.rpn_stride * (y + h)])
                probs[cls_name].append(np.max(P_cls[0, ii, :]))

        all_dets = []

        for key in bboxes:
            bbox = np.array(bboxes[key])

            new_boxes, new_probs = roi_helpers.non_max_suppression_fast(bbox, np.array(probs[key]), overlap_thresh=0.5)
            for jk in range(new_boxes.shape[0]):
                (x1, y1, x2, y2) = new_boxes[jk, :]

                (real_x1, real_y1, real_x2, real_y2) = get_real_coordinates(ratio, x1, y1, x2, y2)

                cv2.rectangle(image, (real_x1, real_y1), (real_x2, real_y2),
                              (int(class_to_color[key][0]), int(class_to_color[key][1]), int(class_to_color[key][2])),
                              2)

                textLabel = '{}: {}'.format(key, int(100 * new_probs[jk]))
                all_dets.append(create_box_resp_field(self.class_mapping_rev[key], new_probs[jk], real_x2/255, real_x1/255, real_y2/255, real_y1/255))

                (retval, baseLine) = cv2.getTextSize(textLabel, cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                textOrg = (real_x1, real_y1 - 0)

                cv2.rectangle(image, (textOrg[0] - 5, textOrg[1] + baseLine - 5),
                              (textOrg[0] + retval[0] + 5, textOrg[1] - retval[1] - 5), (0, 0, 0), 2)
                cv2.rectangle(image, (textOrg[0] - 5, textOrg[1] + baseLine - 5),
                              (textOrg[0] + retval[0] + 5, textOrg[1] - retval[1] - 5), (255, 255, 255), -1)
                cv2.putText(image, textLabel, textOrg, cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 1)

        boxes_str = 'Count: ' + str(len(all_dets)) + ', ' + str(all_dets)
        print('Results: ' + boxes_str)
        DataCollector().write(DATA_TYPE_DETECTION, boxes_str)
        return image, all_dets

