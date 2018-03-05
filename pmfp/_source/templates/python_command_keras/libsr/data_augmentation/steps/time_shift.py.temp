""" 在时间维度上对 wav 数据进行随机的平移，并将空的位置填为 0
"""
import numpy as np


def shift_and_pad_zeros(wav, time_shift=2000):
    """ 在时间维度上对 wav 数据进行随机的平移

    对给定的 wav 时序数据，随机的向左或向右平移一个单位，平移的最大值为 time_shift

    Args:
        wav (np.ndarray): - 一维的 wav 时序数据
        time_shift (int): - 时间平移量的最大值

    Returns:
        shifted_wav: 随机平移后的 wav 时序数据，shape 和 input wav 相同
    """

    wav_length = wav.shape[0]

    if time_shift > 0:
        time_shift_amount = np.random.randint(-time_shift, time_shift)
    else:
        time_shift_amount = 0

    if time_shift_amount > 0:
        # 向右 padding time_shift_amount 个 0
        # 取后面部分
        shifted_wav = np.lib.pad(wav, (0, time_shift_amount), mode='constant')
        return shifted_wav[time_shift_amount:]
    else:
        # 向左 padding time_shift_amount 个 0
        # 取前面部分
        shifted_wav = np.lib.pad(wav, (-time_shift_amount, 0), mode='constant')
        return shifted_wav[:wav_length]
