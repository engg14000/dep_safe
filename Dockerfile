# Allow custom base image or default to Python official image
ARG BASE_IMAGE=
ARG PYTHON_VERSION=3.11

# Use custom base image if provided, otherwise use official Python image
FROM ${BASE_IMAGE:-python:${PYTHON_VERSION}-slim}

# Install pip and pipdeptree for dependency checking
RUN pip install --upgrade pip pipdeptree

# Copy installation artifacts
COPY requirements.txt .
COPY installer.sh .

# Install Python dependencies and check for conflicts
RUN bash installer.sh

# Cleanup installation artifacts
RUN rm requirements.txt installer.sh

# Set working directory
WORKDIR /app

# Default command to show installed packages
CMD ["pipdeptree", "--warn", "fail"]