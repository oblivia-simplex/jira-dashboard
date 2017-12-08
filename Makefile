PYTHON = python3

dashboard:	libdash/*  bin/*
	$(PYTHON) setup.py install
	cp bin/* ~/bin/

clean:
	rm -rf build/ dist/ *egg-info
