import cv2
import numpy as np
from keras.utils import Sequence

from database.builder.datasetbuilder import AnnotationFindBuilder, ImageFindBuilder, LabelFindBuilder
from database.datasetdbv2 import DatasetDBV2, DATASET_CIFAR
from training.datasets.imgaug import augmenters as iaa


class Cifar10Batch(Sequence):
    def __init__(self, type_of_data):
        self.type_of_data = type_of_data
        self.image_size_height = 32
        self.image_size_width = 32
        self.batch_size = 10
        self.counter = 0
        self.images_index = None
        if 'train' in type_of_data:
            self.images_index = [index for index in range(0, 50000)]
        else:
            self.images_index = [index for index in range(50000, 60000)]

        self.cifar10dataDb = DatasetDBV2(DATASET_CIFAR)
        find_builder = LabelFindBuilder()
        self.labels = self.cifar10dataDb.find_label_data(find_builder.build())

        self.aug_pipe = iaa.Sequential(
            [
                iaa.Sometimes(0.5,
                          iaa.Crop(percent=(0, 0.2)),
                          iaa.Affine(rotate=(-45, 45)),
                          iaa.AddToHueAndSaturation((-20, 20)),
                        # execute 0 to 5 of the following (less important) augmenters per image
                        # don't execute all of them, as that would often be way too strong
                        iaa.SomeOf((0, 5),
                            [
                                iaa.OneOf([
                                    iaa.GaussianBlur((0, 3.0)), # blur images with a sigma between 0 and 3.0
                                    iaa.AverageBlur(k=(2, 7)), # blur image using local means with kernel sizes between 2 and 7
                                    iaa.MedianBlur(k=(3, 11)), # blur image using local medians with kernel sizes between 2 and 7
                                ]),
                                iaa.Sharpen(alpha=(0, 1.0), lightness=(0.75, 1.5)), # sharpen images
                                iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05*255), per_channel=0.5), # add gaussian noise to images
                                iaa.OneOf([
                                    iaa.Dropout((0.01, 0.1), per_channel=0.5), # randomly remove up to 10% of the pixels
                                ]),
                                iaa.Add((-10, 10), per_channel=0.5), # change brightness of images (by -10 to 10 of original value)
                                iaa.Multiply((0.5, 1.5), per_channel=0.5), # change brightness of images (50-150% of original value)
                                iaa.ContrastNormalization((0.5, 2.0), per_channel=0.5), # improve or worsen the contrast
                            ],
                            random_order=True
                        ))
            ],
            random_order=True
        )
        np.random.shuffle(self.images_index)

    def __len__(self):
        # Multiple input batch will have hte same length based on one input image set.
        return int(np.ceil(float(len(self.images_index))/self.batch_size))

    def __getitem__(self, idx):
        # dataset will be split based on batch size.
        l_bound = idx * self.batch_size
        r_bound = (idx + 1) * self.batch_size

        if r_bound > len(self.images_index):
            r_bound = len(self.images_index)
            l_bound = r_bound - self.batch_size

        # initialize batches to 0 np arrays
        x_batch = np.zeros((r_bound - l_bound, self.image_size_height, self.image_size_width, 3))
        y_batch = np.zeros((r_bound - l_bound, len(self.labels)))

        instance_count = 0

        for data_index in self.images_index[l_bound:r_bound]:
            image_find_builder = ImageFindBuilder()
            image_find_builder.build_image_id(data_index)
            image = self.cifar10dataDb.find_image_data(image_find_builder.build())[0].get_image()
            image = image.astype(np.float32, copy=False)
            image = self.aug_pipe.augment_image(image)
            image = cv2.resize(image, (self.image_size_height, self.image_size_width))
            image = image[:, :, ::-1]  # BGR -> RGB

            annotation_find_builder = AnnotationFindBuilder()
            annotation_find_builder.build_image_id(data_index)
            annotation = self.cifar10dataDb.find_annotation_data(annotation_find_builder.build())[0]

            x_batch[instance_count] = self.norm(image)
            y_batch[instance_count] = self.get_y(annotation.get_label())

            instance_count = instance_count + 1

        self.counter += 1

        return x_batch, y_batch

    def get_y(self, label_value):
        y = np.zeros(len(self.labels), dtype=int)
        y[label_value] = 1
        return y

    def on_epoch_end(self):
        np.random.shuffle(self.images_index)
        self.counter = 0

    def norm(self, x):
        """
                argument
                    - x: input image data in numpy array [32, 32, 3]
                return
                    - normalized x
            """
        min_val = np.min(x)
        max_val = np.max(x)
        x = (x - min_val) / (max_val - min_val)
        return x