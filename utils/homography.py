import cv2
import numpy as np


def get_point(point, homography, homography_for_search_point):
    homography_inv = np.linalg.inv(homography)
    new_point = np.matmul(homography_for_search_point, homography_inv)
    new_point = np.matmul(new_point, point)
    return new_point

def get_ground_point(point, homography):
    return np.matmul(homography, point)

def compare_two_points():
    point1 = np.array([[68*288*.31], [85*288*.31], [1*288*.31]])
    homography1 = np.array([[-0.211332, -0.405226, 70.781223],
                            [-0.019746, -1.564936, 226.377280],
                            [-0.000025, -0.001961, 0.160791]])
    test1 = np.matmul(np.linalg.inv(homography1), point1)
    point2 = np.array([[258*288*.25], [69*288*.25], [1*288*.25]])
    homography2 = np.array([[0.000745, 0.350335, -98.376103],
                            [-0.164871, -0.390422, 54.081423],
                            [0.000021, -0.001668, 0.111075]])
    test2 = np.matmul(homography2, point2)
    #expected_point2 = get_point(point1, homography1, homography2)


    print('done')
    #return expected_point2 == point2


print(compare_two_points())