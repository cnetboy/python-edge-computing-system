from google.cloud import storage


def get_weights(file_name):
    client = storage.Client()
    bucket = client.get_bucket('eman-cloud')
    weights = bucket.get_blob('weights/' + str(file_name)).download_as_string()
    temp_loc = 'temp_weights.h5'
    with open(temp_loc, 'wb') as fd:
        fd.write(weights)

    return temp_loc