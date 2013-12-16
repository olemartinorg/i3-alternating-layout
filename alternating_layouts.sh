#!/bin/bash

mypath=$(dirname $0)

xprop -root -spy |
    # We need to read both _NET_ACTIVE_WINDOW and _NET_CLIENT_LIST_STACKING,
    # as the latter is the only event we get when certain applications are
    # involved (at least some Java-applications i use have this problem)
    grep --line-buffered '^_NET_ACTIVE_WINDOW\|^_NET_CLIENT_LIST_STACKING' |
    while read line; do

    $mypath/set_layout.py
done