# coding: utf-8
import math
import main
import idw
import csv
import xlrd


def mre(predict_points, measure_points):
    n = len(predict_points)
    _mre = 0.0
    for i in range(n):
        _mre += abs(predict_points[i][2] - measure_points[i][2])
    _mre = _mre / n
    return _mre


def rmse(predict_points, measure_points):
    n = len(predict_points)
    _rmse = 0.0
    for i in range(n):
        _rmse += math.pow(predict_points[i][2] - measure_points[i][2], 2)
    _rmse = _rmse / n
    _rmse = math.sqrt(_rmse)
    return _rmse


def load_all_data(path):
    count = 1
    data = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            if count == 1:
                count += 1
                continue
            new_line = [float(line[1]), float(line[2]), float(line[3])]
            data.append(new_line)
            count += 1
    return data


def load_all_points(col):
    points = []
    work_book = xlrd.open_workbook("/Users/cakemonster/Desktop/删掉异常值第一种excel.xlsx")
    sheet = work_book.sheet_by_index(0)
    for row_number in range(sheet.nrows):
        if row_number == 0:
            continue
        lon = float(sheet.row(row_number)[1].value)
        lat = float(sheet.row(row_number)[2].value)
        concentration = float(sheet.row(row_number)[col].value)
        point = [lon, lat, concentration]
        points.append(point)
    return points


def test():
    # all_points = main.load_all_points()
    all_points = load_all_points(21)
    predict_points = random_validate(all_points)

    for i in range(len(all_points)):
        print('predict z :{} ,   measure z : {}'.format(predict_points[i], all_points[i]))

    print('MRE: {}'.format(mre(predict_points, all_points)))
    print('RMSE: {}'.format(rmse(predict_points, all_points)))


def random_validate(points):
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

        z = idw.interpolation(temp_predict_point[0], temp_predict_point[1], temp_measure_points)
        # print('predict z : {}, measure z :{}'.format(z, temp_predict_point[2]))
        temp_predict_point[2] = z
        all_predict_points.append(temp_predict_point)

    return all_predict_points


if __name__ == '__main__':
    test()
    # load_all_data('/Users/cakemonster/Downloads/tester.csv')
