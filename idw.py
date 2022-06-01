# coding: utf-8
import math


def interpolation(lon, lat, points):
    """
    idw
    :param lon: 未知点经纬度
    :param lat: 未知点经纬度
    :param points: 所有点
    :return: Z
    """
    point_zero = [lon, lat]
    p = -1
    result = 0.0
    _denominator = denominator(point_zero, points, p)
    lambda_sum = 0.0
    for point in points:
        molecular = math.pow(distance(point, point_zero), p)
        lambda_i = molecular / _denominator
        lambda_sum += lambda_i
        result += (lambda_i * point[2])
    return result


def denominator(point_zero, points, p):
    """
    求lambda的分母，就是未知点到其它点的距离的-p次方相加
    :param point_zero: 未知点
    :param points: 所有点
    :param p: p
    :return: 分母
    """
    # 分母
    result = 0.0
    # 遍历获取该点距离所有采样点的距离
    for point in points:
        if point_zero[0] == point[0] and point_zero[1] == point[1]:
            continue
        dis = distance(point_zero, point)
        result += math.pow(dis, p)
    return result


def distance(p, pi):
    """
    计算两点之间距离
    :param p:
    :param pi:
    :return:
    """
    dis = (p[0] - pi[0]) * (p[0] - pi[0]) + (p[1] - pi[1]) * (p[1] - pi[1])
    result = math.sqrt(dis)
    return result


if __name__ == '__main__':
    all_points = [[70.0, 140.0, 115.4], [115.0, 115.0, 123.1], [150.0, 150.0, 113.8], [110.0, 170.0, 110.5],
                  [90.0, 190.0, 107.2], [180.0, 210.0, 131.78]]

    print(interpolation(110.0, 150.0, all_points))
