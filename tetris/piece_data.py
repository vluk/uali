import numpy as np
import math

"""from tetrio.js"""

kicks = {
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

"""converted from tetrio i kick table using TTC implementation offsets"""
"""read: https://harddrop.com/wiki/SRS#How_Guideline_SRS_Really_Works"""

i_kicks = {
    "01": [[1, 0], [2, 0], [-1, 0], [-1, 1], [2, -2]],
    "10": [[-1, 0], [-2, 0], [1, 0], [-2, 2], [1, -1]],
    "12": [[0, -1], [-1, -1], [2, -1], [-1, -3], [2, 0]],
    "21": [[0, 1], [-2, 1], [1, 1], [-2, 0], [1, 3]],
    "23": [[-1, 0], [1, 0], [-2, 0], [1, -1], [-2, 2]],
    "32": [[1, 0], [2, 0], [-1, 0], [2, -2], [-1, 1]],
    "30": [[0, 1], [1, 1], [-2, 1], [1, 3], [-2, 0]],
    "03": [[0, -1], [-1, -1], [2, -1], [2, 0], [-1, -3]],
    "02": [[1, -1], [1, -2]],
    "13": [[-1, -1], [0, -1]],
    "20": [[-1, 1], [-1, 2]],
    "31": [[1, 1], [0, 1]]
}

o_kicks = {
    "01": [0, 1],
    "02": [1, 1],
    "03": [1, 0],
    "10": [0, -1],
    "12": [1, 0],
    "13": [1, -1],
    "20": [-1, -1],
    "21": [-1, 0],
    "23": [0, -1],
    "30": [-1, 0],
    "31": [-1, 1],
    "32": [0, 1]
}

# please let me know if you know how this works, because i certainly don't
def to_kernal(kicks):
    A = np.zeros((7, 7))
    p = 1
    for kick in kicks:
        A[kick[0] + 3][kick[1] + 3] = p
        p *= 2
    return A

kernals = {i: to_kernal(kicks[i]) for i in kicks}
i_kernals = {i: to_kernal(i_kicks[i]) for i in i_kicks}
o_kernals = {i: to_kernal(o_kicks[i]) for i in o_kicks}

minos = ["z", "l", "o", "s", "i", "j", "t"]

pieces = {
    "i": np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 1, 1, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], dtype=np.float32),
    "j": np.array([[1, 0, 0], [1, 1, 1], [0, 0, 0]], dtype=np.float32),
    "l": np.array([[0, 0, 1], [1, 1, 1], [0, 0, 0]], dtype=np.float32),
    "o": np.array([[0, 1, 1], [0, 1, 1], [0, 0, 0]], dtype=np.float32),
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
