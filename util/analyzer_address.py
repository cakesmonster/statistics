# coding: utf-8
import xlrd
import csv
import requests
import os
import sys

default_sheet_index = 0


def analyzer_address(address):
    """
    把地址解析成经纬度
    example: restapi.amap.com/v3/geocode/geo?key=febaf013c2fd8d56f380f82b388b4b73&address=边街村柯和厂湾&city=黄石&output=json
    :param address: 地址
    :return: 经纬度
    """
    response = requests.get('http://restapi.amap.com/v3/geocode/geo',
                            params={'key': 'febaf013c2fd8d56f380f82b388b4b73', 'address': address, 'city': '黄石',
                                    'output': 'json'})
    location = ','
    try:
        location = response.json()['geocodes'][0]['location']
    except KeyError as e:
        print('analyzer address : ' + address + '  failed')
    return location


def process_line(row):
    new_row = [row[0].value, row[1].value]
    address = row[2].value
    new_row.append(row[2].value)
    if len(address) != 0 and address != '':
        location = analyzer_address(address)
        splits = location.split(',')
        new_row.append(splits[0])
        new_row.append(splits[1])
    else:
        new_row.append(row[3].value)
        new_row.append(row[4].value)
    return new_row


def process(input_file, output_file, sheet_index):
    if not os.path.exists(input_file):
        sys.exit('file: {} is not exist'.format(input_file))
    work_book = xlrd.open_workbook(input_file)
    sheet = work_book.sheet_by_index(sheet_index)
    new_lines = []
    try:
        for row_number in range(sheet.nrows):
            new_line = process_line(sheet.row(row_number))
            new_lines.append(new_line)
    except Exception:
        sys.exit('load points in file: {} error'.format(input_file))

    with open(output_file, 'w') as f:
        write = csv.writer(f)
        write.writerows(new_lines)


if __name__ == '__main__':
    _input_file = '/Users/cakemonster/Desktop/fit_populations/test.xlsx'
    _output_file = '/Users/cakemonster/Desktop/fit_populations/test_fill.csv'
    process(_input_file, _output_file, default_sheet_index)
