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
    """
    加载需要拟合的文件
    :param path:  文件的路径
    :return: 需要拟合的点
    """
    # 使用excel读取文件
    work_book = xlrd.open_workbook(path)
    # 获取excel的第一个sheet
    sheet = work_book.sheet_by_index(0)

    title = []
    fit_points = []
    # 遍历第一个sheet里的所有行
    for row_number in range(sheet.nrows):
        # 前两行是标题直接放title的列表里
        if row_number == 0:
            title.append(sheet.row(row_number))
            continue
        # 第一列是姓名
        name = sheet.row(row_number)[0].value
        # 第二列是地址
        address = sheet.row(row_number)[1].value
        # 第三列是经度
        lon = sheet.row(row_number)[2].value
        # 第四列是纬度
        lat = sheet.row(row_number)[3].value
        # 构建一个点
        fit_point = [name, address, lon, lat]
        fit_points.append(fit_point)
    return title, fit_points


def fit(points, fit_points):
    """
    拟合
    :param points: 所有的点
    :param fit_points: 需要拟合的点
    :return:
    """
    new_fit_points = []
    # 遍历需要拟合的点
    for fit_point in fit_points:
        new_fit_point = []
        new_fit_point.extend(fit_point)
        # 判断需要拟合的点的第三列和第四列不为空，也就是经纬度不为空
        if fit_point[2] != '' and fit_points[3] != '':
            # 调用idw方法进行差值
            z = idw.interpolation(float(fit_point[2]), float(fit_point[3]), points, len(points))
            # 新的点的数据就是长这样： [name, address, x , y, z]
            new_fit_point.append(z)
        else:
            # 如果经纬度有一个是空的，就不计算z值，直接插入一个空字符串
            new_fit_point.append('')
        new_fit_points.append(new_fit_point)

    # filename = os.path.basename(path).split('.')[0]
    # new_path = os.path.join(new_dir, filename + '_new.csv')
    #
    # write_csv(new_path, new_fit_points)
    # 返回所有拟合后的点
    return new_fit_points


def write_csv(path, points):
    with open(path, 'w') as f:
        write = csv.writer(f)
        write.writerows(points)


if __name__ == '__main__':
    # _dir = '/Users/cakemonster/Desktop/fit/'
    # _new_dir = '/Users/cakemonster/Desktop/new_fit/'
    # 获取需要拟合的点，文件格式是第一列是姓名，第二列是地址，第三列是经度、第四列是纬度
    # 已经写死了第三列、第四列必须是经纬度，所以如果你自己需要计算别的点的话就需要把经纬度放到第三列和第四列
    title, fit_points = load_fit_population1('/Users/cakemonster/Desktop/fillpeople.xlsx')
    # 遍历第四列到第20列
    for i in range(3, 21):
        # 加载采样点里的第i列的[x, y ,z]的所有的点
        _points = load_points.load_by_csv('/Users/cakemonster/Desktop/sample.csv', 1, 2, i, True)
        # 拟合需要拟合的点
        fit_points = fit(_points, fit_points)
        if i == 20:
            write_csv('/Users/cakemonster/Desktop/new_fit/result.csv', fit_points)
