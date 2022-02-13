import numpy as np
import math

"""from tetrio.js"""

kick_data = {
    "01": [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]],
    "10": [[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]],
    "12": [[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]],
    "21": [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]],
    "23": [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]],
    "32": [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]],
    "30": [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]],
    "03": [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]],
    "02": [[0, 0], [0, -1], [1, -1], [-1, -1], [1, 0], [-1, 0]],
    "13": [[0, 0], [1, 0], [1, -2], [1, -1], [0, -2], [0, -1]],
    "20": [[0, 0], [0, 1], [-1, 1], [1, 1], [-1, 0], [1, 0]],
    "31": [[0, 0], [-1, 0], [-1, -2], [-1, -1], [0, -2], [0, -1]]
}

def to_kernal(kicks):
    A = np.zeros((5, 5))
    p = 1
    for kick in kicks:
        A[kick[0] + 2][kick[1] + 2] = p
        p *= 2
    return A

kick_kernals = {i : to_kernal(kick_data[i]) for i in kick_data}

i_kicks = {
    "01": [[0, 0], [1, 0], [-2, 0], [-2, 1], [1, -2]],
    "10": [[0, 0], [-1, 0], [2, 0], [-1, 2], [2, -1]],
    "12": [[0, 0], [-1, 0], [2, 0], [-1, -2], [2, 1]],
    "21": [[0, 0], [-2, 0], [1, 0], [-2, -1], [1, 2]],
    "23": [[0, 0], [2, 0], [-1, 0], [2, -1], [-1, 2]],
    "32": [[0, 0], [1, 0], [-2, 0], [1, -2], [-2, 1]],
    "30": [[0, 0], [1, 0], [-2, 0], [1, 2], [-2, -1]],
    "03": [[0, 0], [-1, 0], [2, 0], [2, 1], [-1, -2]],
    "02": [[0, 0], [0, -1]],
    "13": [[0, 0], [1, 0]],
    "20": [[0, 0], [0, 1]],
    "31": [[0, 0], [-1, 0]]
}

minos = ["z", "l", "o", "s", "i", "j", "t"]

# i'd like to use the actual ttc implementation of srs kicks but it doesn't work with 180 spins
# its quite nice, but you can't modify it easily
# the "pure rotation" of pieces is far easier to work with, but oh well

pieces = {
    "i": np.array([[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]], dtype=np.float32),
    "j": np.array([[1, 0, 0], [1, 1, 1], [0, 0, 0]], dtype=np.float32),
    "l": np.array([[0, 0, 1], [1, 1, 1], [0, 0, 0]], dtype=np.float32),
    "o": np.array([[1, 1], [1, 1]], dtype=np.float32),
    "s": np.array([[0, 1, 1], [1, 1, 0], [0, 0, 0]], dtype=np.float32),
    "t": np.array([[0, 1, 0], [1, 1, 1], [0, 0, 0]], dtype=np.float32),
    "z": np.array([[1, 1, 0], [0, 1, 1], [0, 0, 0]], dtype=np.float32)
}

def attack(lines, tspin, mini, b2b, combo):
    """calculates attack, not counting all-clear bonus"""
    base = 0
    if tspin:
        base = lines * 2
    elif mini:
        base = lines // 2
    elif lines == 4:
        base = 4
    else:
        base = lines - 1

    r = base

    if b2b:
        r += int(np.log(b2b)) + 1

    if combo:
        r *= 1 + 0.25 * combo
    if base == 0 and combo > 2:
        r = np.log(combo * 1.26)
        print(r)
    return int(r)

rots = {mino: [np.rot90(pieces[mino], i, axes=(1, 0))
               for i in range(4)] for mino in minos}

class RNG():
    def __init__(self, seed):

        self._seed = seed % 2147483647

        if (self._seed <= 0):
            self._seed += 2147483646

    def next(self):
        self._seed = self._seed * 16807 % 2147483647
        return self._seed

    def nextFloat(self):
        return (self.next() - 1) / 2147483646

    def shuffleArray(self, array):
        i = len(array)

        if (i == 0):
            return array

        for i in reversed(range(i)):
            j = math.floor(self.nextFloat() * (i + 1))
            array[i], array[j] = array[j], array[i]
        return array

    def getCurrentSeed(self):
        return self._seed

