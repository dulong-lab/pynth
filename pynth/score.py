import IPython.display as ipd
import numpy as np

from .audio_compiler import AudioCompiler
from .const import SAMPLING_RATE
from .tempo import Tempo
from .instrument import Instrument
from .tools import normalize


class Score:
    class Mixer:
        def mix(self, tracks):
            return normalize(sum(tracks.values()))

    def __init__(self, tempo, parts, title=None, composer=None, mixer=Mixer(), sr=SAMPLING_RATE) -> None:
        self.title = title
        self.composer = composer
        self.mixer = mixer
        self.sr = sr
        self.parts = parts
        self.tempo = Tempo.create(tempo)
        self.instruments = {part: Instrument(None, sr=sr) for part in parts}
        self.symbols = {part: [] for part in parts}

    def audio(self, autoplay=False, normalize=False):
        data = self.build()
        return ipd.Audio(
            data if len(data) != 0 else [0],  # type: ignore
            rate=self.sr,
            autoplay=autoplay,
            normalize=normalize
        )

    def compile(self):
        return {
            part: AudioCompiler().compile(
                self.instruments[part],
                self.tempo,
                self.symbols[part]
            )
            for part in self.parts
        }

    def build(self):
        return self.mixer.mix(self.__pad(self.__normalize(self.compile())))

    def __pad(self, tracks):
        width = max(map(lambda a: a.shape[-1], tracks.values()))
        return {
            part: self.__pad_to_width(data, width)
            for part, data in tracks.items()
        }

    def __pad_to_width(self, data, width):
        d = len(data.shape)
        n = width - data.shape[0]
        pad_width = np.array([(0, 0)]*(d-1) + [(0, n)])
        return np.pad(data, pad_width)

    def __normalize(self, tracks):
        # normalize 防止有时因浮点数经度问题导致出现不在 [-1, 1] 内的值
        # 同时让 mixer 获取到的数据更统一
        return {
            part: normalize(data)
            for part, data in tracks.items()
        }

    def __getitem__(self, name):
        return self.symbols[name]

    def __setitem__(self, name, value):
        self.symbols[name] = value


__all__ = ['Score']
