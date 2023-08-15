ARG  PYTHON_VERSION=latest
FROM python:${PYTHON_VERSION}

# Environments to reduce size of docker image
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100
ENV POETRY_VERSION=1.5.1

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

# Use virtual environment till this issue is fixed:
# https://github.com/python-poetry/poetry/issues/6459
ENV VIRTUAL_ENV=/opt/venv PATH="/opt/venv/bin:$PATH"
RUN python -m venv $VIRTUAL_ENV

# Project initialization:
ARG INSTALL_DEV=false
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi \
    $(test $INSTALL_DEV && echo "--only main")

# Copy all files into the image
COPY . /app

# Final environment variables
ENV PYTHONPATH=/app

# Configure container startup
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
