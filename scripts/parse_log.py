import re

BASE_PATH = 'C:\\Users\\emman\\Desktop\\research_paper_2\\finalexperiments\\4cam\\'


def create_data_file(file_name, data_name, data_list):
    with open(BASE_PATH + file_name + '_' + data_name + '.txt', 'w+') as fd:
        fd.write(data_name + ':: \r\n')
        data_count = 0
        data_added = 0.0
        for data in data_list:
            fd.write(data + '\r\n')
            data_count = data_count + 1
            data_added = data_added + float(data)
        fd.write('\r\nAverage:: ' + str(float(data_added / data_count)))


def parse_data(pattern, file_content):
    collected_data = re.findall(pattern, file_content)
    return [data[1] for data in collected_data]


files_to_parse = \
[
    '2edge2edgetocloud_cam1cloud',
    '2edge2edgetocloud_cam3cloud',
    '2edge2edgetocloud_cam4edge',
]

PROCESSING_PATTERN = '(.*?PROCESSING TIME.*?::\s)(\d+.\d+)'
COMPUTE_TIME_PATTERN = '(.*?COMPUTING TIME.*?::\s)(\d+.\d+)'
DATA_TRANSFER_TIME_PATTERN = '(.*?DATA TRANSFER TIME.*?::\s)(\d+.\d+)'
TRANSFER_SIZE_PATTERN = '(.*?TRANSFER SIZE.*?::\s)(\d+.\d+)'

patterns = [("PROCESSING TIME", PROCESSING_PATTERN),
            #("COMPUTE TIME", COMPUTE_TIME_PATTERN),
            ("DATA TRANSFER TIME", DATA_TRANSFER_TIME_PATTERN),
            ("TRANSFER SIZE", TRANSFER_SIZE_PATTERN)]

for file in files_to_parse:
    with open(BASE_PATH + file + '.log', 'r') as fd:
        file_content = fd.read()
        for pattern in patterns:
            relevant_data = parse_data(pattern[1], file_content)
            create_data_file(file, pattern[0], relevant_data)
