import sys
import curses

#TODO Add title, border, and spacing settings and defaults
class Window(object):

    def __init__(self,width=80):
        self._width = width
        self._buffer = []
        self._window = curses.initscr()

    def write(self,lines):
        lines = self._pad_lines(lines)
        for i, l in enumerate(lines):
            if i < len(self._buffer):
                if l != self._buffer[i]:
                    self._update_line(i,l)
            else:
                self._update_line(i,l)
        self._buffer = lines
        self._refresh()

    def close(self,print_buffer=True):
        curses.endwin()
        for b in self._buffer:
            print(b)


    def _pad_lines(self,lines):
        for i in range(len(lines),len(self._buffer)):
            lines.append("")
        return lines

    def _update_line(self,index,value):
        value = str(value) + " " * self._width
        self._window.addstr(index, 0, value[0:self._width])

    def _refresh(self):
        self._window.refresh()
