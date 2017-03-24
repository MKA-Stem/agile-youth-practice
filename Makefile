SHELL := /usr/bin/env bash

all: deps dev

# Env vars for Flask cli
export PYTHONPATH=$$(PYTHONPATH):$(shell pwd)
export FLASK_APP=server
export FLASK_DEBUG=1
export SECRET=581892a3c50014023b30

setup:
	@if which node >/dev/null && which python3 >/dev/null && which rethinkdb >/dev/null ; then \
		echo "Node, python3, rethink already installed"; \
	else \
		if [[ $$(uname) == "Darwin" ]]; \
			then make setup.osx;                        \
			else make setup.linux;                      \
		fi; \
	fi
	
	-which yarn >/dev/null || npm install -g yarn || sudo npm install -g yarn #Sometimes has funky perms, sort of optional
	pip3 install virtualenv
	
	yarn global add webpack webpack-dev-server
	cd client && yarn
	
	@# Setup python env and deps
	-[[ ! -d "venv" ]] && virtualenv venv
	source venv/bin/activate && pip3 install -r requirements.txt


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

db.setup:
	@echo "--- Setting up Database"
	source venv/bin/activate && python -m lib.db

db.start:
	rethinkdb --config-file rethinkdb.conf

dev.server:
	source venv/bin/activate && flask run --port 8081

dev.client:
	cd client && webpack-dev-server

app.start:
	cd client && NODE_ENV="production" webpack -p --progress
	cp client/app/index.html client/dist/index.html
	source venv/bin/activate && flask run --port 8080
