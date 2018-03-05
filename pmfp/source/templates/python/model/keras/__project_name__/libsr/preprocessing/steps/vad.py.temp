"""去沉默模块
"""

import numpy as np


def remove_muted(wav, muted_rate=0.05):
    """ 去除两端的沉默部分

    Parameters:
        wav (np.ndarray): - 用于去沉默的目标振幅序列
        muted_rate (float): - 定义为沉默的阈值,小于等于它则为沉默部分

    Returns:
        np.ndarray: - 去掉两端沉默部分的振幅序列
    """
    max_voice = wav.max()
    threshold = max_voice * muted_rate
    keep_wav = np.array(np.absolute(wav) > threshold)
    reverse_keep_wav = np.flip(keep_wav, 0)
    start = list(keep_wav).index(True)
    end = wav.size - list(reverse_keep_wav).index(True)
    return wav[start:end]
