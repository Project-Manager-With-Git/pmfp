"""
正态化数据
"""
import numpy as np


def normalization_local(spectrogram):
    """用于正态化频谱中的强度,注意本步正态化是单条音频正态化,不是全局

    Parameters:
        spectrogram (np.ndarray): - 指明音频的频谱数据或者其他类似的东西,比如mfcc(二维)

    Returns:
        np.ndarray: - 正态化的音频频谱数据
    """
    mean = np.mean(spectrogram, axis=0)
    std = np.std(spectrogram, axis=0)
    norm_spectrogram = (spectrogram - mean) / std
    return norm_spectrogram


def normalization_global(spectrograms):
    """用于正态化频谱中的强度,注意本步正态化是全局的

    Parameters:
        spectrograms (np.ndarray): - 指明音频的频谱数据集或者其他类似的东西,比如mfcc(3维,第一维是样本数量)

    Returns:
        np.ndarray: - 正态化的音频频谱数据
    """
    mean = np.mean(spectrograms.reshape(
        spectrograms.shape[0] * spectrograms.shape[1], spectrograms.shape[2]),
        axis=0)
    std = np.std(spectrograms.reshape(
        spectrograms.shape[0] * spectrograms.shape[1], spectrograms.shape[2]),
        axis=0)
    norm_spectrograms = (spectrograms - mean) / std
    return norm_spectrograms
