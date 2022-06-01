# coding: utf-8
import xlrd
import xlwt
import requests


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


def handle_fit_population():
    work_book = xlrd.open_workbook("/Users/cakemonster/Downloads/需要拟合的人群.xls")
    sheet_names = work_book.sheet_names()
    for sheet_name in sheet_names:
        new_rows = []
        sheet = work_book.sheet_by_name(sheet_name)
        for i in range(sheet.nrows):
            new_row = handle_each_row(sheet.row(i))
            new_rows.append(new_row)
        new_file_name = '/Users/cakemonster/Downloads/' + sheet_name + '.xls'
        write_new_sheet(new_file_name, sheet_name, new_rows)


def handle_each_row(row):
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


def write_new_sheet(new_excel, sheet_name, rows):
    index = len(rows)
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(sheet_name)
    for i in range(0, index):
        for j in range(0, len(rows[i])):
            sheet.write(i, j, rows[i][j])
    workbook.save(new_excel)  # 保存工作簿


if __name__ == '__main__':
    handle_fit_population()
