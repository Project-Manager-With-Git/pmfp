"""将silence的数据volumn设为0
"""
import numpy as np


def silence_as_zero(wav, label):

    if label == 'silence':
        # If silence, set all volumn as 0
        volume_scale = 0
    else:
        volume_scale = 1

    return np.multiply(wav, volume_scale)
