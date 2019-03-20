import cv2
import sys
from time import time as timer

from common.data_collector import DataCollector, DATA_TYPE_PROCESSING_TIME, DATA_TYPE_FPS
from common.userparameters import UserParameters
import processors.processorrequest as preq
import clients.noderequest as creq

QUEUE = 1
FRAME_LIMIT = 15000


def process_img_request(image, cam, frame, processor_chain):
    incoming_request = creq.NodeRequest(image, cam, frame)
    processor_request = preq.ProcessorRequest(incoming_request)
    return processor_chain.run(processor_request)


def run_camera(camera_chain, video_file_loc):
    # buffers for demo in batch
    buffer_inp = list()

    # Loop through frames
    elapsed = 0
    start = timer()
    data_collector = DataCollector()

    print('Video file to open: ' + str(video_file_loc))

    while True:
        frame_num = 0
        while frame_num < FRAME_LIMIT:
            print('Press [ESC] to quit demo')
            camera = cv2.VideoCapture(video_file_loc)
            cam_num = UserParameters().get_cam_num()

            while camera.isOpened():
                elapsed += 1
                _, frame = camera.read()
                frame_num = frame_num + 1
                if frame is None:
                    print('\nEnd of Video')
                    break
                buffer_inp.append(frame)
                # Only process and imshow when queue is full
                if elapsed % QUEUE == 0:
                    for image in buffer_inp:
                        collector_start_time = timer()
                        process_image_response = process_img_request(image, cam_num, frame_num, camera_chain.get_processor())
                        cv2.imshow('', process_image_response.boxed_image)
                        #cv2.imshow('', image)
                        duration = str(timer() - collector_start_time)
                        print('Processing Time: ' + duration)
                        data_collector.write(DATA_TYPE_PROCESSING_TIME, duration)
                    # Clear Buffers
                    buffer_inp = list()

                if elapsed % 5 == 0:
                    sys.stdout.write('\r')
                    fps = elapsed / (timer() - start)
                    sys.stdout.write('{0:3.3f} FPS\n'.format(fps))
                    data_collector.write(DATA_TYPE_FPS, str(fps))
                    sys.stdout.flush()
                choice = cv2.waitKey(1)
                if choice == 27:
                    break

            sys.stdout.write('\n')
            camera.release()
            data_collector.close()
            cv2.destroyAllWindows()

#run_camera()