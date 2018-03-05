"""重采样模块
"""
from scipy.io import wavfile
from scipy import signal


def resample(samples, sample_rate, *, new_sample_rate=8000):
    """读取出音频整体傅立叶变换各频域的强度

    Parameters:
        samples  (np.ndarray): - 指明音频的振幅序列
        sample_rate  (int): - 指明抽样率
        new_sample_rate (int): - 指明重采样率

    Returns:
        tuple[np.ndarray,np.ndarray]: - 返回结果为重采样后的由频率(一维)和强度(一维)组成的元组
    """
    # int(new_sample_rate / sample_rate * samples.shape[0])
    resampled = signal.resample(
        samples,
        int(new_sample_rate / sample_rate * samples.shape[0]))
    return new_sample_rate, resampled


def resample_from_path(record_path, *, new_sample_rate=8000):
    """读取出音频整体傅立叶变换各频域的强度

    Parameters:
        record_path (Union[pathlib.Path,str]): - 指明音频的路径
        new_sample_rate (int): - 指明重采样率

    Returns:
        tuple[np.ndarray,np.ndarray]: - 返回结果为重采样后的由频率(一维)和强度(一维)组成的元组
    """
    sample_rate, samples = wavfile.read(str(record_path))

    return resample(sample_rate, samples, new_sample_rate=new_sample_rate)
