install:
	@grep "# Added by st,rt,ct" ~/.bashrc >/dev/null || cat bashrc.shim >> ~/.bashrc
	sudo cp st /usr/bin/st
	sudo cp ct /usr/bin/ct
	sudo cp rt.py /usr/bin/rt