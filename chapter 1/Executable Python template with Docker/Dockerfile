# Image
FROM python:alpine

# Display the Python output through the terminal
ENV PYTHONUNBUFFERED: 1

# Set work directory
WORKDIR /usr/src/app

# Add applications
## Bash
RUN apk add --no-cache bash

# Add Python dependencies
## Update pip
RUN  pip install --upgrade pip
## Copy requirements
COPY requirements.txt ./requirements.txt
## Install requirements
RUN pip3 install -r requirements.txt
