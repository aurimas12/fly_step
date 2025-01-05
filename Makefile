PYTHON = python3.12
APP = script/ryanair_one_way_cheap.py
VENV = fs_env
PIP = $(VENV)/bin/pip
REQUIREMENTS = requirements.txt
RUN_SCHEDULER = script/scripts_scheduler.py


.PHONY: env libs all run run_scheduler clean clean_venv info help


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


run_scheduler:
	@echo "Scheduling to run scripts automatically by time"
	$(VENV)/bin/python $(RUN_SCHEDULER)


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
	@echo to activate environment run command: source $(VENV)/bin/activate
	@echo
	@echo "Main application entry point: $(APP)"
	@echo
	@echo "Run application with scheduler: $(RUN_SCHEDULER)"
	@echo

help:
	@echo "Usage:"
	@echo "  make env           - Creates a virtual environment and upgrades pip"
	@echo "  make libs          - Install dependencies"
	@echo "  make all           - single action to instal virtual venv and Install dependencies"
	@echo "  make run           - Executes the app using the virtual environment"
	@echo "  make clean         - Clean up files"
	@echo "  make clean_venv    - Delete virtual env"
	@echo "  make info          - Display project information"
	@echo "  make run_scheduler - Scheduling to run scripts automatically by time"
	@echo
