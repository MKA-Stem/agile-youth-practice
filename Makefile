all: deps dev

setup: 
	@if [[ $$(uname) == "Darwin" ]];\
		then make deps.osx;                        \
		else make deps.linux;                      \
	fi
	

setup.osx:
	@echo "--- Installing OSX specific dependencies"
	
	@# Node/npm stuff
	[[ $$(which node) && $$(which npm) ]] || brew install node npm
	-brew upgrade node # Upgrade node and npm, ignore errors if already up to date
	-brew upgrade npm
	
	@# Rethinkdb
	-brew install rethinkdb


setup.linux:
	@echo "--- Installing Linux specific dependencies"
	@# TODO: implement this with apt-get or something

run.db:
	rethinkdb --config-file rethinkdb.conf
