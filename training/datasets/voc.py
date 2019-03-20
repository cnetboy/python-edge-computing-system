import cv2
import numpy as np

from keras.utils import Sequence

from common.yolov2detectorconfig import *


class VOCBatch(Sequence):
    def __init__(self, image_ids):
        self.counter = 0
        self.dataset = image_ids
        np.random.shuffle(self.dataset)

    def __len__(self):
        return int(np.ceil(float(len(self.dataset))/BATCH_SIZE))

    def __getitem__(self, idx):
        l_bound = idx * BATCH_SIZE
        r_bound = (idx + 1) * BATCH_SIZE

        if r_bound > len(self.dataset):
            r_bound = len(self.dataset)
            l_bound = r_bound - BATCH_SIZE

        input_images = np.zeros((r_bound - l_bound, IMAGE_H, IMAGE_W, IMAGE_DIM))  # input images
        output_object_detections = np.zeros((r_bound - l_bound, GRID_H, GRID_W, NUM_ANCHORS, NUM_ANCHORS_PARAMS), dtype=np.float32)
        masks = np.zeros((r_bound - l_bound, GRID_H, GRID_W, NUM_ANCHORS, NUM_ANCHORS_PARAMS), dtype=np.float32)

        for data_index, data in enumerate(self.dataset[l_bound:r_bound]):
            data_image = cv2.imread(data.get_file_name())
            numpy_images, numpy_annotations, mask = run_yolov2tiny_imageprepsteps(data_image, data)
            input_images[data_index] = numpy_images
            output_object_detections[data_index] = numpy_annotations
            masks[data_index] = mask

        return [input_images, masks], output_object_detections

    def on_epoch_end(self):
        np.random.shuffle(self.dataset)


