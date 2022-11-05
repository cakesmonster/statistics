# coding: utf-8
import sys

import xlrd
import csv
import os


def load_by_excel(path, sheet_index, lon_index, lat_index, z_index, has_title):
    if not os.path.exists(path):
        sys.exit('file: {} is not exist'.format(path))
    points = []
    work_book = xlrd.open_workbook(path)
    sheet = work_book.sheet_by_index(sheet_index)
    try:
        for row_number in range(sheet.nrows):
            if has_title and row_number == 0:
                continue
            lon = float(sheet.row(row_number)[lon_index].value)
            lat = float(sheet.row(row_number)[lat_index].value)
            concentration = float(sheet.row(row_number)[z_index].value)
            point = [lon, lat, concentration]
            points.append(point)
    except Exception:
        sys.exit('load points in file: {} error'.format(path))
    return points


def load_by_csv(path, lon_index, lat_index, z_index, has_title):
    """
    从csv加载所有的点
    :param path: 文件的地址
    :param lon_index: 经度的索引 就是第几列 - 1
    :param lat_index: 纬度的索引
    :param z_index: z的索引
    :param has_title: 有没有标题
    :return: 所有的点
    """
    if not os.path.exists(path):
        sys.exit('file: {} is not exist'.format(path))
    row_number = 0
    points = []
    # 读取文件
    with open(path, 'r') as f:
        reader = csv.reader(f)
        # 遍历每一行
        for line in reader:
            # 判断有标题，并且当前行是第一行，直接跳过
            if has_title and row_number == 0:
                row_number += 1
                continue
            try:
                # 判断经度、纬度、z值的列都不是空的
                if line[lon_index] != '' and line[lat_index] != '' and line[z_index] != '':
                    # 新建一个点，[x, y ,z]
                    new_line = [float(line[lon_index]), float(line[lat_index]), float(line[z_index])]
                    # 放到返回的所有的点的集合里
                    points.append(new_line)
            except Exception as e:
                # sys.exit('load points in file: {} error'.format(path))
                # 如果读取文件当前行有异常情况，直接打印当前行
                print(line)
    # 返回从csv里读到的点 格式就是[x, y ,z]
    return points


def load_need_fill_data(path, sheet_index, lon_index, lat_index, has_title):
    if not os.path.exists(path):
        sys.exit('file: {} is not exist'.format(path))
    points = []
    work_book = xlrd.open_workbook(path)
    sheet = work_book.sheet_by_index(sheet_index)
    try:
        for row_number in range(sheet.nrows):
            if has_title and row_number == 0:
                continue
            lon = float(sheet.row(row_number)[lon_index].value)
            lat = float(sheet.row(row_number)[lat_index].value)
            point = [lon, lat]
            points.append(point)
    except Exception:
        sys.exit('load points in file: {} error'.format(path))
    return points
