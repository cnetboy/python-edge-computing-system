from common.userparameters import UserParameters
from config.configadapters import WINDOWS, LINUX
from endpoints import nodeendpoint
from processors.chains.nodechain import CameraChain
import threading
system = str(UserParameters().get_system())
if system == WINDOWS:
    from waitress import serve


def run_camera(camera_chain):
    video_file_loc = str(UserParameters().get_video_file_loc())
    if video_file_loc == 'NONE':
        from devices.camera import run_camera as camera
        camera(camera_chain)
    elif video_file_loc == "RECORDING":
        from devices.camerarecord import run_camera as camera
        camera()
    else:
        from devices.camerasimulation import run_camera as camera
        camera(camera_chain, video_file_loc)


def run_service(camera_chain):
    if system == WINDOWS:
        serve(nodeendpoint.create_app(camera_chain), host='0.0.0.0', port=8081)
    elif system == LINUX:
        nodeendpoint.create_app(camera_chain).run(host='0.0.0.0', port=8081)
    else:
        raise Exception('Invalid system: ' + str(system))


def main():
    camera_chain = CameraChain()
    service_thread = threading.Thread(name='service', target=run_service, args=(camera_chain,))
    service_thread.start()
    run_camera(camera_chain)


if __name__ == '__main__':
    main()
