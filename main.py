"""
Main method that starts up threads and web services
based on whether the software is ran on a NODE, EDGE
or CLOUD device.

"""

import argparse
from common.userparameters import UserParameters
from config.configadapters import NODE, EDGE, CLOUD, WINDOWS
import os
import sys


def get_base_path():
    base_path = os.path.dirname(sys.argv[0])
    full_base_path = os.path.abspath(base_path)
    return full_base_path


def get_urls(component, urls):
    if component is NODE:
        return urls[1], urls[2]
    elif component is EDGE:
        return urls[0], urls[2]
    else:
        return urls[0], urls[1]


def run_main():
    parser = argparse.ArgumentParser(description='Initial values set up.')
    parser.add_argument('-s','--system', help='Operating System, either WINDOWS or LINUX',
                        required='True', default=WINDOWS)
    parser.add_argument('-c', '--component', help='System Component, either NODE, EDGE or CLOUD',
                        required='True', default=EDGE)
    parser.add_argument('-m', '--model', help='Object Detection Model, either YOLOV2 or FASTERRCNN',
                        required='True', default='YOLOV2')
    parser.add_argument('-v', '--video', help='Video location if exist', default='NONE')
    parser.add_argument('-C', '--camnum', help='Camera number of node. Applies only for Node component.',
                        default='NONE')
    parser.add_argument('-nurl', '--nodeurl', help='IP Address of Node', default='localhost')
    parser.add_argument('-eurl', '--edgeurl', help='IP Address of Edge', default='localhost')
    parser.add_argument('-curl', '--cloudurl', help='IP Address of Cloud', default='localhost')
    arguments = parser.parse_args(sys.argv[1:])
    system = arguments.system
    base_path = get_base_path()
    component = arguments.component
    model = arguments.model
    video_file_loc = arguments.video
    cam_num = arguments.camnum
    url = get_urls(component, [arguments.nodeurl, arguments.edgeurl, arguments.cloudurl])
    user_parameters = UserParameters(system, base_path, component, model, video_file_loc, cam_num, url)
    app_component = user_parameters.get_component()
    if app_component == NODE:
        import app.mainnode as node
        node.main()
    elif app_component == EDGE:
        import app.mainedge as edge
        edge.main()
    elif app_component == CLOUD:
        import app.maincloud as cloud
        cloud.main()
    else:
        raise Exception('Application not set up for component: ' + str(app_component))


run_main()
