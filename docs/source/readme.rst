Getting Started
=================

Using Poetry (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Currently, the repo is using
`poetry <https://github.com/python-poetry/poetry>`__ Once that's setup
and you've run

``poetry install``

run

``pre-commit install``

to configure the pre-commit scripts. It might be worth it to

``pre-commit run --all-files``

just to setup the pre-commit environment beforehand and make sure it
doesn't bug out later.

demo can be run by just

``python systems``

or

``poetry run python -m systems``

If you're on VS Code, you should consider using the `**Python Docstring
Generator**
extension <https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring>`__
on the Google docstring configuration. If you prefer other editors,
please make sure your commits follow the current docstring convention.

Using Docker (beta)
~~~~~~~~~~~~~~~~~~~

*Natively only supported on Linux and MacOS - use WSL 2 on Windows*

1. Clone this repository
   ``git clone https://github.com/relectric-car-team/systems``
2. ``cd`` into the ``systems`` folder
3. Run ``docker build .`` and copy the image name from the console as
   shown below ``Successfully built <image name>``
4. Then run the build ``docker build <image name>``

Using Requirements File (not recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`requirements.txt <requirements.txt>`__
