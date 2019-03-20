from model.multiviewconfprop import multi_view_predict
import threading
sem = threading.Semaphore(1)


def some_func(data, frame_num, pred1, pred2, an_arg = 0):
    multi_view_predict(pred1, pred2)
    data.set_pred_update(frame_num, 1)
    data.set_pred_update(frame_num, 2)
    data.set_pred_update(frame_num, 3)
    data.set_pred_update(frame_num, 4)


class MultiviewManager(object):
    _instance = None

    def __new__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super().__new__(self, *args, **kwargs)
            self.data = MultiviewDataStructure()
            self.count = 0
        return self._instance

    def manage_data(self, frame_num, cam_num, image):
        self.data.update_data(frame_num, cam_num, image)
        if self.data.is_all_images_exist(frame_num):
            # Run multiview
            multiview_thread = threading.Thread(target=some_func,
                                  args=(self.data, frame_num, self.data.get_data(frame_num).get_pred(1), self.data.get_data(frame_num).get_pred(2)),#, self.data.get_data(frame_num).get_pred(3), self.data.get_data(frame_num).get_pred(4)),
                                  kwargs={"an_arg": 4})
            multiview_thread.start()
            if self.count > 15:
                for num in range(15):
                    self.data.clear_data(num + 1)

    def get_results(self, frame_num, cam_num):
        return self.data.get_results(frame_num, cam_num)

    def is_result_exist(self, frame_num):
        # semaphore needed
        return self.data.is_results_exist(frame_num)


class CameraPredictions(object):

    def __init__(self):
        self.cam_1_pred = None
        self.cam_1_new_pred = None
        self.cam_1_updated = False
        self.cam_2_pred = None
        self.cam_2_new_pred = None
        self.cam_2_updated = False
        self.cam_3_pred = None
        self.cam_3_new_pred = None
        self.cam_3_updated = False
        self.cam_4_pred = None
        self.cam_4_new_pred = None
        self.cam_4_updated = False

    def set_pred(self, cam_num, pred):
        if cam_num == 1:
            self.cam_1_pred = pred
        elif cam_num == 2:
            self.cam_2_pred = pred
        elif cam_num == 3:
            self.cam_3_pred = pred
        elif cam_num == 4:
            self.cam_4_pred = pred
        else:
            raise Exception('Not valid cam num: ' + str(cam_num))

    def get_pred(self, cam_num):
        if cam_num == 1:
            pred = self.cam_1_pred
            if self.is_cam_updated(cam_num):
                self.cam_1_pred = None
            return pred
        elif cam_num == 2:
            pred = self.cam_2_pred
            if self.is_cam_updated(cam_num):
                self.cam_2_pred = None # Eman here
            return pred
        elif cam_num == 3:
            pred = self.cam_3_pred
            if self.is_cam_updated(cam_num):
                self.cam_3_pred = None # Eman here
            return pred
        elif cam_num == 4:
            pred = self.cam_4_pred
            if self.is_cam_updated(cam_num):
                self.cam_4_pred = None # Eman here
            return pred
        else:
            raise Exception('Not valid cam num: ' + str(cam_num))

    def set_update(self, cam_num):
        if cam_num == 1:
            self.cam_1_updated = True
        elif cam_num == 2:
            self.cam_2_updated = True
        elif cam_num == 3:
            self.cam_3_updated = True
        elif cam_num == 4:
            self.cam_4_updated = True
        else:
            raise Exception('Not valid cam num: ' + str(cam_num))

    def is_cam_updated(self, cam_num):
        if cam_num == 1:
            return self.cam_1_updated
        elif cam_num == 2:
            return self.cam_2_updated # Eman here
        elif cam_num == 3:
            return self.cam_3_updated # Eman here
        elif cam_num == 4:
            return self.cam_4_updated # Eman here
        else:
            raise Exception('Not valid cam num: ' + str(cam_num))


class MultiviewDataStructure(object):

    def __init__(self):
        self.data = dict()

    def get_data_structure(self):
        sem.acquire()
        return self.data

    def update_data(self, frame_num, cam_num, pred):
        data = self.get_data_structure()
        if frame_num in data:
            frame_data = data[frame_num]
            frame_data.set_pred(cam_num, pred)
            data[frame_num]
        else:
            frame_data = CameraPredictions()
            frame_data.set_pred(cam_num, pred)
            data[frame_num] = frame_data
        sem.release()

    def set_pred_update(self, frame_num, cam_num):
        self.get_data_structure()[frame_num].set_update(cam_num)
        sem.release()

    def get_data(self, frame_num):
        data = self.get_data_structure()[frame_num]
        sem.release()
        return data

    def clear_data(self, frame_num):
        del self.get_data_structure()[frame_num]
        sem.release()

    def is_all_images_exist(self, frame_num):
        data = self.get_data_structure()
        if len(data) <= 0:
            sem.release()
            return False
        frame_data = data[frame_num]
        if frame_data.get_pred(1) is None \
                or frame_data.get_pred(2) is None:# \
                #or frame_data.get_pred(3) is None \
                #or frame_data.get_pred(4) is None:
            sem.release()
            return False
        sem.release()
        return True

    def is_results_exist(self, frame_num):
        data = self.get_data_structure()
        if len(data) <= 0:
            sem.release()
            return False
        frame_data = data[frame_num]
        if frame_data.is_cam_updated(1) and frame_data.is_cam_updated(2):# and frame_data.is_cam_updated(3) and frame_data.is_cam_updated(4):
            sem.release()
            return True
        sem.release()
        return False

    def get_results(self, frame_num, cam_num):
        data = self.get_data_structure()
        frame_data = data[frame_num]
        result = frame_data.get_pred(cam_num)
        sem.release()
        return result
