# ================================== BUILDER ===================================
ARG  PYTHON_VERSION=latest
FROM python:${PYTHON_VERSION} as builder

# Environments to reduce size of docker image
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONFAULTHANDLER=true
ENV PYTHONUNBUFFERED=true
ENV PYTHONHASHSEED=random
ENV PIP_NO_CACHE_DIR=true
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

# Install system updates and tools
RUN apt-get update 

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY . /app/
RUN python -m pip install --upgrade pip

# Add user so does not run as root
RUN useradd -m sid
RUN chown -R sid:sid /app

# ================================= PRODUCTION =================================
FROM builder AS production

RUN python -m pip install -r requirements.txt

USER sid
EXPOSE 8000
CMD ["uvicorn", "autoapp:app", "--proxy-headers", "--host", "0.0.0.0"]

# ================================= TESTING ====================================
FROM production AS testing
USER root

# Install postgresql for testing
RUN apt-get install -y --no-install-recommends \
    # Install system updates and tools
    postgresql && \
    # Clean up & back to dialog front end
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install -r requirements-test.txt

USER sid
CMD ["python", "-m", "pytest", "tests"]

# ================================= DEVELOPMENT ================================
FROM testing AS development
USER root

RUN python -m pip install -r requirements-dev.txt

USER sid
EXPOSE 5678
CMD ["python", "-Xfrozen_modules=off", \
    "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", \
    "-m", "uvicorn", "autoapp:app", "--reload", "--host", "0.0.0.0" \
    ]
