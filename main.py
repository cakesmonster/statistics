import xlrd
import csv
import os
import idw


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


def fit(path, new_dir, points):
    title, fit_points = load_fit_population(path)
    new_fit_points = []
    new_fit_points.extend(title)
    for fit_point in fit_points:
        new_fit_point = []
        new_fit_point.extend(fit_point)
        if fit_point[3] != '' and fit_points[4] != '':
            z = idw.interpolation(float(fit_point[3]), float(fit_point[4]), points)
            new_fit_point.append(z)
        else:
            pass
        new_fit_points.append(new_fit_point)

    filename = os.path.basename(path).split('.')[0]
    new_path = os.path.join(new_dir, filename + '_new.csv')

    write_csv(new_path, new_fit_points)


def write_csv(path, points):
    with open(path, 'w') as f:
        write = csv.writer(f)
        write.writerows(points)


if __name__ == '__main__':

    _dir = '/Users/cakemonster/Desktop/fit_populations/'
    _new_dir = '/Users/cakemonster/Desktop/new_fit_populations/'
    _points = load_all_points()
    for file in os.listdir(_dir):
        if file == '.DS_Store':
            continue
        _file = os.path.join(_dir, file)
        fit(_file, _new_dir, _points)
