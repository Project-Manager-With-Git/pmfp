import numpy
from scipy.fftpack import dct
from scipy.io import wavfile

sampleRate, signal = wavfile.read("file.wav")
numCoefficients = 13  # choose the sive of mfcc array
minHz = 0
maxHz = 22.000

complexSpectrum = numpy.fft(signal)
powerSpectrum = abs(complexSpectrum) ** 2
filteredSpectrum = numpy.dot(powerSpectrum, melFilterBank())
logSpectrum = numpy.log(filteredSpectrum)
dctSpectrum = dct(logSpectrum, type=2)  # MFCC :)


def melFilterBank(blockSize):
    numBands = int(numCoefficients)
    maxMel = int(freqToMel(maxHz))
    minMel = int(freqToMel(minHz))

    # Create a matrix for triangular filters, one row per filter
    filterMatrix = numpy.zeros((numBands, blockSize))

    melRange = numpy.array(xrange(numBands + 2))

    melCenterFilters = melRange * (maxMel - minMel) / (numBands + 1) + minMel

    # each array index represent the center of each triangular filter
    aux = numpy.log(1 + 1000.0 / 700.0) / 1000.0
    aux = (numpy.exp(melCenterFilters * aux) - 1) / 22050
    aux = 0.5 + 700 * blockSize * aux
    aux = numpy.floor(aux)  # Arredonda pra baixo
    centerIndex = numpy.array(aux, int)  # Get int values

    for i in xrange(numBands):
        start, centre, end = centerIndex[i:i + 3]
        k1 = numpy.float32(centre - start)
        k2 = numpy.float32(end - centre)
        up = (numpy.array(xrange(start, centre)) - start) / k1
        down = (end - numpy.array(xrange(centre, end))) / k2

        filterMatrix[i][start:centre] = up
        filterMatrix[i][centre:end] = down

    return filterMatrix.transpose()


def freqToMel(freq):
    return 1127.01048 * math.log(1 + freq / 700.0)


def melToFreq(mel):
    return 700 * (math.exp(mel / 1127.01048) - 1)
