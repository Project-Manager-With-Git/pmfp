"""计算对数频谱的模块
"""
import numpy as np
from scipy import signal
from scipy.io import wavfile


def log_specgram(sample_rate, audio, cnn=False, *, window='hann', window_size=20,
                 step_size=10, eps=1e-10):
    """从读出的音频数据中算出对数频谱数据

    Parameters:
        audio (np.ndarray): - 指明音频的振幅序列
        sample_rate (int): - 指明抽样率
        cnn (bool): - 是否为cnnreshape出一个维度,默认为False
        window (str): - 指明分窗的算法,可选的详情可以看scipy.signal.get_window的文档
        window_size (Union[pathlib.Path,str]): - 指明音频的分窗大小
        step_size (Union[pathlib.Path,str]): - 指明步进长度
        eps (float): - 指明频谱强度取对数时的最小值,防止输入为0后得到负无穷

    Returns:
        np.ndarray: - 频谱强度(二维)
    """
    nperseg = int(round(window_size * sample_rate / 1e3))
    noverlap = int(round(step_size * sample_rate / 1e3))
    freqs, times, spec = signal.spectrogram(audio,
                                            fs=sample_rate,
                                            window=window,
                                            nperseg=nperseg,
                                            noverlap=noverlap,
                                            detrend=False)
    X_yield = np.log(spec.T.astype(np.float32) + eps)
    if cnn:
        X_yield = X_yield.reshape(tuple(list(X_yield.shape) + [1]))
    return X_yield


def log_specgram_from_path(record_path, cnn=False, *, window='hann', window_size=20,
                           step_size=10, eps=1e-10):
    """从音频文件读取出对数频谱数据

    Parameters:
        record_path (Union[pathlib.Path,str]): - 指明音频的路径
        cnn (bool): - 是否为cnnreshape出一个维度,默认为False
        window (str): - 指明分窗的算法,可选的详情可以看scipy.signal.get_window的文档
        window_size (Union[pathlib.Path,str]): - 指明音频的分窗大小
        step_size (Union[pathlib.Path,str]): - 指明步进长度
        eps (float): - 指明频谱强度取对数时的最小值,防止输入为0后得到负无穷

    Returns:
        np.ndarray: - 频谱强度(二维)
    """
    sample_rate, samples = wavfile.read(str(record_path))
    freqs, times, log_spec = log_specgram(samples, sample_rate,
                                          window=window,
                                          window_size=window_size,
                                          step_size=step_size, eps=eps)
    X_yield = np.log(spec.T.astype(np.float32) + eps)
    if cnn:
        X_yield = X_yield.reshape(tuple(list(X_yield.shape) + [1]))
    return X_yield
