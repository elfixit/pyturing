__author__ = 'oups'

from bitarray import bitarray
import datetime

class Tape(object):

    def __init__(self,
                 start_values="",
                 alphabet_length=1,
                 alphabet={
                        '.':  bitarray('0'),
                        '1':   bitarray('1') },
                 tape_size=2**32
    ):
        self.__data = bitarray(tape_size)
        self.__current_pos = self.__data.length() / 2 / alphabet_length
        self.__alphabet = alphabet
        self.__alphabet_length = alphabet_length
        i = 1
        for char in start_values:
            self[self.__current_pos + i] = char
            i += 1

    def slice_i(self, i):
        assert 0 <= i < self.__data.length()
        return slice(self.__alphabet_length * i, self.__alphabet_length * (i + 1))

    def __getitem__(self, i):
        return self.__data[self.slice_i(i)].decode(self.__alphabet)[0]

    def __setitem__(self, i, v):
        a = bitarray()
        a.encode(self.__alphabet, v)
        self.__data[self.slice_i(i)] = a[:self.__alphabet_length]

    def length(self):
        return self.__data.length / self.__alphabet_length

    def get_current_value(self):
        return self[self.__current_pos]

    def set_current_value(self, value):
        self[self.__current_pos] = value

    current_value = property(get_current_value, set_current_value)

    @property
    def position(self):
        return self.__current_pos

    def move(self, operation="N"):
        if operation == "R":
            self.__current_pos += 1
        elif operation == "L":
            self.__current_pos -= 1

    #primitiv helper func for ui..
    def befor(self, num=15):
        values = []
        pos = self.__current_pos - (num - 1)
        while pos < self.__current_pos:
            values.append(self[pos])
            pos += 1
        return values

    #primitiv helper func for ui
    def after(self, num=15):
        values = []
        pos = self.__current_pos + 1
        while pos < self.__current_pos + (num + 1):
            values.append(self[pos])
            pos += 1
        return values

class TuringMachine(object):
    def __init__(self,
                 init_tapes=[],
                 alphabet = [False, True],
                 alphabet_bitsize = 1,
                 initial_state="init",
                 accepting_states="final",
                 transition_function={},
                 num_tapes=1):
        self.__state = initial_state
        self.__accepting_states = accepting_states
        self.__transition_function = transition_function
        self.__transition_keys = transition_function.keys()
        self.__tapes = []
        self.__steps = 0
        self.time = datetime.timedelta(0)
        self.starttime = datetime.datetime.now()
        self.status = ()
        self.transition = ()
        i = 0
        while i < num_tapes:
            self.__tapes.append(Tape(init_tapes[i], alphabet_bitsize, alphabet))
            i += 1

    @property
    def finished(self):
        if self.__state in self.__accepting_states:
            return True
        else:
            return False

    @property
    def current_values(self):
        values = (tape.current_value for tape in self.__tapes)
        return tuple(values)


    @property
    def tapes(self):
        return self.__tapes


    def step(self):
        if self.__steps == 0:
            self.starttime = datetime.datetime.now()
        status = (self.__state, self.current_values)
        if status in self.__transition_keys:
            self.status = status
            self.transition = self.__transition_function[self.status]
            self.__state = self.transition[0]
            i = 0
            while i < len(self.transition[1]):
                if self.status[1][i] != self.transition[1][i]:
                    self.__tapes[i].current_value = self.transition[1][i]
                i += 1
            i = 0
            for move in self.transition[2]:
                self.__tapes[i].move(move)
                i += 1
            self.__steps += 1
        else:
            self.status = "state unknown!! status: %s" % self.__state
        if self.finished:
            self.time = datetime.datetime.now() - self.starttime

    def run(self):
        start = datetime.datetime.now()
        while not self.finished:
            self.step()
        end = datetime.datetime.now()
        return end - start

    @property
    def steps(self):
        return self.__steps
