#!/usr/bin/env python3
import re
from os import listdir
import os
from sys import argv

DIR = os.environ["HOME"] + "/.config/terminals/"

if len(argv) <= 1:
    print("\n".join(listdir(DIR)))
    exit(0)

OUT = """
[global_config]
  window_state = maximise
[keybindings]
[profiles]
  [[default]]
    cursor_color = "#aaaaaa"
  [[clickhouse]]
    cursor_color = "#aaaaaa"
[layouts]
  [[default]]
    [[[window0]]]
      type = Window
      parent = ""
    [[[child1]]]
      type = Terminal
      parent = window0
      profile = default
"""

try:
    terminals = [t for t in listdir(DIR + "/" + argv[1]) if not t.startswith(".")]
except:
    print("No such session: " + argv[1])
    exit(1)

OUT += (
    "    "
    + f"""
    [[{argv[1]}]]
      [[[window0]]]
        type = Window
        parent = ""
""".strip()
)

i = 1

print(terminals)


def write_terminal(parent, t, order=0):
    global i, OUT
    TERMINATOR_BOOTSTRAP = f"{DIR}{argv[1]}/{t}"
    OUT += f"""
      [[[child{i}]]]
        type = Terminal
        parent = {parent}
        profile = default
        order = {order}
        command = "bash -c 'TERMINATOR_BOOTSTRAP={TERMINATOR_BOOTSTRAP} exec bash'"
    """
    i += 1


def write_split(parent, vertical, t, order=0):
    global i, OUT
    p = f"child{i}"
    OUT += f"""
      [[[{p}]]]
        type = {'VPaned' if vertical else 'HPaned'}
        parent = {parent}
        order = {order}
    """

    i += 1

    l = t[: len(t) // 2]
    r = t[len(t) // 2 :]
    if len(l) == 0:
        raise ValueError()
    elif len(l) == 1:
        write_terminal(p, l[0], order=0)
    else:
        write_split(p, not vertical, l, order=1)
    if len(r) == 0:
        raise ValueError()
    elif len(r) == 1:
        write_terminal(p, r[0], order=1)
    else:
        write_split(p, not vertical, r, order=1)


if len(terminals) == 1:
    write_terminal("window0", terminals[0])
else:
    write_split("window0", True, terminals)

with open(f"{DIR}{argv[1]}/.conf", "w") as f:
    print(re.sub(r"\n\s+\n", "\n", OUT, flags=re.M), file=f)
