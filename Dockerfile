# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9.2-slim-buster as python-base

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
# pip disable cache, don't check version, timeout
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100
# poetry environment variables
ENV POETRY_VERSION=1.1.5
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1

ENV SYSTEMS_HOME="/systems/"
ENV SYSTEMS_WHEEL_PATH="/systems/dist/*.whl"
ENV VENV_PATH="/systems/.venv"
ENV PATH="${POETRY_HOME}/bin:${VENV_PATH}/bin:$PATH"


FROM python-base AS builder-base
RUN apt-get update && apt-get install --no-install-recommends -y curl build-essential
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

WORKDIR $SYSTEMS_HOME
COPY poetry.lock pyproject.toml ./
COPY systems/ systems/
RUN poetry install --no-dev --no-root
RUN poetry build


FROM python-base AS development
WORKDIR $SYSTEMS_HOME
RUN apt-get update && apt-get install -y git gnupg2
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $SYSTEMS_HOME $SYSTEMS_HOME
RUN poetry install
CMD ["bash"]


FROM python-base AS production
COPY --from=builder-base $SYSTEMS_WHEEL_PATH $SYSTEMS_HOME
RUN find systems/*.whl | xargs pip install

CMD ["python", "-m", "systems"]
