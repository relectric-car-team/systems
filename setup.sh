# !/bin/sh

if ! [ -x "$(command -v poetry)" ]; then
    echo "bruh install poetry then come back"
    exit 1
else
    poetry install
    pre-commit install
    echo "this one might take some time for initial setup"
    pre-commit run --all-files
    echo "setup completed"
    exit 0
fi