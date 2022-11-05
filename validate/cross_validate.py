# coding: utf-8
import copy

import argparse
import sys
import os
from main import idw
from main import load_points
from util import statistics
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import numpy as np


def handle_command_line(args):
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input-file', dest='input_file', action='store', type=str, help='need handle file')
    parser.add_argument('--file-type', dest='file_type', action='store', type=str, default='excel',
                        help='input file type, just support excel and csv, default is excel')
    parser.add_argument('--excel-sheet-index', dest='excel_sheet_index', action='store', type=int, default=0,
                        help='handle excel sheet index, default is 0')
    parser.add_argument('--lon-index', dest='lon_index', action='store', type=int, default=1,
                        help='lon column index in input file, default is 1')
    parser.add_argument('--lat-index', dest='lat_index', action='store', type=int, default=2,
                        help='lat column index in input file, default is 2')
    parser.add_argument('--z-index', dest='z_index', action='store', type=int, default=3,
                        help='z column index in input file, default is 3')
    parser.add_argument('--has-title', dest='has_title', action='store_true', default=True,
                        help='input file has title, default is True')
    options = parser.parse_args(args)
    return options


def validate_options(options):
    if not os.path.exists(options.input_file):
        sys.exit('input file is not exist')

    file_type = options.file_type.trim()
    if file_type != 'excel' or file_type != 'csv':
        sys.exit('file type just support excel and csv')


def cross_interpolation(points, distance_limit):
    predict_points = []
    for i in range(len(points)):
        temp_measure_points = copy.deepcopy(points)
        temp_predict_point = temp_measure_points.pop(i)
        z = idw.interpolation(temp_predict_point[0], temp_predict_point[1], temp_measure_points,
                              len(temp_measure_points), distance_limit)
        temp_predict_point[2] = z
        predict_points.append(temp_predict_point)

    return predict_points


def process(options):
    # 根据文件类型加载所有的点
    if options.file_type == 'excel':
        all_points = load_points.load_by_excel(options.input_file, options.excel_sheet_index, options.lon_index,
                                               options.lat_index, options.z_index, options.has_title)
    else:
        all_points = load_points.load_by_csv(options.input_file, options.lon_index, options.lat_index, options.z_index,
                                             options.has_title)

    # 交叉验证
    predict_points = cross_interpolation(all_points, 500)

    for i in range(len(all_points)):
        print('predict point :{} ,   measure point : {}'.format(predict_points[i], all_points[i]))

    measure_zs = np.array(all_points)[..., 2]
    predict_zs = np.array(predict_points)[..., 2]

    print('ME: {}'.format(statistics.me(measure_zs, predict_zs)))
    print('RMSE: {}'.format(mean_squared_error(measure_zs, predict_zs) ** .5))
    print('R2: {}'.format(r2_score(measure_zs, predict_zs)))


if __name__ == '__main__':
    excel_file = '/Users/cakemonster/Desktop/statics/采样点.csv'
    _lon_index = '1'
    _lat_index = '2'
    _z_index = '3'

    # excel
    # _args = ['--input-file', excel_file, '--lon-index', _lon_index, '--lat-index', _lat_index, '--z-index',
    #          _z_index]

    # csv
    _args = ['--input-file', excel_file, '--lon-index', _lon_index, '--lat-index', _lat_index, '--z-index',
             _z_index, '--file-type', 'csv']
    _options = handle_command_line(_args)
    validate_options(_options)
    process(_options)

# 可以测试一个文件的n个浓度
# if __name__ == '__main__':
#     for col_index in range(3, 19):
#         excel_file = '/Users/cakemonster/Desktop/statics/湖北大冶土壤SVOCS.xlsx'
#         _lon_index = '1'
#         _lat_index = '2'
#         _z_index = str(col_index)
#
#         _args = ['--input-file', excel_file, '--lon-index', _lon_index, '--lat-index', _lat_index, '--z-index',
#                  _z_index]
#         _options = handle_command_line(_args)
#         validate_options(_options)
#         print('============== column index: {}  ==================='.format(col_index))
#         process(_options)

# 正确用法
# if __name__ == '__main__':
#     _options = handle_command_line(sys.argv[1:])
#     validate_options(_options)
#     process(_options)
