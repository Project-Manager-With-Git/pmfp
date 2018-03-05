"""使wav数据整齐"""
import numpy as np


def desired_samples_wav(wav, desired_samples=16000):
    """ 如果wav数据没有采样足够,则用0值补齐否则随机的在 wav 数据里面挑选一段足够采样的连续完整wav出来

    Args:
        wav (np.ndarray) : - 一维的音频序列
        desired_samples (int) : - 要求的采样数目,默认为16000

    Returns:
        np.dnarray: -长度与desired_samples值一致的wav一维数组
    """
    wav_length = wav.shape[0]
    if wav_length < desired_samples:
        # Pad 0 at the end
        desired_wav = np.lib.pad(
            wav, (0, desired_samples - wav_length), mode='constant')
    elif wav_length > desired_samples:
        # Random choose a range from the data
        start = np.random.randint(0, wav_length - desired_samples)
        desired_wav = wav[start:start + desired_samples]
    else:
        desired_wav = wav
    return desired_wav


# if __name__=='__main__':

#     from scipy.io import wavfile
#     from pathlib  import Path

#     DEFAULT_DATASET_PATH = Path(__file__).absolute(
#         ).parent.parent.parent.parent.parent.joinpath('dataset')

#     wav_filepath = DEFAULT_DATASET_PATH.joinpath('train',
#         'audio', 'bed', '0a7c2a8d_nohash_0.wav')
#     _, wav = wavfile.read(str(wav_filepath))

#     # Change wav length to 13000, so now the wav is not the length we need
#     wav = wav[:13000]
#     # Use this function to preprocess it to desired length
#     desired_wav = desired_samples_wav(wav)

#     print('')
#     print('------------------- Test 1: pad 0 for short wav ---------------------')
#     print('')
#     print('Original wav length:', wav.shape[0],
#           'after preprocessing, desired length:', desired_wav.shape[0])

#     # Pad wav to make it longer than 16000
#     wav = np.lib.pad(wav, (0, 4000), mode='constant')
#     # Use this function to preprocess it to desired length
#     desired_wav = desired_samples_wav(wav)

#     print('')
#     print('-------------- Test 2: random choose range for long wav -------------')
#     print('')
#     print('Original wav length:', wav.shape[0],
#           'after preprocessing, desired length:', desired_wav.shape[0])
#     print('')
