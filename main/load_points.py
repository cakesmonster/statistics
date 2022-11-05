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
    if not os.path.exists(path):
        sys.exit('file: {} is not exist'.format(path))
    row_number = 0
    points = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            if has_title and row_number == 0:
                row_number += 1
                continue
            try:
                if line[lon_index] != '' and line[lat_index] != '' and line[z_index] != '':
                    new_line = [float(line[lon_index]), float(line[lat_index]), float(line[z_index])]
                    points.append(new_line)
            except Exception as e:
                # sys.exit('load points in file: {} error'.format(path))
                print(line)
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
