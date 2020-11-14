PYTHONPATH := $(shell pwd)
BASE_DIR := ./
PKG_NAME := backend
SRC_DIR := $(BASE_DIR)/$(PKG_NAME)/

dev-env:
	pip install pipenv
	pipenv install --dev

requirements:
	pipenv lock
	pipenv lock -r > requirements.txt
	pipenv lock -r --dev > requirements-dev.txt
