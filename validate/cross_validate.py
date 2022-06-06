# coding: utf-8
import copy

from main import idw
from main import load_points
from util import statistics
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import numpy as np

default_sheet_index = 0
default_has_title = True


def cross_interpolation(points):
    predict_points = []
    for i in range(len(points)):
        temp_measure_points = copy.deepcopy(points)
        temp_predict_point = temp_measure_points.pop(i)
        z = idw.interpolation(temp_predict_point[0], temp_predict_point[1], temp_measure_points,
                              len(temp_measure_points))
        temp_predict_point[2] = z
        predict_points.append(temp_predict_point)

    return predict_points


def process(path, sheet_index, lon_index, lat_index, z_index, has_title):
    all_points = load_points.load_by_excel(path, sheet_index, lon_index, lat_index, z_index, has_title)
    predict_points = cross_interpolation(all_points)

    for i in range(len(all_points)):
        print('predict point :{} ,   measure point : {}'.format(predict_points[i], all_points[i]))

    measure_zs = np.array(all_points)[..., 2]
    predict_zs = np.array(predict_points)[..., 2]

    print('ME: {}'.format(statistics.me(measure_zs, predict_zs)))
    print('RMSE: {}'.format(mean_squared_error(measure_zs, predict_zs) ** .5))
    print('R2: {}'.format(r2_score(measure_zs, predict_zs)))


if __name__ == '__main__':
    excel_file = '/Users/cakemonster/Desktop/statics/ace1.xls'
    _lon_index = 1
    _lat_index = 2
    _z_index = 3
    process(excel_file, default_sheet_index, _lon_index, _lat_index, _z_index, default_has_title)
