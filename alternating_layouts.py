#!/usr/bin/env python

import json
import subprocess
import getopt
import sys
import os


def set_layout(node):
    """
        Set the layout/split for the currently
        focused window to either vertical or
        horizontal, depending on its width/height
    """
    height = node['rect']['height']
    width = node['rect']['width']

    if height > width:
        sway_set_split(node["id"], "splitv")
    else:
        sway_set_split(node["id"], "splith")


def sway_set_split(con_id, split):
    """
    Sends the split layout msg to sway
    """
    cmd = '[con_id="{}"] {}'.format(con_id, split)
    process = subprocess.Popen(
        ['swaymsg', cmd],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return True
#
#
# def print_help():
#     print("Usage: " + sys.argv[0] + " [-p path/to/pid.file]")
#     print("")
#     print("Options:")
#     print("    -p path/to/pid.file   Saves the PID for this program in the filename specified")
#     print("")


def get_sway_tree():
    """
    returns the sway tree
    """
    process = subprocess.Popen(
        ['swaymsg', '-t', 'get_tree'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return json.loads(process.stdout.read())

def traverse_sway_tree(json_tree, finder):
    # First check for root node
    if isinstance(json_tree, dict) and json_tree.get("id") == 1:
        return traverse_sway_tree(json_tree["nodes"], finder)
    else:
        for subnode in json_tree:
            ret = finder(subnode)
            if ret:
                return ret
            else:
                if subnode.get("nodes"):
                    ret = traverse_sway_tree(subnode["nodes"], finder)
                    if ret:
                        return ret
                    else:
                        continue
        return False

def get_focused_node(json_tree):
    if json_tree.get("focused"):
        return json_tree
    else:
        return False


def is_focused_id(json_tree):
    if json_tree.get("focused"):
        return json_tree["id"]
    else:
        return False


def switch_layout():
    process = subprocess.Popen(
        ['swaymsg', '-t', 'command', '"splitv"'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


def main():
    """
        Main function - listen for window focus
        changes and call set_layout when focus
        changes
    """

    # subscribe to window changes
    process = subprocess.Popen(
        ['swaymsg', '-t', 'subscribe', '-m',  '["window"]'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    for line in process.stdout:
        tree = get_sway_tree()
        focused_node = traverse_sway_tree(tree, get_focused_node)
        set_layout(focused_node)


if __name__ == "__main__":
    main()
