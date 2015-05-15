#!/usr/bin/env python

import i3
import re
import subprocess


def find_parent(window_id):
    """
        Find the parent of a given window id
    """
    root_window = i3.get_tree()
    result = [None]

    def finder(n, p=None):
        if result[0] is not None:
            return
        for node in n:
            if node['id'] == window_id:
                result[0] = p
                return
            if len(node['nodes']):
                finder(node['nodes'], node)

    finder(root_window['nodes'])
    return result[0]


def set_layout():
    """
        Set the layout/split for the currently
        focused window to either vertical or
        horizontal, depending on its width/height
    """
    current_win = i3.filter(nodes=[], focused=True)
    for win in current_win:
        parent = find_parent(win['id'])

        if parent and "rect" in parent and parent['layout'] != 'tabbed':
            height = parent['rect']['height']
            width = parent['rect']['width']

            if height > width:
                new_layout = 'vertical'
            else:
                new_layout = 'horizontal'

            i3.split(new_layout)


def main():
    """
        Main function - listen for window focus
        changes and call set_layout when focus
        changes
    """
    process = subprocess.Popen(
        ['xprop', '-root', '-spy'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    regex = re.compile(b'^_NET_CLIENT_LIST_STACKING|^_NET_ACTIVE_WINDOW')
    while True:
        line = process.stdout.readline()
        if regex.match(line):
            set_layout()

if __name__ == "__main__":
    main()
