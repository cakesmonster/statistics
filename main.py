import xlrd
import csv
import os
from main import idw
from main import load_points


def load_all_points():
    points = []
    work_book = xlrd.open_workbook("/Users/cakemonster/Downloads/采样POINT.xls")
    sheet = work_book.sheet_by_index(0)
    for row_number in range(sheet.nrows):
        if row_number == 0:
            continue
        lon = float(sheet.row(row_number)[1].value)
        lat = float(sheet.row(row_number)[2].value)
        concentration = float(sheet.row(row_number)[19].value)
        point = [lon, lat, concentration]
        points.append(point)
    return points


def load_fit_population(path):
    work_book = xlrd.open_workbook(path)
    sheet = work_book.sheet_by_index(0)

    title = []
    fit_points = []
    for row_number in range(sheet.nrows):
        # 前两行是标题直接放title的列表里
        if row_number == 0 or row_number == 1:
            title.append(sheet.row(row_number))
            continue
        number = sheet.row(row_number)[0].value
        name = sheet.row(row_number)[1].value
        address = sheet.row(row_number)[2].value
        lon = sheet.row(row_number)[3].value
        lat = sheet.row(row_number)[4].value
        fit_point = [number, name, address, lon, lat]
        fit_points.append(fit_point)
    return title, fit_points


def load_fit_population1(path):
    work_book = xlrd.open_workbook(path)
    sheet = work_book.sheet_by_index(0)

    title = []
    fit_points = []
    for row_number in range(sheet.nrows):
        # 前两行是标题直接放title的列表里
        if row_number == 0:
            title.append(sheet.row(row_number))
            continue
        name = sheet.row(row_number)[0].value
        address = sheet.row(row_number)[1].value
        lon = sheet.row(row_number)[2].value
        lat = sheet.row(row_number)[3].value
        fit_point = [name, address, lon, lat]
        fit_points.append(fit_point)
    return title, fit_points


def fit(points, fit_points):
    new_fit_points = []
    for fit_point in fit_points:
        new_fit_point = []
        new_fit_point.extend(fit_point)
        if fit_point[2] != '' and fit_points[3] != '':
            z = idw.interpolation(float(fit_point[2]), float(fit_point[3]), points, len(points))
            new_fit_point.append(z)
        else:
            new_fit_point.append('')
        new_fit_points.append(new_fit_point)

    # filename = os.path.basename(path).split('.')[0]
    # new_path = os.path.join(new_dir, filename + '_new.csv')
    #
    # write_csv(new_path, new_fit_points)
    return new_fit_points


def write_csv(path, points):
    with open(path, 'w') as f:
        write = csv.writer(f)
        write.writerows(points)


if __name__ == '__main__':
    _dir = '/Users/cakemonster/Desktop/fit/'
    _new_dir = '/Users/cakemonster/Desktop/new_fit/'

    title, fit_points = load_fit_population1('/Users/cakemonster/Desktop/fit/fillpeople(1).xlsx')
    for i in range(3, 19):
        _points = load_points.load_by_csv('/Users/cakemonster/Desktop/statics/采样点.csv', 1, 2, i, True)
        fit_points = fit(_points, fit_points)
        if i == 18:
            write_csv('/Users/cakemonster/Desktop/new_fit/result.csv', fit_points)
