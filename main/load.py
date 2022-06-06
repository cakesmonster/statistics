# coding: utf-8
import xlrd
import csv
import os


def load_by_excel(path, sheet_index, lon_index, lat_index, z_index, has_title):
    points = []
    work_book = xlrd.open_workbook(path)
    sheet = work_book.sheet_by_index(sheet_index)
    for row_number in range(sheet.nrows):
        if has_title and row_number == 0:
            continue
        lon = float(sheet.row(row_number)[lon_index].value)
        lat = float(sheet.row(row_number)[lat_index].value)
        concentration = float(sheet.row(row_number)[z_index].value)
        point = [lon, lat, concentration]
        points.append(point)
    return points


def load_by_csv(path, lon_index, lat_index, z_index, has_title):
    row_number = 0
    points = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            if has_title and row_number == 0:
                row_number += 1
                continue
            new_line = [float(line[lon_index]), float(line[lat_index]), float(line[z_index])]
            points.append(new_line)
    return points
