#! /usr/bin/python2
from __future__ import print_function
import curses, json, select, signal, sys, os
# import pydevd

# pydevd.settrace('localhost', port=46018)
# CONSTANTS
MAX_COLS = 100
MAX_ROWS = 200

# GLOBALS
# Input file/pipe
f = open("input", "r", 1)

# First screen showing line, for tabbing
heading_line = 0

term_size = (0, 0)  # Current terminal size (y,x)
need_refresh = False
last_data = []


def refresh_view(screen):
    global need_refresh

    need_refresh = False
    if not last_data:
        return

    # Clear screen
    screen.clear()

    pos_width = len(str(len(last_data)))
    cnt_width = len(str(last_data[0][1]))
    str_width = term_size[1] - pos_width - cnt_width - 2  # TODO Check!
    str_width = str_width if str_width >= 3 else 3

    truncar = lambda str: len(str) > str_width and str[:str_width - 3] + "..." or str

    for pos, (qname, cnt) in enumerate(last_data, start=1):
        line = "{0!s: >{poslen}} {1: <{strlen}} {2!s: >{cntlen}}".format(pos, truncar(qname), cnt,
                                                                         poslen=pos_width, strlen=str_width,
                                                                         cntlen=cnt_width)
        screen.addstr(pos, 0, line)

    screen.refresh(0, 0, 0, heading_line, term_size[0] - 1, heading_line + term_size[1] - 1)


def main(screen):
    global stdscr, heading_line, need_refresh, last_data

    stdscr = screen
    # Terminal setup
    # screen.scrollok(True)
    screen.nodelay(True)
    # screen.border()
    curses.curs_set(2)
    get_size()
    pad = curses.newpad(MAX_ROWS, MAX_COLS)

    # Main loop
    running = True
    while running:
        # Non-blocking input reading
        while f in select.select([f], [], [], 0)[0]:
            last_data = read_data()
            need_refresh = True
            break

        if need_refresh:
            refresh_view(pad)

        # Catch pressed keys
        ch = screen.getch()
        while ch != curses.ERR:
            # print("Debug: key pressed", ch, file=sys.stderr)
            if ch == curses.KEY_UP or ch == curses.KEY_SR:
                heading_line+= 1 if heading_line < len(last_data) else 0
                # screen.scroll(1)
                # screen.refresh()
            elif ch == curses.KEY_DOWN or ch == curses.KEY_SF:
                heading_line+= -1 if heading_line < len(last_data) else 0
                # screen.scroll(-1)
                # screen.refresh()
            elif ch == ord("q") or ch == ord("Q"):
                running = False
            ch = screen.getch()
        curses.napms(200)


def read_data():
    line = f.readline()
    print(line, file=sys.stderr)
    if not line:
        print("Broken pipe, EOF found", file=sys.stderr)
        exit(-1)
    json_list = json.loads(line)

    return list(json_list)


def get_size(*args, **kwargs):
    global term_size, need_refresh

    term_size = stdscr.getmaxyx()
    print(term_size, file=sys.stderr)
    need_refresh = True


if __name__ == '__main__':
    # Catch Terminal resize signal
    signal.signal(signal.SIGWINCH, get_size)

    # Debug-friendly curses wrapper
    curses.wrapper(main)
