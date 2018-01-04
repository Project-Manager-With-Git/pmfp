""" 把 wav 数据的值规范化到 0 - 1 之间
"""
import numpy as np


def normalize_wav(wav):
    """ 把 wav 数据的值规范化到 0 - 1 之间

    Args:
        wav (np.ndarray) : - 一维的音频序列
    Returns:
        Numpy array holding the sample data as floats between -1.0 and 1.0.
    """

    wav = wav.astype(np.float32) / np.iinfo(np.int16).max
    return wav
