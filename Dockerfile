FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies for YOUR specific needs
RUN apt-get update && apt-get install -y \
    # PostGIS/GIS support (you use django.contrib.gis)
    gdal-bin \
    libgdal-dev \
    # PostgreSQL client
    libpq-dev \
    # Build tools
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python requirements
COPY fayvad_geosolutions/requirements /app/requirements
RUN pip install --upgrade pip
RUN pip install -r /app/requirements/production.txt

# Copy project
COPY . /app/

# Create directories for static and media files
RUN mkdir -p /app/logs && \
    useradd --create-home fayvad && \
    chown -R fayvad:fayvad /app

EXPOSE 8000