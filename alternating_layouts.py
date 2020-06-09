#!/usr/bin/env python3

import getopt
import sys
import os
from i3ipc import Connection, Event


def find_parent(i3, window_id):
    """
        Find the parent of a given window id
    """
    root_window = i3.get_tree()
    result = [None]

    def finder(n, p=None):
        if result[0] is not None:
            return
        for node in n:
            if node.id == window_id:
                result[0] = p
                return
            if len(node.nodes):
                finder(node.nodes, node)

    finder(root_window.nodes)
    return result[0]


def set_layout(i3, e):
    """
        Set the layout/split for the currently
        focused window to either vertical or
        horizontal, depending on its width/height
    """
    win = i3.get_tree().find_focused()
    parent = find_parent(i3, win.id)

    if (parent and parent.layout != 'tabbed'
            and parent.layout != 'stacked'):
        height = win.rect.height
        width = win.rect.width

        if height > width:
            i3.command('split v')
        else:
            i3.command('split h')


def print_help():
    print("Usage: " + sys.argv[0] + " [-p path/to/pid.file]")
    print("")
    print("Options:")
    print("    -p path/to/pid.file   Saves the PID for this program in the filename specified")
    print("")


def main():
    """
    Main function - listen for window focus
        changes and call set_layout when focus
        changes
    """
    opt_list, args = getopt.getopt(sys.argv[1:], 'hp:')
    pid_file = None
    for opt in opt_list:
        if opt[0] == "-h":
            print_help()
            sys.exit()
        if opt[0] == "-p":
            pid_file = opt[1]

    if pid_file:
        with open(pid_file, 'w') as f:
            f.write(str(os.getpid()))

    i3 = Connection()
    i3.on(Event.WINDOW_FOCUS, set_layout)
    i3.main()


if __name__ == "__main__":
    main()
