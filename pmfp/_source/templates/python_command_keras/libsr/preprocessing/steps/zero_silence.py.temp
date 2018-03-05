""" 将 silence 全部设置为 0 """
import numpy as np


def silence_as_zero(wav, label):
    """ 将 silence 全部设置为 0

    Args:
        wav (np.ndarray) : - 音频数据序列
        label (str)      : - 音频对应的 label
    """
    if label == 'silence':
        # If silence, set all volume as 0
        volume_scale = 0
    else:
        volume_scale = 1
    return np.multiply(wav, volume_scale)
