"""从路径获取数据,先进行重采样,再将结果用于计算对数频谱,最后padding后返回mfcc数据
"""
from .steps.normalize_wav import normalize_wav
from .steps.desired_samples import desired_samples_wav


def normalize_perprocess(sample_rate, samples,
                         desired_samples=16000):
    """标准化wav数据,预处理顺序为:
    正态化->数据对齐

    Parameters:
        sample_rate (int): - 音频采样率
        samples (np.ndarray): - wav数据
        desired_samples (int): -  要求的采样数目,默认为16000

    Return:
        (int): - 预处理后的采样率sample_rate
        (np.ndarray): - 预处理后的能量数据sample
    """
    samples = normalize_wav(samples)
    samples = desired_samples_wav(samples, desired_samples=desired_samples)
    return sample_rate, samples
