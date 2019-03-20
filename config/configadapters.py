import ast
from common.userparameters import UserParameters
import configparser

# Common Configuration constants
CONFIG_FILE = '//config/system_config'

# Model Configuration constants
MODEL_CONFIG = 'MODEL CONFIG'


class ModelConfig(object):

    def __init__(self):
        config_parser = configparser.ConfigParser()
        config_parser.read(UserParameters().get_base_path() + CONFIG_FILE)
        self.model = config_parser[MODEL_CONFIG]['MODEL']

    def model(self):
        return self.model


# Threshold Configuration constants
THRESHOLDS = 'THRESHOLDS'


class ThresholdConfig(object):

    def __init__(self):
        config_parser = configparser.ConfigParser()
        config_parser.read(UserParameters().get_base_path() + CONFIG_FILE)
        self.prediction_accuracy = config_parser[THRESHOLDS]['PREDICTION_ACCURACY']
        self.battery_percent = config_parser[THRESHOLDS]['BATTERY_PERCENT']
        self.computation_time = config_parser[THRESHOLDS]['COMPUTATION_TIME']
        self.send_image_traffic = config_parser[THRESHOLDS]['SEND_IMAGE_TRAFFIC']
        self.train_size = config_parser[THRESHOLDS]['TRAIN_SIZE']
        self.train_error_rate = config_parser[THRESHOLDS]['TRAIN_ERROR_RATE']

    def prediction_accuracy(self):
        return self.__prediction_accuracy

    def battery_percent(self):
        return self.__battery_percent

    def computation_time(self):
        return self.__computation_time

    def send_image_traffic(self):
        return self.__send_image_traffic

    def train_size(self):
        return self.__train_size

    def train_error_rate(self):
        return self.__train_error_rate


# System Configuration constants
SYSTEM = 'SYSTEM'
WINDOWS = 'WINDOWS'
LINUX = 'LINUX'

# Component Configuration constants
NODE = 'NODE'
EDGE = 'EDGE'
CLOUD = 'CLOUD'


class SystemConfig(object):

    def __init__(self):
        config_parser = configparser.ConfigParser()
        config_parser.read(UserParameters().get_base_path() + CONFIG_FILE)
        #config_parser.read('D://Files//Box Sync//research//source code//Grit//' + CONFIG_FILE)
        self.is_cluster = config_parser[SYSTEM]['CLUSTER']
        self.is_larger_model = config_parser[SYSTEM]['USE_LARGER_MODEL']
        self.is_battery_saver = config_parser[SYSTEM]['BATTERY_SAVER']
        self.is_save_images = config_parser[SYSTEM]['SAVE_IMAGES']
        self.is_train = config_parser[SYSTEM]['TRAIN']
        self.component = config_parser[SYSTEM]['COMPONENT']

    def is_cluster(self):
        return self.__is_cluster == "ON"

    def is_larger_model(self):
        return self.__is_larger_model == "ON"

    def is_battery_saver(self):
        return self.__is_battery_saver == "ON"

    def is_save_images(self):
        return self.__is_save_images == "ON"

    def is_train(self):
        return self.__is_train == "ON"

    def component(self):
        return self.component


# E System Model Configuration constants
E_FUSION = 'E_FUSION'


class EFusionConfig(object):

    def __init__(self):
        config_parser = configparser.ConfigParser()
        config_parser.read(UserParameters().get_base_path() + CONFIG_FILE)
        self.classes = list(config_parser[E_FUSION]['CLASSES'].split(','))
        self.image_size_width = int(config_parser[E_FUSION]['IMAGE_SIZE_WIDTH'])
        self.image_size_height = int(config_parser[E_FUSION]['IMAGE_SIZE_HEIGHT'])
        self.alpha = float(config_parser[E_FUSION]['ALPHA'])
        self.boxes_per_cell = int(config_parser[E_FUSION]['BOXES_PER_CELL'])
        self.object_scale = float(config_parser[E_FUSION]['OBJECT_SCALE'])
        self.no_object_scale = float(config_parser[E_FUSION]['NO_OBJECT_SCALE'])
        self.class_scale = float(config_parser[E_FUSION]['CLASS_SCALE'])
        self.coord_scale = float(config_parser[E_FUSION]['COORD_SCALE'])
        self.learning_rate = float(config_parser[E_FUSION]['LEARNING_RATE'])
        self.decay_steps = int(config_parser[E_FUSION]['DECAY_STEPS'])
        self.decay_rate = float(config_parser[E_FUSION]['DECAY_RATE'])
        self.batch_size = int(config_parser[E_FUSION]['BATCH_SIZE'])
        self.epoch = int(config_parser[E_FUSION]['EPOCH'])
        self.max_iter = int(config_parser[E_FUSION]['MAX_ITER'])
        self.summary_iter = int(config_parser[E_FUSION]['SUMMARY_ITER'])
        self.save_iter = int(config_parser[E_FUSION]['SAVE_ITER'])
        self.threshold = float(config_parser[E_FUSION]['THRESHOLD'])
        self.iou_threshold = float(config_parser[E_FUSION]['IOU_THRESHOLD'])
        self.num_cameras = int(config_parser[E_FUSION]['NUM_CAMERAS'])
        self.weight_file = config_parser[E_FUSION]['WEIGHT_FILE']
        self.staircase = config_parser[E_FUSION]['STAIRCASE']
        self.gpu = float(config_parser[E_FUSION]['GPU'])
        self.output_file = config_parser[E_FUSION]['OUTPUT_FILE']
        self.grid_h = int(config_parser[E_FUSION]['GRID_H'])
        self.grid_w = int(config_parser[E_FUSION]['GRID_W'])
        self.n_anchors = config_parser[E_FUSION]['N_ANCHORS']
        self.anchors = ast.literal_eval(config_parser[E_FUSION]['ANCHORS'])

    def classes(self):
        return self.classes

    def image_size_width(self):
        return self.image_size_width

    def image_size_height(self):
        return self.image_size_height

    def alpha(self):
        return self.alpha

    def boxes_per_cell(self):
        return self.boxes_per_cell

    def object_scale(self):
        return self.object_scale

    def no_object_scale(self):
        return self.no_object_scale

    def class_scale(self):
        return self.class_scale

    def coord_scale(self):
        return self.coord_scale

    def learning_rate(self):
        return self.learning_rate

    def decay_steps(self):
        return self.decay_steps

    def decay_rate(self):
        return self.decay_rate

    def batch_size(self):
        return self.batch_size

    def epoch(self):
        return self.epoch

    def max_iter(self):
        return self.max_iter

    def summary_iter(self):
        return self.summary_iter

    def save_iter(self):
        return self.save_iter

    def threshold(self):
        return self.threshold

    def iou_threshold(self):
        return self.iou_threshold

    def num_cameras(self):
        return self.num_cameras

    def weight_file(self):
        return self.weight_file

    def staircase(self):
        return self.staircase

    def gpu(self):
        return self.gpu

    def output_file(self):
        return self.output_file

    def grid_h(self):
        return self.grid_h

    def grid_w(self):
        return self.grid_w

    def n_anchors(self):
        return self.n_anchors

    def anchors(self):
        return self.anchors
