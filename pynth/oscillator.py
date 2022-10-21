from functools import cached_property
from inspect import signature
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np

from .const import SAMPLING_RATE


class Oscillator:
    @cached_property
    def map(self):
        argc = len(signature(self.take).parameters)  # type: ignore
        if argc == 1:
            return self.__map1
        elif argc == 2:
            return self.__map2
        elif argc == 3:
            return self.__map3
        else:
            raise Exception("take 参数数量错误")

    @cached_property
    def __vectorized_take(self):
        return np.vectorize(self.take, cache=True)  # type: ignore

    def __map1(self, p, _, __):
        return self.__vectorized_take(p)

    def __map2(self, p, t, _):
        return self.__vectorized_take(p, t)

    def __map3(self, p, t, d):
        return self.__vectorized_take(p, t, d)

    def plot(self, n=1, dur=1.0):
        s = int(dur * SAMPLING_RATE)
        p = np.tile(np.linspace(0, 1, s // n, endpoint=False), n + 1)[:s]
        t = np.linspace(0, dur, s, endpoint=False)
        d = np.full(s, t[-1])
        data = np.array(self.map(p, t, d))

        if len(data.shape) == 1:
            plt.plot(data)
        else:
            for row in data:
                plt.plot(row)

    def __combine(self, op, other):
        if isinstance(other, Oscillator):
            return OscillatorOpOscillator(self, op, other)
        else:
            return OscillatorOpValue(self, op, other)

    def __add__(self, other):
        return self.__combine(np.add, other)

    def __sub__(self, other):
        return self.__combine(np.subtract, other)

    def __mul__(self, other):
        return self.__combine(np.multiply, other)

    def __pow__(self, other):
        return self.__combine(np.power, other)

    def __truediv__(self, other):
        return self.__combine(np.true_divide, other)

    def __floordiv__(self, other):
        return self.__combine(np.floor_divide, other)

    def __mod__(self, other):
        return self.__combine(np.mod, other)

    def __pos__(self):
        return self

    def __neg__(self):
        return OpOscillator(np.negative, self)

    def __abs__(self):
        return OpOscillator(np.abs, self)


class CombinedOscillator(Oscillator):
    def take(self, p, t, d):
        v = self.map([p], [t], [d]).T[0]
        return tuple(v) if isinstance(v, Iterable) else v


class OpOscillator(CombinedOscillator):
    def __init__(self, op, a):
        self.op = op
        self.a = a

    def map(self, p, t, d):
        return self.op(self.a.map(p, t, d))


class OscillatorOpOscillator(CombinedOscillator):
    def __init__(self, a, op, b):
        self.a = a
        self.op = op
        self.b = b

    def map(self, p, t, d):
        return self.op(self.a.map(p, t, d), self.b.map(p, t, d))


class OscillatorOpValue(CombinedOscillator):
    def __init__(self, a, op, b):
        self.a = a
        self.op = op
        self.b = b

    def map(self, p, t, d):
        return self.op(self.a.map(p, t, d), self.b)


__all__ = ['Oscillator']
