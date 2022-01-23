init:
	pip3 install -e ".[testing]"

test: clean init
	python3 setup.py --verbose test
	python3 -m pylint fixup_chooser/ test/

test-e2e: clean init
	./init-test-repository.sh basic test-basic
	cd tmp/test-basic;fixupChooser --list
	cd tmp/test-basic;fixupChooser --list | sed 's/\x1b\[[0-9;]*m//g' | grep '(1/2) File 4 revised$$'
	cd tmp/test-basic;fixupChooser --list | sed 's/\x1b\[[0-9;]*m//g' | grep '(2/2) File 1 revised2, File 4 revised 5$$'

clean:
	find . -name "__pycache__" | xargs rm -r
