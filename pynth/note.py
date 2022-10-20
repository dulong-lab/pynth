from copy import copy
from functools import cached_property

from .let import Let


class NoteMeta(type):
    def __truediv__(cls, value):
        return cls().__truediv__(value)


class Note(metaclass=NoteMeta):
    def __init__(self):
        self.dur = None
        self.after_let = None
        self.that_let = None
        self.then_let = None
        self.after = self.__after
        self.that = self.__that
        self.then = self.__then

    def __truediv__(self, value):
        obj = copy(self)
        obj.dur = 1.0 / value
        return obj

    def __mul__(self, value):
        obj = copy(self)
        obj.dur *= value
        return obj

    @classmethod
    def after(cls, wav=None, amp=None, freq=None, fx=None):
        return cls().__after(wav, amp, freq, fx)

    @classmethod
    def that(cls, wav=None, amp=None, freq=None, fx=None):
        return cls().__that(wav, amp, freq, fx)

    @classmethod
    def then(cls, wav=None, amp=None, freq=None, fx=None):
        return cls().__then(wav, amp, freq, fx)

    def __after(self, wav=None, amp=None, freq=None, fx=None):
        obj = copy(self)
        obj.after_let = Let(wav=wav, amp=amp, freq=freq, fx=fx)
        return obj

    def __that(self, wav=None, amp=None, freq=None, fx=None):
        obj = copy(self)
        obj.that_let = Let(wav=wav, amp=amp, freq=freq, fx=fx)
        return obj

    def __then(self, wav=None, amp=None, freq=None, fx=None):
        obj = copy(self)
        obj.then_let = Let(wav=wav, amp=amp, freq=freq, fx=fx)
        return obj

    def complete(self, dur):
        if self.dur != None:
            return self

        obj = copy(self)
        obj.dur = dur
        return obj


class N(Note):
    def __init__(self, freq):
        super().__init__()
        self.freq = freq


class R(Note):
    pass


class NamedNoteMeta(NoteMeta):
    def __pos__(cls):
        return cls().__pos__()

    def __neg__(cls):
        return cls().__neg__()


class NamedNote(Note, metaclass=NamedNoteMeta):
    def __init__(self, std_freq, p8):
        super().__init__()
        self.std_freq = std_freq
        self.p8 = p8
        self.accidental = 0

    def __pos__(self):
        # TODO: 错误检查
        obj = copy(self)
        obj.accidental += 1
        return obj

    def __neg__(self):
        # TODO: 错误检查
        obj = copy(self)
        obj.accidental -= 1
        return obj

    def complete(self, p8, dur):
        if self.p8 != None and self.dur != None:
            return self

        obj = copy(self)
        if obj.p8 == None:
            obj.p8 = p8
        if obj.dur == None:
            obj.dur = dur
        return obj

    @cached_property
    def freq(self):
        return self.std_freq * 2**(self.p8-4 + self.accidental/12)


class C(NamedNote):
    def __init__(self, p8=None):
        super().__init__(440.0 * 2**(-9/12), p8)


class D(NamedNote):
    def __init__(self, p8=None):
        super().__init__(440.0 * 2**(-7/12), p8)


class E(NamedNote):
    def __init__(self, p8=None):
        super().__init__(440.0 * 2**(-5/12), p8)


class F(NamedNote):
    def __init__(self, p8=None):
        super().__init__(440.0 * 2**(-4/12), p8)


class G(NamedNote):
    def __init__(self, p8=None):
        super().__init__(440.0 * 2**(-2/12), p8)


class A(NamedNote):
    def __init__(self, p8=None):
        super().__init__(440.0, p8)


class B(NamedNote):
    def __init__(self, p8=None):
        super().__init__(440.0 * 2**(2/12), p8)


__all__ = ['Note', 'N', 'R', 'C', 'D', 'E', 'F', 'G', 'A', 'B']
