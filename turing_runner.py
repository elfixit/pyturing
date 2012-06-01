#!/usr/bin/python
__author__ = 'oups'

import fakultunaer
import multiunaer

from bitarray import bitarray
from turing import TuringMachine
import curses


def get_param(prompt_string):
     screen.clear()
     screen.border(0)
     screen.addstr(2, 2, prompt_string)
     screen.refresh()
     input = screen.getstr(10, 10, 60)
     return input

def get_result(turing, respos, loc):
    if turing.finished:
        result = long(0)
        if loc == 'L':
            pos = turing.tapes[respos].position - 1
            while turing.tapes[respos][pos] == '1':
                result += 1
                pos -= 1
            return result
        else:
            pos = turing.tapes[respos].position + 1
            while turing.tapes[respos][pos] == '1':
                result += 1
                pos += 1
            return result
    else:
        return '?'

def run_turing(berechnung, turing, respos, loc):
    x = 0

    while x != ord('e'):
        screen.clear()
        screen.border(0)
        screen.addstr(2,2, "Turing Maschine von Christoffel Gehring und Felix Marthaler")
        screen.addstr(4,4, "Berechung: %s" % berechnung)
        screen.addstr(6,4, "r - run throw")
        screen.addstr(7,4, "s - step by step")
        screen.addstr(8,4, "e - exit")

        i = 0
        while i < len(turing.tapes):
            tapestrpartsbefor = [" %s" % char for char in turing.tapes[i].befor()]
            tapestrpartsafter = [" %s" % char for char in turing.tapes[i].after()]
            tapestr = "|%s |%s|%s |" % (''.join(tapestrpartsbefor), turing.tapes[i].current_value, ''.join(tapestrpartsafter))
            screen.addstr(10+i, 4, tapestr)
            i += 1

        screen.addstr(15,4, "Status: %s      Transition: %s" % (str(turing.status), str(turing.transition)))
        screen.addstr(16,4, "Steps: %s" % str(turing.steps))
        screen.addstr(17,4, "Time: %s ms" % str(turing.time))
        screen.addstr(18,4, "Result: %s" % str(get_result(turing, respos, loc)))
        screen.refresh()
        x = screen.getch()

        if x == ord('s'):
            turing.step()
        elif x == ord('r'):
            turing.run()


if __name__ == "__main__":

    x = 0
    screen = curses.initscr()
    while x != ord('e'):

        screen.clear()
        screen.border(0)
        screen.addstr(2,2, "Turing Maschine von Christoffel Gehring und Felix Marthaler")
        screen.addstr(4,4, "m - zum Multiplizieren")
        screen.addstr(6,4, 'f - zur Berechnung der Faktult')
        screen.addstr(8,4, 'e - exit')

        x = screen.getch()

        if x == ord('m'):
            # get multi
            num1 = int(get_param("Erste Nummer:"))
            num2 = int(get_param("Zweite Nummer:"))
            name, turing, respos, loc = multiunaer.setup(num1, num2)
            run_turing(name, turing, respos, loc)
        elif x == ord('f'):
            num = int(get_param("Deine Nummer:"))
            name, turing, respos, loc= fakultunaer.setup(num)
            run_turing(name, turing, respos, loc)
    screen.clear()
    curses.endwin()
