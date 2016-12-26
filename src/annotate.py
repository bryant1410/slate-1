#!/usr/bin/env python3

from __future__ import print_function

import curses
import argparse
import logging
import sys

from data import *
from config import *
from view import *

def annotate(window, config, filenames):
    out_filename = "files_still_to_do"
    overwrite = False
    for i in range(len(sys.argv)):
        if sys.argv[i] == '-log' and len(sys.argv) > i + 1:
            out_filename = sys.argv[i + 1]
        if sys.argv[i] == '-overwrite':
            overwrite = True
    out = open(out_filename, "w")

    # Set color combinations
    for num, fore, back in COLORS:
        curses.init_pair(num, fore, back)

    # No blinking cursor
    curses.curs_set(0)

    cfilename = 0
    datum = Datum(filenames[cfilename], config)
    view = View(window, [0, 0], datum, config, cfilename, len(filenames))

    at_end = None
    while True:
        if at_end is None:
            # Draw screen
            view.render()
            # Get input
            user_input = window.getch()

            if user_input == curses.KEY_LEFT: view.move_left()
            elif user_input == curses.KEY_SLEFT: view.move_to_start()
            elif user_input == curses.KEY_RIGHT: view.move_right()
            elif user_input == curses.KEY_SRIGHT: view.move_to_end()
            elif user_input == curses.KEY_UP: view.move_up()
            elif user_input == 337: view.move_to_top() # SHIFT + UP, Worked out on a Mac by hand...
            elif user_input == curses.KEY_DOWN: view.move_down()
            elif user_input == 336: view.move_to_bottom() # SHIFT + DOWN, Worked out on a Mac by hand...
            elif user_input == ord("n"): view.next_number()
            elif user_input == ord("h"): view.toggle_help()
            elif user_input == ord("p"): view.next_number()
            elif user_input == ord("u"):
                datum.remove_annotation(view.pos, view.ref)
            elif user_input in [ord('s'), ord('b'), ord('r')]:
                datum.modify_annotation(view.pos, view.ref, chr(user_input))
            elif user_input == ord("/"):
                # If we can get another file, do
                datum.write_out()
                if cfilename < len(filenames) -1:
                    cfilename += 1
                    datum = Datum(filenames[cfilename], config)
                    view.datum = datum

                    # Reset, but do not rename as we want the view to have the
                    # same objects still
                    view.pos = [0, 0]
                else:
                    at_end = 'end'
            elif user_input == ord("\\"):
                # If we can go earlier, do
                datum.write_out()
                if cfilename > 0:
                    cfilename -= 1
                    datum = Datum(filenames[cfilename], config)
                    view.datum = datum

                    # Reset, but do not rename as we want the view to have the
                    # same objects still
                    view.pos = [0, 0]
                else:
                    at_end = 'start'
            elif user_input == ord("q"): break
        else:
            # Draw screen
            view.render_edgecase(at_end)
            # Get input
            user_input = window.getch()
            if at_end == 'start' and user_input == ord("/"):
                at_end = None
            elif at_end == 'end' and user_input == ord("\\"):
                at_end = None
            elif user_input == ord("q"): break

        window.clear()

    print('\n'.join(filenames[cfilename:]), file=out)
    out.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A tool for annotating text data with extra information.')
    parser.add_argument('data', help='File containing a list of files to annotate')
    parser.add_argument('--output', help='File containing a list of files to annotate', choices=['overwrite', 'inline', 'standoff'], default="overwrite")
    parser.add_argument('--log_prefix', help='Prefix for logging files (otherwise none)')
    args = parser.parse_args()

    ### Start interface
    filenames = read_filenames(args.data)
    config = get_default_config(args)
    curses.wrapper(annotate, config, filenames)
