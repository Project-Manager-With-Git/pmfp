"""用于加长或者截断音频数据是数据整齐
"""
import numpy as np


def padding_spec(spec, max_lenght=16000):
    """读取出音频整体傅立叶变换各频域的强度或mfcc等二维的数据.然后在末尾填充0值到最大长度

    Parameters:
        spec (np.ndarray): - 傅立叶变换各频域的强度或mfcc等二维的数据
        max_lenght (int): - 要填充到的最大长度

    Returns:
        np.ndarray: - 返回结果为padding后的频域的强度或mfcc等二维的数据
    """
    if spec.shape[0] >= max_lenght:
        return spec
    result = np.pad(spec, ((0, max_lenght - len(spec)), (0, 0)),
                    mode='constant',
                    constant_values=0)
    return result


def padding_wave(sample, max_lenght=16000):
    """读取出音频整体的波形强度(一维数组),然后在末尾填充0值到最大长度

    Parameters:
        samples (np.ndarray): - 指明音频的振幅序列
        max_lenght (int): - 要填充到的最大长度

    Returns:
        np.ndarray: - 返回结果为padding后的波形强度数据
    """
    if len(sample) >= max_lenght:
        return sample
    result = np.pad(sample, pad_width=(max_lenght - len(sample), 0),
                    mode='constant', constant_values=(0, 0))
    return result


def chop_audio_gen(samples, L=16000, num=20):
    """将大于L值的波形/频谱等数据,分段为最长16000采样的几个.这是用于处理噪音的

    Parameters:
        samples (np.ndarray): - 指明音频的振幅序列
        L (int): - 最大长度
        num (int): - 最大分段个数

    Yield:
        np.ndarray: - 返回结果为chop后的波形强度数据
    """
    for _ in range(num):
        beg = np.random.randint(0, len(samples) - L)
        yield samples[beg: beg + L]
