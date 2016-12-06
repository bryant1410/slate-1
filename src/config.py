from __future__ import print_function

import curses

class KeyConfig(object):
    def __init__(self, key, label, color=2, start='{', end='}'):
        self.key = key
        self.label = label
        self.color = color
        self.start_mark = start
        self.end_mark = end

    def start(self, token, length=-1):
        ans = self.start_mark
        if length < 0:
            ans += self.label
        elif length > 0:
            ans += self.label[:length+1]
        ans += token
        return ans, self.color

    def end(self, token, length=-1):
        ans = token
        if length < 0:
            ans += self.label
        elif length > 0:
            ans += self.label[:length+1]
        ans += self.end_mark
        return ans, self.color

    def start_and_end(self, token, length=-1):
        ans = self.start_mark
        if length < 0:
            ans += self.label
        elif length > 0:
            ans += self.label[:length+1]

        ans += token

        if length < 0:
            ans += self.label
        elif length > 0:
            ans += self.label[:length+1]
        ans += self.end_mark
        return ans, self.color

class Config(object):
    def __init__(self, keys, min_unique_length=-1, overwrite=False):
        self.keys = keys
        self.unique_length = min_unique_length
        self.overwrite = overwrite

    def set_by_file(self, filename):
        self.keys = {}
        for line in open(filename):
            parts = line.strip().split()

            label = parts[0]

            # Default is to numerically assign keys in order, starting at 1
            key = str(len(self.keys) + 1)
            if len(parts) > 1:
                key = parts[1]
            if len(key) > 1:
                raise Exception("This key is too long: "+ key)
            if key in SPECIAL_KEYS:
                raise Exception("This key is a reserved value: "+ key)

            start = '{'
            if len(parts) > 2:
                start = parts[2]
            end = '}'
            if len(parts) > 3:
                end = parts[3]

            color = 0
            if len(parts) > 4:
                # TODO
                pass

            config = KeyConfig(key, label, color, start, end)

        # Find the shortest length at which prefixes of the labels are unique
        self.unique_length = -1
        for i in range(1, min(len(self.keys[key]) for key in self.keys)):
            done = True
            seen = set()
            for key in self.keys:
                start = self.keys[key][:i+1]
                if start in seen:
                    done = False
                    break
                seen.add(start)
            if done:
                self.unique_length = i
                break

DEFAULT_CONFIG = Config(
    {
        's': KeyConfig('s', 'SELL', 2, '{', '}'),
        'b': KeyConfig('b', 'BUY', 3, '[', ']'),
        'r': KeyConfig('r', 'RATE', 7, '|', '|'),
    },
    0
)

SPECIAL_KEYS = {'u', 'q', 'h', 'p', 'n'}
COLORS = [
    # Color combinations, (ID#, foreground, background)
    (1, curses.COLOR_BLUE, curses.COLOR_WHITE),
    (2, curses.COLOR_GREEN, curses.COLOR_BLACK),
    (3, curses.COLOR_YELLOW, curses.COLOR_BLACK),
    (4, curses.COLOR_WHITE, curses.COLOR_BLACK),
    (5, curses.COLOR_BLACK, curses.COLOR_WHITE),
    (6, curses.COLOR_CYAN, curses.COLOR_BLACK),
    (7, curses.COLOR_MAGENTA, curses.COLOR_BLACK),
]
OVERLAP_COLOR = 6
DEFAULT_COLOR = 4
CURSOR_COLOR = 1
HELP_COLOR = 5

def read_config(filename):
    # TODO: this is a stub, actually implement reading a config
    keys = DEFAULT_CONFIG.keys
    unique_length = 0
    overwrite = True
    return Config(keys, unique_length, overwrite)
