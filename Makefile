PYTHON = python3.12
APP = script/ryanair_one_way_cheap.py
VENV = fs_env
PIP = $(VENV)/bin/pip
REQUIREMENTS = requirements.txt

.PHONY: venv setup all run clean clean_venv info help


env:
	@echo "Creates a virtual environment and upgrades pip"
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip


libs:
	@echo "Install dependencies"
	$(VENV)/bin/pip install -r $(REQUIREMENTS)


all: venv setup


run:
	@echo "Run the app"
	$(VENV)/bin/python $(APP)


clean:
	@echo "Cleaning temporary files"
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete


clean_venv:
	@echo "Delete virtual env"
	rm -rf $(VENV)


info:
	@echo "Project Information:"
	@echo "---------------------"
	@echo "Main project folder name:"
	@echo $(shell basename $(shell pwd))
	@echo
	@echo "Python version:"
	@$(PYTHON) --version
	@echo
	@echo "Pip version:"
	@$(PYTHON) -m pip --version
	@echo
	@echo "Installed dependencies:"
	@$(PIP) list
	@echo
	@echo "Virtual environment location:"
	@echo "$(VENV)"
	@echo
	@echo to activate run command: source $(VENV)/bin/activate
	@echo
	@echo "Main application entry point: $(APP)"


help:
	@echo "Usage:"
	@echo "  make env         - Creates a virtual environment and upgrades pip"
	@echo "  make libs      - Install dependencies"
	@echo "  make all         - single action to instal virtual venv and Install dependencies"
	@echo "  make run         - Executes the app using the virtual environment"
	@echo "  make clean       - Clean up files"
	@echo "  make clean_venv  - Delete virtual env"
	@echo "  make info        - Display project information"
