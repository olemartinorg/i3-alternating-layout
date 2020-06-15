i3-alternating-layout
=====================

Scripts to open new windows in i3wm using alternating layouts (splith/splitv) for each new window. These scripts were made for [/u/ke7ofi](http://www.reddit.com/user/ke7ofi) after she/he asked a question on how to do this [you can read the question here](http://www.reddit.com/r/i3wm/comments/1sdc39/alternating_horizontal_and_vertical_splitting/).

Installation
------------
### Ubuntu

```
sudo apt-get install python3-pip git
pip3 install i3ipc
git clone https://github.com/olemartinorg/i3-alternating-layout
```
And add `alternating_layouts.py` to your `~/.i3/config` autostart:
```
exec --no-startup-id /path/to/alternating_layouts.py
```
### Arch Linux
Install `python-i3ipc`, then add
```
exec --no-startup-id /path/to/alternating_layouts.py
```
to your `~/.i3/config`.


Screenshot
----------

Using regular i3, creating a window layout like this would involve a lot of `$mod+Return`, `$mod+h` and `$mod+v`. Using this script, you only need to open a bunch of new windows!

![Screenshot](https://github.com/olemartinorg/i3-alternating-layout/raw/master/screenshot.png "Screenshot (1920x1080)")
