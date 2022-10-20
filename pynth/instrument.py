import IPython.display as ipd
import matplotlib.pylab as plt
import numpy as np

from .const import SAMPLING_RATE
from .oscillator import Oscillator


class Instrument:
    def __init__(self, wav, amp=1, freq=1, fx=None, sr=SAMPLING_RATE):
        self.wav = wav
        self.amp = amp
        self.freq = freq
        self.fx = fx
        self.sr = sr

    def produce(self, freq, dur):
        n = int(dur * self.sr)
        p = np.linspace(0, 1, n, endpoint=False)
        t = np.linspace(0, dur, n, endpoint=False)
        d = np.full(n, t[-1])
        f = self.__carrier(self.freq, p, t, d, n) * freq
        a = self.__carrier(self.amp, p, t, d, n)

        data = self.wav.map(np.modf(t * f)[0], t, d)
        return (self.fx.apply(data) if self.fx else data) * a

    def plot(self, freq=1, dur=2):
        data = self.produce(freq, dur)

        if len(data.shape) == 1:
            plt.plot(data)
        else:
            for row in data:
                plt.plot(row)

    def audio(self, freq=440, dur=2, autoplay=False, normalize=False):
        data = self.produce(freq, dur)
        return ipd.Audio(
            data if len(data) != 0 else [0],
            rate=self.sr,
            autoplay=autoplay,
            normalize=normalize
        )

    def __carrier(self, obj, p, t, d, n):
        if isinstance(obj, Oscillator):
            return obj.map(p, t, d)
        else:
            return np.full(n, obj)


__all__ = ['Instrument']
