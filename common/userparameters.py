MODEL_YOLOV2 = "YOLOV2"
MODEL_FASTERRCNN = "FASTERRCNN"


class UserParameters(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            if len(args) > 0:
                cls.system = args[0]
                cls.base_path = args[1]
                cls.component = args[2]
                cls.none_node_model = args[3]
                cls.video_file_loc = args[4]
                cls.cam_num = args[5]
                if cls.component == 'NODE':
                    cls.node_ip = 'localhost:8080'
                    cls.edge_ip = args[6][0]
                    cls.cloud_ip = args[6][1]
                if cls.component == 'EDGE':
                    cls.edge_ip = 'localhost:8080'
                    cls.node_ip = args[6][0]
                    cls.cloud_ip = args[6][1]
                if cls.component == 'CLOUD':
                    cls.cloud_ip = 'localhost:8080'
                    cls.node_ip = args[6][0]
                    cls.edge_ip = args[6][1]
            else:
                cls.system = ''
                cls.base_path = ''
                cls.component = ''
                cls.none_node_model = ''
        return cls._instance

    def get_system(self):
        return self.system

    def get_base_path(self):
        return self.base_path

    def get_component(self):
        return self.component

    def get_none_node_model(self):
        return self.none_node_model

    def get_video_file_loc(self):
        return self.video_file_loc

    def get_cam_num(self):
        return self.cam_num

    def get_node_ip(self):
        return self.node_ip

    def get_edge_ip(self):
        return self.edge_ip

    def get_cloud_ip(self):
        return self.cloud_ip
