class Let:
    def __init__(self, wav=None, amp=None, freq=None, fx=None, tempo=None, p8=None, dur=None) -> None:
        self.wav = wav
        self.amp = amp
        self.freq = freq
        self.fx = fx
        self.tempo = tempo
        self.p8 = p8
        self.dur = dur


let = Let

__all__ = ['let']
