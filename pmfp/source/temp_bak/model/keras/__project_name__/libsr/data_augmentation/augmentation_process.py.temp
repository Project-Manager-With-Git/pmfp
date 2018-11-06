from .steps.mix_noise import mix_background_noise
from .steps.time_shift import shift_and_pad_zeros
from .steps.silence_as_zero import silence_as_zero


def aug_process(wav, label, mode,
                time_shift=2000,
                background_volume_range=0.1,
                background_frequency=0.1):
    if mode in ('train',):
        wav = silence_as_zero(wav, label)
        wav = shift_and_pad_zeros(wav, time_shift=time_shift)
        wav = mix_background_noise(
            wav,
            background_volume_range=background_volume_range,
            background_frequency=background_frequency)
        return wav
    elif mode in ('validation',):
        wav = mix_background_noise(
            wav,
            background_volume_range=background_volume_range,
            background_frequency=background_frequency)
        return wav
    else:
        return wav
