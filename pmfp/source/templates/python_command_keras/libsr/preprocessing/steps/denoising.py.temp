"""去噪音模块
"""
import numpy as np


def get_main_voice(wav, filter_threshold=0.1, seg_length=800):
    """ 保留主要的音频而去除噪音

    Args:
        wav (np.ndarray)         : - 音频数据序列
        filter_threshold (float) : - 筛选阈值：如果某一段音频的平均值低于最大值乘以这个阈值，我们就认为它是没有声音的
        seg_length (int)         : - 根据多长来切断音频进行筛选，默认长度是 800

    Returns:
        np.ndarray : - wav_with_only_main_voice 只包含主要音的音频数据，长度应该是小于输入的音频长度的
    """

    # Split wav into segements
    splitted_wavs = _split_by_length(wav, seg_length)

    # Compute the avg of all segments
    wavs_mean = []
    for sw in splitted_wavs:
        wavs_mean.append(np.absolute(sw).mean())
    wavs_mean = np.array(wavs_mean)

    # Check if each segments will be kept or not
    # seg_keep_array : [1 0 1 1 0 1 1 1 1 0 0 0 0 0 0 0 0 0 1 0]
    seg_keep_array = (wavs_mean > filter_threshold *
                      wavs_mean.max()).astype(int)

    # Find the longgest keep period
    # [1 0 1 1 0 1 1 1 1 0 0 0 0 0 0 0 0 0 1 0] -> 5, 8 (longest continunous 1)
    wav_length = wav.shape[0]
    num_seg = int(wav_length / seg_length) + 1
    start, end = _get_longest_period(seg_keep_array)
    if start > 1:
        start = (start - 1)
    if end < num_seg - 1:
        end = (end + 1)

    wav_with_only_main_voice = wav[int(
        seg_length * start):int(seg_length * end)]
    return wav_with_only_main_voice


def _split_by_length(wav, seg_length):
    """Split the wav by segment length"""

    wav_length = wav.shape[0]

    indice = 0
    splitted_wavs = []

    while indice + seg_length <= wav_length:
        w = wav[indice: indice + seg_length]
        splitted_wavs.append(w)
        indice += seg_length

    return np.array(splitted_wavs)


def _group_consecutives(vals, step=0):
    """Return list of consecutive lists of numbers from vals (number list)."""
    run = []
    result = [run]
    expect = None
    for v in vals:
        if (v == expect) or (expect is None):
            run.append(v)
        else:
            run = [v]
            result.append(run)
        expect = v + step
    return result


def _get_longest_period(seg_keep_array):
    """获取最长的主干周期"""
    cons_wav = _group_consecutives(seg_keep_array)
    cons_wav_length = [sum(wav) for wav in cons_wav]
    start = 0
    end = 0
    for i in range(cons_wav_length.index(max(cons_wav_length)) + 1):
        if i < cons_wav_length.index(max(cons_wav_length)):
            start += len(cons_wav[i])
        end += len(cons_wav[i])
    return start, end
