APP = script/ryanair_one_way_cheap.py
PYTHON = $(VENV)/bin/python3
PYTHON_3_12 = python3.12.5
PIP = $(VENV)/bin/pip
REQUIREMENTS = requirements.txt
VENV = .venv
UV = uv

.PHONY: venv setup all run clean del_venv clean info help


ifeq ($(OS),Windows_NT)
    ACTIVATION = .\$(VENV)\Scripts\activate
else
    ACTIVATION = source $(VENV)/bin/activate
endif


venv:
	@echo "Creates a virtual environment"
	$(UV) init
	$(UV) venv --python=$(PYTHON_3_12)


setup:
	@echo "Install dependencies from requirements.txt and sync with uv.lock"
	$(UV) add -r $(REQUIREMENTS)
	$(UV) lock


all: venv setup


run:
	@echo "Run the app"
	$(ACTIVATION) && $(PYTHON) $(APP)


clean:
	@echo "Clean up temporary files"
	$(UV) cache clean
	$(UV) cache dir
	rm -rf __pycache__ *.pyc *.pyo


del_venv:
	@echo "Delete virtual env"
	rm -rf $(VENV)
	rm -rf pyproject.toml
	rm -rf uv.lock


info:
	@echo "Project Information:"
	@echo "---------------------"
	@echo "Main project folder name:"
	@basename $(shell pwd)
	@echo
	@echo "Full project path:"
	@pwd
	@echo
	@echo "Python version:"
	@$(PYTHON) --version
	@echo
	@echo "UV version:"
	@$(UV) version
	@echo
	@echo "Installed dependencies:"
	@$(UV) tree
	@echo
	@echo "Virtual environment location:"
	@echo "$(VENV)"
	@echo
	@echo "Active virtual environment:"
	@echo "$(VIRTUAL_ENV)"
	@echo
	@echo to activate run command: source $(VENV)/bin/activate
	@echo
	@echo "Main application entry point: $(APP)"
	@echo


help:
	@echo "Usage:"
	@echo "  make info        - Display project information"
	@echo "  make venv        - Creates a virtual environment"
	@echo "  make setup       - Update UV and install dependencies"
	@echo "  make all         - single action to setup venv"
	@echo "  make run         - Executes the app using the virtual environment"
	@echo "  make clean       - Clean up files"
	@echo "  make del_venv    - Clean and delete virtual env and files exp: pyproject.toml, uv.lock"
	@echo
