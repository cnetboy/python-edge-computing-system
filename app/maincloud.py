from common.userparameters import UserParameters
from config.configadapters import WINDOWS, LINUX
from endpoints import cloudendpoint
system = str(UserParameters().get_system())
if system == WINDOWS:
    from waitress import serve


def main():
    if system == WINDOWS:
        serve(cloudendpoint.create_app(), host='0.0.0.0', port=8082)
    elif system == LINUX:
        cloudendpoint.create_app().run(host='0.0.0.0')
    else:
        raise Exception('Invalid system: ' + str(system))


if __name__ == '__main__':
    main()
