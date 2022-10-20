from copy import copy
from inspect import isclass

import IPython.display as ipd
import numpy as np

from .let import Let
from .note import NamedNote, Note, R
from .tempo import Tempo


class AudioCompiler:
    def __init(self, instrument, tempo):
        self.__instrument = instrument
        self.__tempo = Tempo.create(tempo)
        self.__saved_instrument = instrument
        self.__saved_tempo = tempo
        self.__p8 = None
        self.__dur = None
        self.__nchannel = None
        self.__rest_idx = []
        self.__let_idx = []

    def compile(self, instrument, tempo, symbols):
        self.__init(instrument, tempo)
        data = [self.__compile_symbol(i, it) for i, it in enumerate(symbols)]

        if self.__nchannel == None:
            self.__nchannel = len(self.__instrument.wav.map([0], [0], [0]))

        if self.__nchannel != 1:
            for i in self.__rest_idx:
                data[i] = np.zeros([self.__nchannel, len(data[i])])
            for i in self.__let_idx:
                data[i] = np.empty([self.__nchannel, 0])

        if len(data) == 0:
            return np.empty(0 if self.__nchannel == 1 else [self.__nchannel, 0])

        return np.concatenate(data, axis=0 if self.__nchannel == 1 else 1)

    def audio(self, instrument, tempo, symbols, autoplay=False, normalize=False):
        data = self.compile(instrument, tempo, symbols)
        return ipd.Audio(
            data if len(data) != 0 else [0],
            rate=instrument.sr,
            autoplay=autoplay,
            normalize=normalize
        )

    def __compile_symbol(self, i, symbol):
        if isclass(symbol):
            if issubclass(symbol, NamedNote):
                note = symbol().complete(self.__p8, self.__dur)  # type: ignore
                return self.__compile_named_note(note)
            elif issubclass(symbol, R):
                return self.__compile_rest(i, symbol().complete(self.__dur))
            elif issubclass(symbol, Note):
                return self.__compile_note(symbol().complete(self.__dur))
            else:
                raise Exception(f"不明符号 {symbol}")
        else:
            if isinstance(symbol, NamedNote):
                return self.__compile_named_note(symbol.complete(self.__p8, self.__dur))
            elif isinstance(symbol, R):
                return self.__compile_rest(i, symbol.complete(self.__dur))
            elif isinstance(symbol, Note):
                return self.__compile_note(symbol.complete(self.__dur))
            elif isinstance(symbol, Let):
                self.__let_idx.append(i)
                self.__let_context(symbol)
                return np.empty(0)
            else:
                raise Exception(f"不明符号 {symbol}")

    def __compile_named_note(self, note):
        self.__before_produce(note)
        data = self.__instrument.produce(
            note.freq, self.__tempo.convert(note.dur))
        self.__after_produce(note)

        self.__p8 = note.p8
        self.__dur = note.dur

        if self.__nchannel == None:
            self.__nchannel = 1 if len(data.shape) == 1 else data.shape[0]

        return data

    def __compile_rest(self, i, note):
        self.__before_produce(note)
        data = np.zeros(int(self.__tempo.convert(
            note.dur) * self.__instrument.sr))
        self.__after_produce(note)

        self.__dur = note.dur
        self.__rest_idx.append(i)

        return data

    def __compile_note(self, note):
        self.__before_produce(note)
        data = self.__instrument.produce(
            note.freq, self.__tempo.convert(note.dur))
        self.__after_produce(note)

        self.__dur = note.dur
        if self.__nchannel == None:
            self.__nchannel = 1 if len(data.shape) == 1 else data.shape[0]

        return data

    def __before_produce(self, note):
        if note.after_let:
            self.__let_context(note.after_let)
        if note.that_let:
            self.__save_context()
            self.__let_context(note.that_let)

    def __after_produce(self, note):
        if note.that_let:
            self.__load_context()
        if note.then_let:
            self.__let_context(note.then_let)

    def __save_context(self):
        self.__saved_tempo = self.__tempo
        self.__instrument, self.__saved_instrument =\
            copy(self.__instrument), self.__instrument

    def __let_context(self, let):
        if let.wav != None:
            self.__instrument.wav = let.wav
        if let.amp != None:
            self.__instrument.amp = let.amp
        if let.freq != None:
            self.__instrument.freq = let.freq
        if let.fx != None:
            self.__instrument.fx = let.fx
        if let.tempo != None:
            self.__tempo = Tempo.create(let.tempo)
        if let.p8 != None:
            self.__p8 = let.p8
        if let.dur != None:
            self.__dur = let.dur

    def __load_context(self):
        self.__tempo = self.__saved_tempo
        self.__instrument = self.__saved_instrument


__all__ = ['AudioCompiler']
