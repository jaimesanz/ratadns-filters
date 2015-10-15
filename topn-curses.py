#! /usr/bin/env python2
from __future__ import print_function
import curses
import json
import select
import signal
import sys

# sys.path.extend(['/opt/pycharm-professional/debug-eggs/pycharm-debug.egg'])
# import pydevd
# pydevd.settrace('localhost', port=46018, suspend=False)


class TopNViz(object):
    # CONSTANTS
    MAX_COLS = 100
    MAX_LINES = 200

    QUIT_KEYS = (ord('q'), ord('Q'))
    DOWN_KEYS = (curses.KEY_DOWN, curses.KEY_SF)
    UP_KEYS = (curses.KEY_UP, curses.KEY_SR)

    UP = -1
    DOWN = 1

    def __init__(self, f):
        self.f = f  # Input file/pipe
        self.stdscr = None  # Real screen
        self.pad = None  # Virtual scroll-able screen

        # self.n = n  # Max number of QNAMEs positions
        # self.n_width = len(str(self.n))  # Width of max n value string
        self.n_width = 3  # Width of max n value string
        self.headline = 0  # First line on the page (0 to len(last_data)-1)
        self.high_line = 0  # Highlighted line (0 to len(last_data)-1)
        self.term_size = (0, 0)  # Current terminal size (y,x)
        self.need_refresh = False  # Refresh flag
        self.last_data = []  # Last input data

    def main(self, screen):
        self.stdscr = screen
        self.pad = curses.newpad(self.MAX_LINES, self.MAX_COLS)

        # Terminal setup
        # self.stdscr.scrollok(True)
        self.stdscr.nodelay(True)
        curses.curs_set(0)
        self.get_term_size()

        # Main loop
        running = True
        while running:
            # Input reading
            if self.f in select.select([self.f, sys.stdin], [], [], 0)[0]:
                self.last_data = self.read_data()
                self.need_refresh = True

            # Catch pressed keys
            ch = screen.getch()
            while ch != curses.ERR:
                # print("Debug: key pressed", ch, file=sys.stderr)
                if ch in self.UP_KEYS:
                    self.move_high_line(self.UP)
                elif ch in self.DOWN_KEYS:
                    self.move_high_line(self.DOWN)
                elif ch in self.QUIT_KEYS:
                    running = False
                ch = screen.getch()

            if self.need_refresh:
                self.refresh_view()
            curses.napms(50)

    def read_data(self):
        line = self.f.readline()
        # print(line, file=sys.stderr)
        if not line:
            print("Fatal Error: Broken pipe, EOF found", file=sys.stderr)
            exit(-1)

        try:
            json_list = json.loads(line)
        except ValueError:
            print("Error: Input line is not JSON-serialized: '", repr(line), file=sys.stderr)
            return self.last_data

        return list(json_list[:self.MAX_LINES])

    def refresh_view(self):
        self.need_refresh = False
        if len(self.last_data) == 0:
            return

        # print(len(self.last_data), file=sys.stderr)
        # Clear screen
        self.pad.clear()

        # Adjust highlighted and head line if needed
        if self.high_line > len(self.last_data) - 1:
            self.high_line = len(self.last_data) - 1
            self.headline = max(0, len(self.last_data) - self.term_size[0])

        cnt_width = len(str(self.last_data[0][1]))
        str_width = self.term_size[1] - self.n_width - cnt_width - 2
        str_width = str_width if str_width >= 3 else 3

        truncate = lambda s: len(s) > str_width and s[:str_width - 3] + "..." or s

        pos = 1
        last_cnt = self.last_data[0][1]
        for i, (qname, cnt) in enumerate(self.last_data, start=0):
            if last_cnt != cnt:
                pos += 1
                last_cnt = cnt

            line = "{0!s: >{poslen}} {1: <{strlen}} {2!s: >{cntlen}}".format(pos, truncate(qname), cnt,
                                                                             poslen=self.n_width, strlen=str_width,
                                                                             cntlen=cnt_width)
            # print(len(line), file=sys.stderr)
            if self.high_line == i:
                self.pad.addstr(i, 0, line, curses.A_REVERSE)
            else:
                self.pad.addstr(i, 0, line)

        for i in range(len(self.last_data), self.MAX_LINES):
            if self.high_line == i:
                self.pad.addstr(i, 0, "~", curses.A_REVERSE)
            else:
                self.pad.addstr(i, 0, "~")

        self.pad.refresh(self.headline, 0, 0, 0, self.term_size[0] - 1, self.term_size[1] - 1)

    def get_term_size(self, signum=None, frame=None):
        self.term_size = self.stdscr.getmaxyx()
        # print(self.term_size, file=sys.stderr)
        self.headline = 0
        self.high_line = 0
        self.need_refresh = True

        # Touch all the window, to redraw
        self.stdscr.redrawwin()
        self.pad.redrawwin()

    def move_high_line(self, direction):
        if direction == self.UP and self.headline == self.high_line:  # Top highlight
            if self.headline > 0:  # Not first line
                self.headline += self.UP
            else:
                # print("headline ", str(self.headline), "\nhighline ", str(self.high_line), file=sys.stderr)
                return
        elif direction == self.DOWN and self.headline + self.term_size[0] - 1 == self.high_line:  # Bottom highlight
            if self.headline + self.term_size[0] < len(self.last_data) - 1:  # Not last line
                self.headline += self.DOWN
            else:
                # print("headline ", str(self.headline), "\nhighline ", str(self.high_line), file=sys.stderr)
                return

        self.high_line += direction
        self.need_refresh = True
        # print("headline ", str(self.headline), "\nhighline ", str(self.high_line), file=sys.stderr)


if __name__ == '__main__':
    input_file = open("input", "r", 1)
    viz = TopNViz(input_file)

    # Catch Terminal resize signal
    signal.signal(signal.SIGWINCH, viz.get_term_size)
    # Debug-friendly curses wrapper
    curses.wrapper(viz.main)
