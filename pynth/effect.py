from abc import abstractmethod


class Effect:
    @abstractmethod
    def apply(self, data):
        pass

    def __rshift__(self, other):
        return ChainedEffect(self, other)


class ChainedEffect(Effect):
    def __init__(self, effect1, effect2):
        self.effect1 = effect1
        self.effect2 = effect2

    def apply(self, data):
        return self.effect2.apply(self.effect1.apply(data))
