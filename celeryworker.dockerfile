ARG  PYTHON_VERSION=latest
FROM python:${PYTHON_VERSION}

# Environments to reduce size of docker image
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100
ENV POETRY_VERSION=1.0.0

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

# Copy all files into the image
COPY . /app

# Final environment variables
ENV C_FORCE_ROOT=1
ENV PYTHONPATH=/app

# Configure Celery worker start up
RUN chmod +x /worker-start.sh
CMD ["bash", "/worker-start.sh"]
