# make help - find available targes in the Makefile
.PHONY: help
help:
	@echo " pre-commit           Run pre-commit hooks"
	@echo " unit-test            Run unit tests"
	@echo " run-me           	 Run the project"

# make pre-commit - run pre-commit hooks
.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files

# make unit-test - run unit tests
.PHONY: unit-test
unit-test:
	python -m unittest tests/tests.py

# make run-me - run the project
.PHONY: run-me
run-me:
	python main_project.py --zips data/zips.csv --plans data/plans.csv --slcsp data/slcsp.csv --output data/output.csv
