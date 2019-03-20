import pickle

from flask import request, jsonify, Flask
from time import time as timer

from processors.chains.edgechain import SingleViewChain, MultiViewChain
import processors.processorrequest as preq
import clients.edgerequest as creq
from common.logger import get_logger
from common.observer import Subject
from model.yolov2tiny import YoloV2Tiny

my_logger = get_logger(__name__)

# Initialize flask server
app = Flask(__name__)


def process_img_request(ip, image, frame, cam, processor_chain):
    incoming_request = creq.EdgeRequest(ip, image, frame, cam)
    processor_request = preq.ProcessorRequest(incoming_request)
    return processor_chain.run(processor_request)


def create_box_resp_field(box):
    resp_fields = dict()
    if type(box) is dict:
        return box

    resp_fields['label'] = int(box.label)
    resp_fields['score'] = float(box.score)
    resp_fields['xmax'] = float(box.xmax)
    resp_fields['xmin'] = float(box.xmin)
    resp_fields['ymax'] = float(box.ymax)
    resp_fields['ymin'] = float(box.ymin)
    return resp_fields


def create_app():
    single_view_chain = SingleViewChain()
    multi_view_chain = MultiViewChain()
    subject = Subject()
    subject.attach(single_view_chain)
    subject.attach(multi_view_chain)

    @app.route('/chain/update/<view>/<processor>', methods=['GET'])
    def update_chain(view, processor):
        subject.subject_state = str(view) + str(processor)
        return jsonify(update='received')

    @app.route('/ip', methods=['GET'])
    def ip():
        return jsonify({'ip': request.remote_addr}), 200

    def process_image(processor):
        my_logger.info('process_image__full():: Request entering in Edge.')
        start_time = timer()
        image = pickle.load(request.files.get('file'))

        try:
            my_logger.info('process_image__full():: Image processing starting.')
            processor_response = process_img_request(str(request.remote_addr), image, 1, 1, processor)
            my_logger.info('process_image__full():: Image processing completed.')
        except OSError:
            my_logger.error('process_image__full():: Error during image processing. Return original request to client.')
            return jsonify(prediction=[], computational_time=[str(timer() - start_time)])

        duration = str(timer() - start_time)
        print('Computational Time: ' + duration)
        if len(processor_response.boxed_loc) <= 0:
            content = jsonify(prediction=[],
                              computational_time=[str(duration)]
                              )
        else:
            if processor_response.computational_time is not None:
                computational_time = [str(duration), str(processor_response.computational_time)]
            else:
                computational_time = [str(duration)]
            content = jsonify(
                prediction=[create_box_resp_field(box) for box in processor_response.boxed_loc],
                computational_time=computational_time
            )
        return content

    @app.route('/process/image/singleview', methods=['POST'])
    def process_image_single_view():
        return process_image(single_view_chain.get_processor())

    @app.route('/process/image/multiview', methods=['POST'])
    def process_image_multi_view():
        my_logger.info('process_image__full():: Request entering in Edge.')

        request_json = request.get_json()

        try:
            my_logger.info('process_image__full():: Image processing starting.')
            processor_response = process_img_request(str(request.remote_addr), request_json['prediction'],
                                                     request_json['frame'], request_json['cam'],
                                                     multi_view_chain.get_processor())
            my_logger.info('process_image__full():: Image processing completed.')
        except OSError:
            my_logger.error('process_image__full():: Error during image processing. Return original request to client.')
            return jsonify(request_json)

        if processor_response.boxed_loc is None:
            content = jsonify(request_json)
        elif len(processor_response.boxed_loc) <= 0:
            content = jsonify(request_json)
        else:
            content = jsonify(
                prediction=processor_response.boxed_loc,
                computational_time=processor_response.computational_time
            )
        return content

    @app.route('/process/image/quick', methods=['POST'])
    def process_image_quick():
        my_logger.info('process_image__full():: Request entering in Edge for quick detect.')

        image = pickle.load(request.files.get('file'))

        my_logger.info('process_image__full():: Image processing starting.')
        image_annotated, boxes = YoloV2Tiny().predict(image)
        my_logger.info('process_image__full():: Image processing completed.')
        boxes = [create_box_resp_field(box) for box in boxes]
        if len(boxes) <= 0:
            content = jsonify(prediction=[])
        else:
            content = jsonify(
                prediction=boxes
            )
        return content

    return app
