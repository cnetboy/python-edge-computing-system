CLASS_DIC =\
    {
        "background": 0,
        "aeroplane": 1,
        "bicycle": 2,
        "bird": 3,
        "boat": 4,
        "bottle": 5,
        "bus": 6,
        "car": 7,
        "cat": 8,
        "chair": 9,
        "cow": 10,
        "diningtable": 11,
        "dog": 12,
        "horse": 13,
        "motorbike": 14,
        "person": 15,
        "pottedplant": 16,
        "sheep": 17,
        "sofa": 18,
        "train": 19,
        "tvmonitor": 20,
        "unknown": 21,
    }

IMAGE_H = 416
IMAGE_W = 416
IMAGE_DIM = 3

GRID_H = 13
GRID_W = 13

ANCHORS = [(1.08,1.19), (3.42,4.41), (6.63,11.38), (9.42,5.11), (16.62,10.52)]

NUM_CLASSES = len(CLASS_DIC)

NUM_ANCHORS = len(ANCHORS)
NUM_ANCHORS_PARAMS = 5 + NUM_CLASSES  # (obj, x, y, w, h, c1, c2, ...c20)
PRIORS = np.array([
    1.08, 1.19, 3.42, 4.41, 6.63, 11.38, 9.42, 5.11, 16.62, 10.52
]).reshape(5, 2)

BATCH_SIZE = 64

LAMBDA_COORD = 5.0
LAMBDA_NO_OBJ = 0.5

LEARNING_RATE_INIT = 0.0005
MOMENTUM_INIT = 0.9
WEIGHT_DECAY_INIT = 0.0005

EPOCH = 160

