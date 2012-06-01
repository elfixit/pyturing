__author__ = 'oups'
from bitarray import bitarray
from turing import TuringMachine

def setup(num1, num2):
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
        ("MultiRight", ('1', '1', '.')):("MultiRight", ('1', '1', '1'), ('N', 'R', 'R')),
        ("MultiRight", ('1', '.', '.')):("MultiLeft", ('1', '.', '.'), ('R', 'L', 'N')),
        ("MultiLeft", ('1', '1', '.')): ("MultiLeft", ('1', '1', '1'), ('N', 'L', 'R')),
        ("MultiLeft", ('1', '.', '.')): ("MultiRight", ('1', '.', '.'), ('R', 'R', 'N')),
        ("MultiLeft", ('.', '.', '.')): ("Finish", ('.', '.', '.'), ()),
        ("MultiLeft", ('.', '1', '.')): ("Finish", ('.', '.', '.'), ()),
        ("MultiRight", ('.', '.', '.')):("Finish", ('.', '.', '.'), ()),
        ("MultiRight", ('.', '1', '.')):("Finish", ('.', '.', '.'), ()),
    }
    num1str = ''
    i = 1
    while i <= num1:
        num1str += '1'
        i += 1

    num2str = ''
    i = 1
    while i <= num2:
        num2str += '1'
        i += 1

    tape_init = [num1str, num2str, '']

    turing = TuringMachine(tape_init, alphabet, alphabet_bitsize, initial_state, accepting_states, transition_functions, num_tapes)
    return ("%s * %s" % (str(num1), str(num2)), turing, 2, 'L')
