# !/bin/sh

if ! [ -x "$(command -v poetry)" ]; then
    echo "Please see README instructions for Getting Started"
    exit 1
else
    poetry install
    poetry run pre-commit install
    echo "Setting up pre-commit, this may take a while"
    poetry run pre-commit run --all-files
    echo "Setup completed!"
    exit 0
fi
