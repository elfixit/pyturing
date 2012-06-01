from bitarray import bitarray
from turing import TuringMachine

def setup(num):
    alphabet = {
        '.':  bitarray('0'),
        '1':  bitarray('1')
    }

    alphabet_bitsize = 1

    initial_state = "Init"

    num_tapes = 3

    accepting_states = ["Finish",]

    transition_functions = {
        ("Init", ('.', '.', '.')):      ("Init", ('.', '.', '.'), ('R', 'R', 'N')),
        ("Init", ('1', '1', '.')):      ("MultiRight", ('1', '1', '1'), ('N', 'R', 'R')),
        ("Init", ('1', '.', '.')):      ("SetupStart", ('.', '1', '.'), ('R', 'R', 'N')),
        ("SetupStart", ('1', '.', '.')):("SetupStart", ('1', '1', '.'), ('R', 'R', 'N')),
        ("SetupStart", ('.', '.', '.')):("SetupStartPos", ('.', '.', '.'), ('L', 'L', 'N')),
        ("SetupStartPos", ('1', '1', '.')):("SetupStartPos", ('1', '1', '.'), ('L', 'L', 'N')),
        ("SetupStartPos", ('.', '1', '.')):("Init", ('.', '1', '.'), ('N', 'L', 'N')),
        ("MultiRight", ('1', '1', '.')):("MultiRight", ('1', '1', '1'), ('N', 'R', 'R')),
        ("MultiRight", ('1', '.', '.')):("MultiLeft", ('1', '.', '.'), ('R', 'L', 'N')),
        ("MultiLeft", ('1', '1', '.')): ("MultiLeft", ('1', '1', '1'), ('N', 'L', 'R')),
        ("MultiLeft", ('1', '.', '.')): ("MultiRight", ('1', '.', '.'), ('R', 'R', 'N')),
        ("MultiLeft", ('.', '1', '.')): ("ResetLeft", ('.', '.', '.'), ('L', 'N', 'N')),
        ("MultiRight", ('.', '1', '.')):("ResetRight", ('.', '.', '.'), ('L', 'N', 'N')),

        ("ResetLeft", ('1', '.', '.')): ('ResetLeft', ('.', '.', '.'), ('N', 'L', 'N')),
        ("ResetLeft", ('1', '1', '.')): ('ResetLeft', ('.', '.', '.'), ('N', 'L', 'N')),
        ("ResetLeft", ('.', '1', '.')): ('ResetLeft', ('.', '.', '.'), ('N', 'L', 'N')),
        ("ResetLeft", ('.', '.', '.')): ('CopyStart', ('.', '.', '.'), ('N', 'N', 'L')),

        ("ResetRight", ('1', '.', '.')): ('ResetRight', ('.', '.', '.'), ('N', 'R', 'N')),
        ("ResetRight", ('1', '1', '.')): ('ResetRight', ('.', '.', '.'), ('N', 'R', 'N')),
        ("ResetRight", ('.', '1', '.')): ('ResetRight', ('.', '.', '.'), ('N', 'R', 'N')),
        ("ResetRight", ('.', '.', '.')): ('CopyStart', ('.', '.', '.'), ('N', 'N', 'L')),

        ("CopyStart", ('.', '.', '1')): ('CopyStart', ('.', '1', '.'), ('N', 'L', 'L')),
        ("CopyStart", ('.', '.', '.')): ('Move1Start', ('.', '.', '.'), ('L', 'N', 'N')),

        ("Move1Start", ('1', '.', '.')): ('Move1Start', ('1', '.', '.'), ('L', 'N', 'N')),
        ("Move1Start", ('.', '.', '.')): ('CheckRight', ('.', '.', '.'), ('R', 'N', 'N')),
        ("CheckRight", ('1', '.', '.')): ('MultiRight', ('1', '.', '.'), ('N', 'R', 'N')),
        ("CheckRight", ('.', '.', '.')): ('CheckLeft', ('.', '.', '.'), ('L', 'N', 'N')),
        ("CheckLeft", ('.', '.', '.')): ('CheckLeft2', ('.', '.', '.'), ('L', 'N', 'N')),
        ('CheckLeft2', ('.', '.', '.')): ('Finish', ('.', '.', '.'), ()),
        ("Move2Start", ('.', '.', '.')): ('Finish', ('.', '.', '.'), ('N', 'N', 'N')),
        ("Move2Start", ('.', '1', '.')): ('Finish', ('.', '1', '.'), ('N', 'L', 'N')),
        ("Move2Start", ('1', '1', '.')): ('MultiRight', ('.', '.', '.'), ('R', 'R', 'N')),
        ("Move1Start", ('.', '1', '.')): ('Finish', ('.', '.', '.'), ()),
        ("MultiRight", ('.', '.', '.')): ('Finish', ('.', '.', '.'), ('')),
        ("CheckLeft", ('.', '.', '.')): ('Finish', ('.', '.', '.'), ()),
    }

    numstr = ''
    i = 1
    while i <= num:
        numstr += '1'
        i += 1

    tape_init = [numstr, '', '']

    turing = TuringMachine(tape_init, alphabet, alphabet_bitsize, initial_state, accepting_states, transition_functions, num_tapes)
    return ("%s!" % str(num), turing, 1, 'R')
