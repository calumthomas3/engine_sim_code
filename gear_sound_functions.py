import random


def compress_signal(sample, count):
    indexed = [item for item in enumerate(sample)]
    random.shuffle(indexed)
    trimmed = indexed[:count]
    trimmed.sort()
    return [item for index, item in trimmed]


#  Chunking function
def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


# Resampling function
def resample(arr, newlength):
    chunksize = len(arr)/newlength
    return [np.mean(chunk) for chunk in chunks(arr, chunksize)]
