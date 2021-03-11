# Relectric Systems

## Setup

Currently, the repo is using [poetry](https://github.com/python-poetry/poetry), so if you can definitely set it up. If poetry isn't the move for you, def feel free to install regularly through [requirements.txt](requirements.txt).

Once that's setup and you've run

`poetry install`

run

`pre-commit install`

to configure the pre-commit scripts. It might be worth it to

`pre-commit run --all-files`

just to setup the pre-commit environment beforehand and make sure it doesn't bug out later.

demo can be run by just

`python systems`

or

`poetry run python -m systems`

If you're on VS Code, I also have the docstrings through the [__Python Docstring Generator__ extension](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring) on the Google docstring configuration. (we can definitely change the format if you guys want i just think the google config looks beautiful). If you're on some other editor then rip.

## systems/core

[architecture diagram](architecture.drawio)
