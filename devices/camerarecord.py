import cv2
import sys
from time import time as timer


def run_camera():
    camera = cv2.VideoCapture(0)
    assert camera.isOpened(), 'Cannot capture source'

    cv2.namedWindow('', 0)
    _, frame = camera.read()
    height, width, _ = frame.shape
    cv2.resizeWindow('', width, height)

    # buffers for demo in batch
    buffer_inp = list()

    # Loop through frames
    elapsed = 0
    start = timer()
    print('Press [ESC] to quit demo')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # cv2.VideoWriter_fourcc() does not exist
    video_writer = cv2.VideoWriter("/home/pi/source_codes/Grit/recording.avi", fourcc, 20.0, (width, height))
    while camera.isOpened():
        elapsed += 1
        ret, frame = camera.read()
        if ret:
            video_writer.write(frame)
            cv2.imshow('video stream', frame)
        choice = cv2.waitKey(1)
        if choice == 27:
            break

    sys.stdout.write('\n')
    camera.release()
    cv2.destroyAllWindows()
