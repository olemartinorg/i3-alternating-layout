#!/usr/bin/env python

import i3
import re
import subprocess
import os

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
            
def toggle_execution():
    """
        If another instance of this script is running,
        exit and terminate all other instances,
        so that the execution of this program acts as a toggle for i.tg
        This way, this script can be keysym-ed directly and the same
        key be used for turning off and on the alternating layout.
        We use a signaling file in /tmp to indicate that another instance is running.
    """
    self_name = os.path.basename(__file__)
    pidfile_dir = "/tmp/" + self_name + ".lock"

    if os.path.isfile(pidfile_dir): # indicator file exists: other instance running

        try:
            pid = eval(open(pidfile_dir).readline()) # get first line from the file; onl$
            os.kill(pid, 15) # signal 15 is SIGTERM

        except (SyntaxError, OSError): # eval fails or kill fails
            print "Malformed lockfile. Please retry running this."

        os.remove(pidfile_dir) # remove the file before exiting
        exit(1)

    else: # indicator file doesn't exist: no other instance
        pidfile = open(pidfile_dir, "w") # create the file
        pidfile.write(str(os.getpid())) # write this PID into it
        pidfile.close()

def main():
    """
        Main function - listen for window focus
        changes and call set_layout when focus
        changes
    """

    toggle_execution()

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
