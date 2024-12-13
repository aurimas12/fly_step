# Variables
PYTHON = python3
APP = script/ryanair_one_way_cheap.py
VENV = fs_env


# Detect OS
ifeq ($(OS),Windows_NT)
    ACTIVATION=.\$(VENV)\Scripts\activate
else
    ACTIVATION=source $(VENV)/bin/activate
endif


venv:
	@echo "Creates a virtual environment and upgrades pip"
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip


setup: venv
	@echo "Create virtual env and install dependencies"
	$(VENV)/bin/pip install -r requirements.txt


# Default target, single action to instal and run app
all: setup run


run:
	@echo "Run the app"
	$(ACTIVATION) && $(PYTHON) $(APP)
#$(VENV)/bin/$(PYTHON) $(APP)


clean:
	@echo "Cleaning temporary files"
	rm -rf __pycache__ *.pyc *.pyo

clean_venv:
	@echo "Delete virtual env"
	rm -rf $(VENV)


help:
	@echo "Usage:"
	@echo "  make venv        - Creates a virtual environment and upgrades pip"
	@echo "  make setup       - Creates a virtual environment and Install dependencies"
	@echo "  make all         - single action to instal and run app"
	@echo "  make run         - Executes the app using the virtual environment"
	@echo "  make clean       - Clean up files"
	@echo "  make clean_venv  - Delete virtual env"
