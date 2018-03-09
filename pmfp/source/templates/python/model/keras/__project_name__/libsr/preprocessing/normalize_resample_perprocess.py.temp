from .steps.resample import resample
from .steps.normalize_wav import normalize_wav
from .steps.desired_samples import desired_samples_wav


def normalize_resample_perprocess(sample_rate, samples, desired_samples=16000, new_sample_rate=8000):
    """预处理顺序为:
    正态化->数据对齐->resample

    Parameters:
        sample_rate (int): - 音频采样率
        samples (np.ndarray): - wav数据
        desired_samples (int): -  要求的采样数目,默认为16000
        new_sample_rate (int): - 重采样的目标采样频率

    yield:
        (np.ndarray): - 若cnn参数为True.则返回的特征(3维),本处为(99, 81, 1),\
        否则返回特征(2维),本处为(99, 81)
    """
    samples = normalize_wav(samples)
    samples = desired_samples_wav(samples, desired_samples=desired_samples)
    new_sample_rate, resampled = resample(
        samples, sample_rate, new_sample_rate=new_sample_rate)

    return new_sample_rate, resampled
