from scipy.io import wavfile
import python_speech_features


def mfcc(sample_rate, audio, cnn=False, **kwargs):
    """从读出的音频数据中算出mfcc,具体可以看python_speech_features的文档

    Parameters:
        audio (np.ndarray): - 指明音频的振幅序列
        sample_rate (int): - 指明抽样率
        cnn (bool): - 是否为cnnreshape出一个维度,默认为False
        numcep (int): - 指明返回的倒数数量,默认为13

    Returns:
        np.ndarray: - mfcc强度(二维)组成的元组,shape为(times.shape,numcep)
    """
    X_yield = python_speech_features.mfcc(audio, sample_rate, **kwargs)
    if cnn:
        X_yield = X_yield.reshape(tuple(list(X_yield.shape) + [1]))
    return X_yield


def mfcc_from_path(record_path, cnn=False, **kwargs):
    """从音频文件读取出mfcc

    Parameters:
        record_path (Union[pathlib.Path,str]): - 指明音频的路径
        cnn (bool): - 是否为cnnreshape出一个维度,默认为False
        numcep (int): - 指明返回的倒数数量,默认为13

    Returns:
        np.ndarray: - mfcc强度(二维)组成的元组,shape为(times.shape,numcep)
    """
    sample_rate, samples = wavfile.read(str(record_path))
    X_yield = mfcc(samples, sample_rate, **kwargs)
    if cnn:
        X_yield = X_yield.reshape(tuple(list(X_yield.shape) + [1]))
    return X_yield
