from common.userparameters import UserParameters
from config.configadapters import CLOUD
import database.googlecloudstorage as gcs


def get_weight(file_name):
    component = UserParameters().get_component()

    if component == CLOUD:
        return gcs.get_weights(file_name)
    else:
        return UserParameters().get_base_path() + '/weights/' + str(file_name)