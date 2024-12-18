PYTHON = python3
APP = script/ryanair_one_way_cheap.py
VENV = fs_env
PIP = $(VENV)/bin/pip
REQUIREMENTS = requirements.txt


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
	$(VENV)/bin/pip install -r $(REQUIREMENTS)


all: setup run


run:
	@echo "Run the app"
	$(ACTIVATION) && $(PYTHON) $(APP)



clean:
	@echo "Cleaning temporary files"
	rm -rf __pycache__ *.pyc *.pyo

clean_venv:
	@echo "Delete virtual env"
	rm -rf $(VENV)


info:
	@echo "Project Information:"
	@echo "---------------------"
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
	@echo "Main application entry point: $(APP)"


help:
	@echo "Usage:"
	@echo "  make venv        - Creates a virtual environment and upgrades pip"
	@echo "  make setup       - Creates a virtual environment and Install dependencies"
	@echo "  make all         - single action to instal and run app"
	@echo "  make run         - Executes the app using the virtual environment"
	@echo "  make clean       - Clean up files"
	@echo "  make clean_venv  - Delete virtual env"
	@echo "  make info        - Display project information"
