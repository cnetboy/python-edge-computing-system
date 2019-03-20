from common.userparameters import UserParameters
from config.configadapters import WINDOWS, LINUX
from endpoints import edgeendpoint
import threading
system = str(UserParameters().get_system())
if system == WINDOWS:
    from waitress import serve


def run_system_processing_speed_monitoring():
    pass  # This is in private github account


def run_network_traffic_monitoring():
    pass  # This is in private github account


def run_service():
    if system == WINDOWS:
        serve(edgeendpoint.create_app(), host='0.0.0.0', port=8080)
    elif system == LINUX:
        edgeendpoint.create_app().run(host='0.0.0.0')
    else:
        raise Exception('Invalid system: ' + str(system))


def main():
    service_thread = threading.Thread(name='monitor_system_processing_speed', target=run_system_processing_speed_monitoring)
    service_thread.start()
    service_thread = threading.Thread(name='monitor_network_traffic', target=run_network_traffic_monitoring)
    service_thread.start()
    run_service()


if __name__ == '__main__':
    main()
