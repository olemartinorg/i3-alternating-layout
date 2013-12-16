#!/usr/bin/env python

import i3


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

if __name__ == "__main__":
    current_win = i3.filter(nodes=[], focused=True)
    for win in current_win:
        parent = find_parent(win['id'])

        if parent and "last_split_layout" in parent:
            layout = parent['last_split_layout']
            if layout == 'splith':
                new_layout = 'vertical'
            else:
                new_layout = 'horizontal'

            i3.split(new_layout)
