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


def truncate(s, str_width):
    return len(s) > str_width and s[:str_width - 3] + "..." or s


class TopNViz(object):
    # CONSTANTS
    INIT_COLS = 200
    INIT_LINES = 200

    QUIT_KEYS = (ord('q'), ord('Q'))
    DOWN_KEYS = (curses.KEY_DOWN, curses.KEY_SF)
    UP_KEYS = (curses.KEY_UP, curses.KEY_SR)

    UP = -1
    DOWN = 1

    def __init__(self, f):
        self._f = f  # Input file/pipe
        self._stdscr = None  # Real screen
        self._pad = None  # Virtual scroll-able screen

        # self._n = n  # Max number of QNAMEs positions
        # self._n_width = len(str(self.n))  # Width of max n value string
        self._n_width = 3  # Width of max n value string
        self._headline = 0  # First line on the page (0 to len(last_data)-1)
        self._high_line = 0  # Highlighted line (0 to len(last_data)-1)
        self._term_size = (0, 0)  # Current terminal size (y,x)
        self._need_refresh = False  # Refresh flag
        self._last_data = []  # Last input data

    def main(self, screen):
        self._stdscr = screen
        self._pad = curses.newpad(self.INIT_LINES, self.INIT_COLS)

        # Terminal setup
        # self.stdscr.scrollok(True)
        self._stdscr.nodelay(True)
        curses.curs_set(0)
        self.get_term_size()

        # Main loop
        running = True
        while running:
            # Input reading
            if self._f in select.select([self._f, sys.stdin], [], [], 0)[0]:
                self._last_data = self.read_data()
                self._need_refresh = True

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
                elif ch == curses.KEY_RESIZE:
                    self.get_term_size()
                    self._stdscr.resize(self._term_size[0], self._term_size[1])
                ch = screen.getch()

            if self._need_refresh:
                self.refresh_view()
            curses.napms(50)

    def read_data(self):
        line = self._f.readline()
        # print(line, file=sys.stderr)
        if not line:
            print("Fatal Error: Broken pipe, EOF found", file=sys.stderr)
            exit(-1)

        try:
            json_list = json.loads(line)
        except ValueError:
            print("Error: Input line is not JSON-serialized: '",
                  repr(line), file=sys.stderr)
            return self._last_data

        return list(json_list)

    def refresh_view(self):
        self._need_refresh = False
        if len(self._last_data) == 0:
            return

        # print(len(self.last_data), file=sys.stderr)
        # Clear screen
        self._pad.clear()

        # Adjust highlighted and head line if needed
        if self._high_line > len(self._last_data) - 1:
            self._high_line = len(self._last_data) - 1
            self._headline = max(0, len(self._last_data) - self._term_size[0])

        # Adjust pad length if needed
        pad_size = self._pad.getmaxyx()
        if len(self._last_data) > pad_size[0]:
            self._pad.resize(len(self._last_data), pad_size[1])

        cnt_width = len(str(self._last_data[0][1]))
        str_width = self._term_size[1] - self._n_width - cnt_width - 2
        str_width = str_width if str_width >= 3 else 3

        pos = 1
        last_cnt = self._last_data[0][1]
        for i, (qname, cnt) in enumerate(self._last_data, start=0):
            if last_cnt != cnt:
                pos += 1
                last_cnt = cnt

            line = "{0!s: >{poslen}} " \
                   "{1: <{strlen}}" \
                   " {2!s: >{cntlen}}".format(pos,
                                              truncate(qname, str_width),
                                              cnt,
                                              poslen=self._n_width,
                                              strlen=str_width,
                                              cntlen=cnt_width)
            # print(len(line), file=sys.stderr)
            if self._high_line == i:
                self._pad.addstr(i, 0, line, curses.A_REVERSE)
            else:
                self._pad.addstr(i, 0, line)

        for i in range(len(self._last_data), self.INIT_LINES):
            if self._high_line == i:
                self._pad.addstr(i, 0, "~", curses.A_REVERSE)
            else:
                self._pad.addstr(i, 0, "~")

        self._pad.refresh(self._headline, 0, 0, 0, self._term_size[
                         0] - 1, self._term_size[1] - 1)

    def get_term_size(self):
        self._term_size = self._stdscr.getmaxyx()
        # print(self.term_size, file=sys.stderr)
        self._headline = 0
        self._high_line = 0
        self._need_refresh = True

        # Resize pad width if needed
        pad_size = self._pad.getmaxyx()
        if self._term_size[1] > pad_size[1]:
            self._pad.resize(pad_size[0], self._term_size[1])

        # Touch all the window, to redraw
        self._stdscr.redrawwin()
        self._pad.redrawwin()

    def move_high_line(self, direction):
        if direction == self.UP and \
                self._headline == self._high_line:  # Top highlight
            if self._headline > 0:  # Not first line
                self._headline += self.UP
            else:
                # print("headline ", str(self.headline), "\nhighline ",
                #      str(self.high_line), file=sys.stderr)
                return
        # Bottom highlight
        elif direction == self.DOWN and self._headline +\
                self._term_size[0] - 1 == self._high_line:
            # Not last line
            if self._headline + self._term_size[0] < len(self._last_data) - 1:
                self._headline += self.DOWN
            else:
                # print("headline ", str(self.headline), "\nhighline ",
                #      str(self.high_line), file=sys.stderr)
                return

        self._high_line += direction
        self._need_refresh = True
        # print("headline ", str(self.headline), "\nhighline ",
        #      str(self.high_line), file=sys.stderr)


if __name__ == '__main__':
    input_file = open("input", "r", 1)
    viz = TopNViz(input_file)

    # Debug-friendly curses wrapper
    curses.wrapper(viz.main)
