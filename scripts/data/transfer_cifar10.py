import pickle
import glob

from database.datasetdb import DatasetDB
from database.entities.datasetentities import DatasetEntity, DatasetImage, DatasetLabel, DatasetLabelName

CIFAR_LOC = "D:\\Files\\datasets\\cifar\\cifar-10-python.tar\\cifar-10-python\\cifar-10-batches-py\\"
DATA_SIZE = 10000
ID_WIDTH = 6


def get_cifar_data(batch_index, type_of_data, file):
    with open(file, 'rb') as fo:
        data_dic = pickle.load(fo, encoding='bytes')

    images = list()
    labels = list()

    id_base_num = batch_index * DATA_SIZE

    for index in range(DATA_SIZE):
        image_id = index + id_base_num
        filename = data_dic[b'filenames'][index].decode("utf-8")
        image_data = data_dic[b'data'][index]
        images.append(DatasetImage(image_id, filename, image_data))
        labels.append(DatasetLabel(image_id, 'CIFAR10', type_of_data, data_dic[b'labels'][index]))

    return DatasetEntity(images, labels)


def transfer_data(dataset):
    datasetDb = DatasetDB()

    for image in dataset.get_images():
        datasetDb.insert_image_class(image)

    for label in dataset.get_labels():
        datasetDb.insert_label_data(label)


def run():
    files = glob.glob(CIFAR_LOC + "data_batch*")
    for batch_index, file in enumerate(files):
        dataset = get_cifar_data(batch_index, "train", file)
        transfer_data(dataset)


def test_run():
    files = glob.glob(CIFAR_LOC + "test_batch*")
    for file in files:
        dataset = get_cifar_data(5, "validate", file)
        transfer_data(dataset)

#run()
#test_run()


def set_cifar_label_dic():
    #file = glob.glob(CIFAR_LOC + "batches*")
    with open(CIFAR_LOC + 'batches.meta', 'rb') as fo:
        data_dic = pickle.load(fo, encoding='bytes')

    datasetDb = DatasetDB()
    for index, name in enumerate(data_dic[b'label_names']):
        datasetDb.insert_label_names(DatasetLabelName("CIFAR10", index, name.decode("utf-8")))

#set_cifar_label_dic()

CIFAR_LOC_100 = "D:\\Files\\dataset\\cifar\\cifar-100-python.tar\\cifar-100-python\\test"
def get_cifar_people_data():
    files = glob.glob(CIFAR_LOC_100)
    with open(CIFAR_LOC_100, 'rb') as fo:
        data_dic = pickle.load(fo, encoding='bytes')

    datasetDb = DatasetDB()
    for index, name in enumerate(data_dic[b'label_names']):
        datasetDb.insert_label_names(DatasetLabelName("CIFAR100", index, name.decode("utf-8")))

get_cifar_people_data()