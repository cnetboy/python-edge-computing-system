from flask import jsonify, Flask
from common.observer import Subject
from devices.ina219sensor import INA219DCCurrentSensor

# Initialize flask server
app = Flask(__name__)


def create_app(update_chain):
    subject = Subject()
    subject.attach(update_chain)
    ina219Sensor = INA219DCCurrentSensor()

    @app.route('/status/battery', methods=['GET'])
    def status_battery():
        return jsonify(battery_percent=float(ina219Sensor.get_power() / 100.0))

    @app.route('/chain/update/<view>/<processor>', methods=['GET'])
    def update_chain(view, processor):
        subject.subject_state = str(view) + str(processor)
        return jsonify(newstate=subject.subject_state)

    return app
