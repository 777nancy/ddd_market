import numpy as np
import pandas as pd


def intersection(a, b):
    """
    配列a, bの交点のインデックスを求める
    :param a:配列
    :param b:配列
    :return:
    """

    min_length = min(len(a), len(b))
    diff_sign_array = np.sign(a[len(a) - min_length :] - b[len(b) - min_length :])
    if not len(diff_sign_array):
        return np.array([]), np.array([])
    if type(diff_sign_array) is pd.Series:
        diff_sign_array = diff_sign_array.reset_index(drop=True)
    up_index = []
    down_index = []
    for i in range(1, len(diff_sign_array)):
        if (diff_sign_array[i - 1] == 1) and (diff_sign_array[i] in [0, -1]):
            up_index.append(i)
        elif (diff_sign_array[i - 1] == -1) and (diff_sign_array[i] in [0, 1]):
            down_index.append(i)

    return np.array(up_index), np.array(down_index)


def intersection_with_bounds(a, b, upper_bound, lower_bound):
    """
    配列a, bの交点のインデックスを求める
    :param a:配列
    :param b:配列
    :param upper_bound:上限
    :param lower_bound:下限
    :return:
    """
    print(a, b)
    min_length = min(len(a), len(b))
    diff_sign_array = np.sign(a[len(a) - min_length :] - b[len(b) - min_length :])
    if not len(diff_sign_array):
        return np.array([]), np.array([])
    if type(diff_sign_array) is pd.Series:
        diff_sign_array = diff_sign_array.reset_index(drop=True)
    up_index = []
    down_index = []
    for i in range(1, len(diff_sign_array)):
        if (diff_sign_array[i - 1] == 1) and (diff_sign_array[i] in [0, -1]):
            if (a[len(a) - min_length :][i - 1] < lower_bound) and (b[len(b) - min_length :][i - 1] < lower_bound):
                up_index.append(i)
        elif (diff_sign_array[i - 1] == -1) and (diff_sign_array[i] in [0, 1]):
            if a[len(a) - min_length :][i - 1] > upper_bound and b[len(b) - min_length :][i - 1] > upper_bound:
                down_index.append(i)

    return np.array(up_index), np.array(down_index)
