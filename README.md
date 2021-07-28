<img alt="Docker" src="https://img.shields.io/badge/Docker-2496ed.svg?&style=for-the-badge&logo=docker&logoColor=white"/> <img alt="Python" src="https://img.shields.io/badge/python-3776AB.svg?&style=for-the-badge&logo=python&logoColor=white"/> <img alt="ZeroMQ" src="https://img.shields.io/badge/ZeroMQ-DF0000.svg?&style=for-the-badge&logo=zeromq&logoColor=white"/>
<img alt="yapf" src="https://img.shields.io/badge/code%20style-yapf-blue?style=for-the-badge"/>
<img alt="precommit" src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge&logo=pre-commit&logoColor=white"/>

# Relectric Systems

Source code behind the development of the system architecture for our first electric car conversion. This code will allow us to connect our [User Interface](https://github.com/relectric-car-team/user-interface) to our hardware interfaces such as [CANBUS](https://github.com/relectric-car-team/canbus-mcu-base).

The code base is currently based off this [architecture and data flow diagram](docs/images/architecure.png).

## Lint Status
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/relectric-car-team/systems/master.svg)](https://results.pre-commit.ci/latest/github/relectric-car-team/systems/master)


## Getting Started

### Using Poetry (recommended)

Currently, the repo is using [poetry](https://github.com/python-poetry/poetry)
Once that's setup and you've run

`poetry install`

run

`pre-commit install`

to configure the pre-commit scripts. It might be worth it to

`pre-commit run --all-files`

just to setup the pre-commit environment beforehand and make sure it doesn't bug out later.

demo can be run by just

`python -m systems`

or

`poetry run python -m systems`

If you're on VS Code, you should consider using the [__Python Docstring Generator__ extension](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring) on the Google docstring configuration. If you prefer other editors, please make sure your commits follow the current docstring convention.

### Windows Installation

Install [pyenv-win](https://github.com/pyenv-win/pyenv-win) to easily switch between Python versions. From pyenv, install python 3.9.1 and set it as the Python verion of the current repo.

Once pyenv is setup, install [poetry](https://github.com/python-poetry/poetry#installation), change directory in your
terminal towards the project folder and run the following command

`poetry shell`

to run a virtual enviroment, then

`poetry install`

after that, run the following command to install pre-commit scripts

`pre-commit install`

finally, run the demo by just entering this command

`python -m systems`

or

`poetry run python -m systems`

### Using Docker (beta)

*Natively only supported on Linux and MacOS - use WSL 2 on Windows*

1. Clone this repository `git clone https://github.com/relectric-car-team/systems`
2. `cd` into the `systems` folder
3. Run `docker build .` and copy the image name from the console as shown below
   ```
   Successfully built <image name>
   ```
4. Then run the build `docker build <image name>`

### Using Requirements File (not recommended)

[requirements.txt](requirements.txt)

## Contributing

Please use semantic commit messages and branch naming conventions using this guide. Private branches should be named using the semantic/name/purpose convention. For example: docs/ratik/update-readme signifies that Ratik is responsible for this documentation change and the purpose of the branch is to update the README. Please base all pull requests off of the main branch as they will be rebase merged. The linear history requirement is enforced on main.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
