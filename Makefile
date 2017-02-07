SHELL := /usr/bin/env bash

all: deps dev


setup: 
	@if [[ $$(uname) == "Darwin" ]];\
		then make setup.osx;                        \
		else make setup.linux;                      \
	fi
	

setup.osx:
	@echo "--- Installing OSX specific dependencies"
	
	@# Node/npm stuff
	[[ $$(which node) && $$(which npm) ]] || brew install node npm
	-brew upgrade node # Upgrade node and npm, ignore errors if already up to date
	-brew upgrade npm

	@# Python stuff
	-brew install python3
	-brew upgrade python3
	
	@# Rethinkdb
	-brew install rethinkdb


setup.linux:
	@echo "--- Installing Linux specific dependencies"
	sudo apt -y update
	[[ $$(which node) && $$(which npm) ]] || sudo apt -y install nodejs-legacy
	

	@# Rethinkdb
	@# Copypasta from https://www.rethinkdb.com/docs/install/ubuntu/
	source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $$DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
	wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
	sudo apt -y update
	sudo apt -y install rethinkdb

	@# Python3
	sudo apt -y install python3

	@# Updates and stuff
	sudo apt -y upgrade nodejs-legacy python3


run.db:
	rethinkdb --config-file rethinkdb.conf

run.server:
	python3 server.py
