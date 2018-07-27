.PHONY: help bootstrap test safety requirements

# Path of the virtualenv directory
VENV?=.venv
IN_VENV=. $(VENV)/bin/activate ;
VENV_COMMAND?=pyvenv-3.5

help:
	@echo
	@echo "make bootstrap       -- setup development environment"
	@echo "make test            -- run full test suite"
	@echo "make safety          -- run safety check on packages"
	@echo
	@echo "make requirements    -- only compile the requirements*.txt files"
	@echo "make .venv           -- only (re)install the dev requirements into the virtualenv"
	@echo

bootstrap: $(VENV)
	@# 3. Install pre-commit hook scripts in .git directory
	.venv/bin/pre-commit install
	@# 4. Inform the user about editorconfig.org
	@echo '******************************************************************************'
	@echo "Don't forget to setup your editor to use the config file, see editorconfig.org"
	@echo '******************************************************************************'

test:
	$(IN_VENV) pytest --cov tests

safety:
	$(IN_VENV) safety check -r requirements-dev.txt

requirements: requirements.txt requirements-dev.txt


# Actual files/directories
################################################################################

# Create this directory as a symbolic link to an existing virtualenv, if you want to use that.
$(VENV): requirements-dev.txt
	test -d $(VENV) || $(VENV_COMMAND) $(VENV)
	$(IN_VENV) pip install -r requirements-dev.txt
	touch $(VENV)

# These should only be created when running make requirements, they should not be
# created as a side effect of something else.
requirements.txt: requirements.in
	@test -d $(VENV) || (echo "Virtualenv dir \"$(VENV)\" missing, please create it." && false)
	$(IN_VENV) pip-compile --rebuild requirements.in --output-file $@ > /dev/null

requirements-dev.txt: requirements.in requirements-dev.in
	@test -d $(VENV) || $(VENV_COMMAND) $(VENV)
	$(IN_VENV) pip install pip-tools
	$(IN_VENV) pip-compile --rebuild requirements.in requirements-dev.in --output-file $@ > /dev/null
