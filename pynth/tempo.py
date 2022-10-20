from typing import Iterable


class Tempo:
    def __init__(self, number, referent=1/4, text=None):
        self.number = number
        self.referent = referent
        self.text = text
        self.__seconds_per_whole_note = 60 / (number * referent)

    def convert(self, dur):
        return self.__seconds_per_whole_note * dur

    @classmethod
    def create(cls, args):
        if isinstance(args, (int, float)):
            return Tempo(args)
        elif isinstance(args, Iterable):
            return Tempo(*args)
        else:
            return args


class NamedTempo(Tempo):
    def __call__(self, number, referent=None):
        return NamedTempo(number, referent or self.referent, self.text)


Allegro = NamedTempo(120, 1/4, "Allegro")

__all__ = ['Tempo', 'Allegro']
