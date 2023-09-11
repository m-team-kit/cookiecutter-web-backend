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
ENTRYPOINT [ "python" ]
CMD [ "-m", "uvicorn", "autoapp:app", "--proxy-headers", "--host", "0.0.0.0" ]

# ================================= TESTING ====================================
FROM production AS testing
USER root

RUN python -m pip install -r requirements-test.txt

USER sid
ENTRYPOINT [ "python" ]
CMD ["-m", "pytest", "-n=auto", "--dist=loadscope", "tests"]

# ================================= DEVELOPMENT ================================
FROM testing AS development
USER root

RUN python -m pip install -r requirements-dev.txt

USER sid
EXPOSE 5678
ENTRYPOINT ["python", "-Xfrozen_modules=off", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client" ]
CMD ["-m", "uvicorn", "autoapp:app", "--reload", "--host", "0.0.0.0" ]
