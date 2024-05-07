#! /bin/bash
pipx install poetry
poetry shell
poetry install 
poetry build
pipx install dist/depbot-0.5.0.tar.gz
scraper --all