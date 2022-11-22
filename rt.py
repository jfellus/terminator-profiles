#!/usr/bin/env python3
from uuid import uuid4
import re
from os import listdir
import os
from sys import argv

DIR = os.environ["HOME"] + "/.config/terminals/"

if len(argv) <= 1:
    print("\n".join(listdir(DIR)))
    exit(0)

UUID4 = uuid4()

OUT = f"""[global_config]
  window_state = maximise
[keybindings]
[profiles]
  [[default]]
    cursor_color = "#aaaaaa"
[layouts]
  [[default]]
    [[[window0]]]
      type = Window
      parent = ""
      fullscreen = False
      size = 2560, 1391
      title = {argv[1]}
      last_active_term = {UUID4}
      last_active_window = True
    [[[child1]]]
      type = Terminal
      parent = window0
      profile = default
      uuid = {UUID4}
"""

try:
    terminals = [t for t in listdir(DIR + "/" + argv[1]) if not t.startswith(".")]
except:
    print("No such session: " + argv[1])
    exit(1)

OUT += (
    "  "
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
    global i, OUT, UUID4
    TERMINATOR_BOOTSTRAP = f"{DIR}{argv[1]}/{t}"
    OUT += f"""
    [[[terminal{i}]]]
      type = Terminal
      parent = {parent}
      profile = default
      order = {order}
      command = "bash -c 'TERMINATOR_BOOTSTRAP={TERMINATOR_BOOTSTRAP} exec bash'"
      uuid = {UUID4}
    """
    UUID4 = uuid4()
    i += 1


def write_split(parent, vertical, t, order=0):
    global i, OUT
    p = f"child{i}"
    OUT += f"""
    [[[{p}]]]
      type = {'VPaned' if vertical else 'HPaned'}
      parent = {parent}
      order = {order}
      position = 800
      ratio = 0.5
    """

    i += 1

    l = t[: len(t) // 2]
    r = t[len(t) // 2 :]
    if len(l) == 0:
        raise ValueError()
    elif len(l) == 1:
        write_terminal(p, l[0], order=0)
    else:
        write_split(p, not vertical, l, order=0)
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

OUT += """
[plugins]
"""

with open(f"{os.environ['HOME']}/.config/terminator/config", "w") as f:
    print(re.sub(r"\n\s+\n", "\n", OUT, flags=re.M), file=f)
with open(f"{DIR}{argv[1]}/.conf", "w") as f:
    print(re.sub(r"\n\s+\n", "\n", OUT, flags=re.M), file=f)


os.system(f"terminator -l {argv[1]}")
