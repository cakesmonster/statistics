# coding: utf-8
from main import idw
from main import load
from util import statistics
from sklearn.metrics import r2_score
import numpy as np

default_execl_index = 0
default_has_title = True


def cross_interpolation(points):
    all_predict_points = []
    for i in range(len(points)):
        temp_measure_points = []
        temp_predict_point = list.copy(points[i])
        if i == 0:
            temp_measure_points.extend(points[1:])
        else:
            temp_measure_points.extend(points[0: i - 1])
            if i + 1 != len(points):
                temp_measure_points.extend(points[i + 1:])

        z = idw.interpolation(temp_predict_point[0], temp_predict_point[1], temp_measure_points,
                              len(temp_measure_points))
        # print('predict z : {}, measure z :{}'.format(z, temp_predict_point[2]))
        temp_predict_point[2] = z
        all_predict_points.append(temp_predict_point)

    return all_predict_points


def process(path, lon_index, lat_index, z_index):
    all_points = load.load_by_excel(path, default_execl_index, lon_index, lat_index, z_index, default_has_title)
    predict_points = cross_interpolation(all_points)

    for i in range(len(all_points)):
        print('predict z :{} ,   measure z : {}'.format(predict_points[i], all_points[i]))

    measure_zs = np.array(all_points)[..., 2]
    predict_zs = np.array(predict_points)[..., 2]

    print('R2: {}'.format(r2_score(measure_zs, predict_zs)))
    print('ME: {}'.format(statistics.me(measure_zs, predict_zs)))


if __name__ == '__main__':
    process("/Users/cakemonster/Desktop/statics/ace1.xls", 0, 2, 3)
