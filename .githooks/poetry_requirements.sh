#!/bin/sh

if [ -x "$(command -v poetry)" ]; then
    poetry install
    poetry export -f requirements.txt --output requirements.txt --without-hashes
else
    echo "bruh get poetry"
fi

exit 0
