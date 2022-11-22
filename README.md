# st, rt, ct : spawn multiple terminals with preconfigured working dir and command execution, saved into multiple profiles


## Install
The following must be installed first:
* Terminator
* python3
* make (for install process)

Then call
````bash
make install
````

The script prompts for sudo to install binaries in `/usr/bin`

It also append the content of `bashrc.shim` to your `~/.bashrc` to inject `$TERMINATOR_BOOTSTRAP` shims at terminator startup.

The tool stores its data under `~/.config/terminals/...`

## Save existing terminals last command and working dir to a profile

In one terminal, type
````bash
$ ls
$ st my_profile

Saved  session [my_profile], terminal [58097]
  CMD: ls
  PWD: /home/me
(session has now 1 terminals)
````

In another terminal, type
````bash
$ watch ps
$ st my_profile

Saved  session [my_profile], terminal [58019]
  CMD: watch ps
  PWD: /home/me/other/folder/somewhere/else
(session has now 2 terminals)
````

## Restore a full profile with a single command

````bash
$ rt   # Will list saved profiles
ch
my_profile

$ rt my_profile   # Will restore the profile
````
This will open a terminator window splitted with all saved terminals. Terminals will start in the saved working dirs and execute the last saved command

## Clear a profile

````bash
$ ct my_profile

Cleared session [my_profile] with 2 terminals
````
