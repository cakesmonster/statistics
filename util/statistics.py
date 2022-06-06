# coding: utf-8
import numpy as np


def me(measure_zs, predict_zs):
    return np.mean(np.subtract(measure_zs, predict_zs))
