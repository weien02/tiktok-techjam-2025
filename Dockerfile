# Base image with CUDA for GPU support
FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Install Python 3.11 and common tools
RUN apt-get update && apt-get install -y \
    python3.11 python3.11-venv python3.11-dev python3-pip \
    git curl build-essential && \
    rm -rf /var/lib/apt/lists/*

# Make python3.11 the default for both python3 and python
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Upgrade pip for the default Python
RUN python3 -m pip install --upgrade pip

# Copy requirements and install stable versions
COPY requirements.txt .
RUN python3.11 -m pip install --no-cache-dir -r requirements.txt

# Set working directory to /workspace
WORKDIR /workspace

EXPOSE 8000

# Default command: open bash
CMD ["/bin/bash"]