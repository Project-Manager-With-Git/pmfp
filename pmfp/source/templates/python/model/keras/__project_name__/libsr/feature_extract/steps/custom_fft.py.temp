"""
傅立叶变换模块
"""
import numpy as np
from scipy.io import wavfile
from scipy.fftpack import fft


def custom_fft(samples, sample_rate):
    """读取出音频整体傅立叶变换各频域的强度

    Parameters:
        samples  (np.ndarray): - 指明音频的振幅序列
        sample_rate  (int): - 指明抽样率

    Returns:
        tuple[np.ndarray,np.ndarray]: - 由频率(一维)和强度(一维)组成的元组
    """
    T = 1.0 / sample_rate
    N = samples.shape[0]
    yf = fft(samples)
    xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
    vals = 2.0 / N * np.abs(yf[0:N // 2])
    return xf, vals


def custom_fft_from_path(record_path):
    """从音频文件读取出音频整体傅立叶变换各频域的强度

    Parameters:
        record_path (Union[pathlib.Path,str]): - 指明音频的路径

    Returns:
        tuple[np.ndarray,np.ndarray]: - 由频率(一维)和强度(一维)组成的元组
    """
    sample_rate, samples = wavfile.read(str(record_path))
    return custom_fft(sample_rate, samples)
