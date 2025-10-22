# Docker Deployment Guide for RiskOptima Engine

This guide covers containerized deployment options for the RiskOptima Engine using Docker and Docker Compose.

## Table of Contents

- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Deployment Options](#deployment-options)
- [Configuration](#configuration)
- [MT5 Integration in Docker](#mt5-integration-in-docker)
- [Production Deployment](#production-deployment)
- [Troubleshooting](#troubleshooting)
- [Performance Optimization](#performance-optimization)

## Quick Start

### Single Container Deployment

```bash
# Clone the repository
git clone <repository-url>
cd risk-optima-engine

# Build and run
.\scripts\docker-build.ps1

# Or manually:
docker build -t riskoptima-engine .
docker run -p 8000:8000 -p 8501:8501 riskoptima-engine
```

### Multi-Service Deployment

```bash
# Using Docker Compose (recommended)
docker-compose up -d

# Access the application
# Frontend: http://localhost:8501
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Prerequisites

### System Requirements
- **Docker Desktop**: Version 4.0+ recommended
- **RAM**: Minimum 4GB, recommended 8GB+
- **Disk Space**: 5GB+ free space
- **Operating System**: Windows 10/11, macOS, or Linux

### Docker Installation

#### Windows
1. Download Docker Desktop from https://www.docker.com/products/docker-desktop
2. Install and start Docker Desktop
3. Enable WSL 2 backend if prompted

#### macOS
1. Download Docker Desktop for Mac
2. Install and start Docker Desktop
3. Ensure Rosetta 2 is enabled for Apple Silicon Macs

#### Linux
```bash
# Install Docker Engine
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group (optional)
sudo usermod -aG docker $USER
```

## Deployment Options

### 1. Development Deployment

Perfect for local development and testing:

```bash
# Build development image
docker build -t riskoptima-engine:dev -f Dockerfile .

# Run with hot reload and debugging
docker run -p 8000:8000 -p 8501:8501 \
  -v $(pwd)/src:/app/src \
  -e PYTHONUNBUFFERED=1 \
  -e RUST_BACKTRACE=1 \
  riskoptima-engine:dev
```

### 2. Production Deployment

Optimized for production use:

```bash
# Build production image
docker build -t riskoptima-engine:latest \
  --target runtime \
  --build-arg BUILDKIT_INLINE_CACHE=1 .

# Run production container
docker run -d \
  --name riskoptima-engine-prod \
  --restart unless-stopped \
  -p 8000:8000 \
  -p 8501:8501 \
  -v riskoptima_data:/app/data \
  -v riskoptima_logs:/app/logs \
  -e PYTHONUNBUFFERED=1 \
  riskoptima-engine:latest
```

### 3. Docker Compose Deployment

Most comprehensive deployment option:

```yaml
# docker-compose.yml (already provided)
version: '3.8'
services:
  riskoptima-engine:
    build: .
    ports:
      - "8000:8000"
      - "8501:8501"
    volumes:
      - riskoptima_data:/app/data
    restart: unless-stopped
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PYTHONPATH` | `/app/src` | Python module search path |
| `PYTHONUNBUFFERED` | `1` | Disable Python output buffering |
| `RUST_BACKTRACE` | `1` | Enable Rust backtraces |
| `API_HOST` | `0.0.0.0` | API server bind address |
| `API_PORT` | `8000` | API server port |

### Volume Mounts

```bash
# Persistent data storage
-v riskoptima_data:/app/data
-v riskoptima_logs:/app/logs
-v riskoptima_uploads:/app/uploads

# Development mounts
-v $(pwd)/src:/app/src
-v $(pwd)/tests:/app/tests
```

### Resource Limits

```yaml
services:
  riskoptima-engine:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '0.5'
          memory: 1G
```

## MT5 Integration in Docker

### Challenge: MT5 is Windows-only

The official MetaTrader 5 terminal only runs on Windows, creating challenges for Docker deployment:

### Solution 1: Host MT5 Integration (Recommended)

Run RiskOptima Engine in Docker, but connect to host MT5:

```bash
# Windows host with MT5 terminal running
docker run -p 8000:8000 -p 8501:8501 \
  --network host \
  riskoptima-engine

# The container can now connect to MT5 on host via IPC
```

### Solution 2: Wine-based MT5 in Container (Experimental)

Run MT5 terminal inside container using Wine:

```dockerfile
FROM mcr.microsoft.com/windows/servercore:ltsc2022

# Install Wine and MT5
# Note: This is complex and may not work reliably
# MT5 licensing and installation required
```

### Solution 3: Hybrid Architecture

```yaml
version: '3.8'
services:
  riskoptima-engine:
    # Main application
    build: .
    depends_on:
      - mt5-connector

  mt5-connector:
    # Windows service that connects to MT5 and exposes data via API
    image: windows-server-with-mt5
    networks:
      - riskoptima-network
```

### MT5 Connection Configuration

```python
# In mt5_integration.py
MT5_HOST = os.getenv("MT5_HOST", "host.docker.internal")  # Windows host
MT5_PORT = os.getenv("MT5_PORT", "8222")  # Default MT5 port
```

## Production Deployment

### With Nginx Reverse Proxy

```yaml
version: '3.8'
services:
  riskoptima-engine:
    build: .
    expose:
      - "8000"
      - "8501"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - riskoptima-engine
```

### SSL/TLS Configuration

```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 \
  -keyout key.pem -out cert.pem -days 365 -nodes

# Mount certificates
docker run -v $(pwd)/cert.pem:/etc/ssl/certs/cert.pem \
           -v $(pwd)/key.pem:/etc/ssl/private/key.pem \
           your-image
```

### Health Checks and Monitoring

```yaml
services:
  riskoptima-engine:
    healthcheck:
      test: ["CMD", "python", "-c", "import risk_optima_engine; print('OK')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Troubleshooting

### Common Issues

#### 1. Build Failures

**Problem**: Rust compilation fails in Docker
```bash
# Solution: Ensure proper base image
FROM rust:1.70-slim as rust-builder
RUN apt-get update && apt-get install -y pkg-config libssl-dev
```

#### 2. Memory Issues

**Problem**: Container runs out of memory during builds
```bash
# Solution: Increase Docker memory limit
# Docker Desktop > Settings > Resources > Memory
```

#### 3. Port Conflicts

**Problem**: Ports 8000/8501 already in use
```bash
# Solution: Use different ports
docker run -p 8001:8000 -p 8502:8501 riskoptima-engine
```

#### 4. MT5 Connection Issues

**Problem**: Cannot connect to MT5 from container
```bash
# Solution: Use host networking
docker run --network host riskoptima-engine

# Or expose MT5 ports from host
# Windows Firewall > Allow MT5 ports
```

#### 5. File Permission Issues

**Problem**: Permission denied on mounted volumes
```bash
# Solution: Set proper user permissions
RUN useradd --create-home --shell /bin/bash riskoptima
USER riskoptima
```

### Debugging Commands

```bash
# View container logs
docker logs riskoptima-engine

# Access container shell
docker exec -it riskoptima-engine /bin/bash

# Check container resource usage
docker stats riskoptima-engine

# Inspect container configuration
docker inspect riskoptima-engine
```

### Performance Monitoring

```bash
# Monitor container performance
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Check application health
curl http://localhost:8000/health

# View application logs
docker-compose logs -f riskoptima-engine
```

## Performance Optimization

### Build Optimizations

```dockerfile
# Use multi-stage builds
FROM rust:1.70-slim as rust-builder
FROM python:3.11-slim as python-builder
FROM python:3.11-slim as runtime

# Use build cache
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Minimize image size
RUN apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*
```

### Runtime Optimizations

```yaml
services:
  riskoptima-engine:
    environment:
      - PYTHONDONTWRITEBYTECODE=1
      - PYTHONUNBUFFERED=1
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
    restart: unless-stopped
```

### Caching Strategies

```python
# Redis for session caching
import redis

redis_client = redis.Redis(host='redis', port=6379)

# Cache expensive computations
@redis_client.cache(expire=3600)
def expensive_calculation(data):
    return perform_calculation(data)
```

## Security Considerations

### Container Security

```dockerfile
# Use non-root user
RUN useradd --create-home --shell /bin/bash riskoptima
USER riskoptima

# Minimize attack surface
RUN apt-get remove -y curl wget && apt-get autoremove -y

# Use specific base images
FROM python:3.11-slim@sha256:...
```

### Network Security

```yaml
services:
  riskoptima-engine:
    networks:
      - secure-network
    # Don't expose ports directly in production
    # Use reverse proxy instead

networks:
  secure-network:
    driver: bridge
    internal: true  # Isolate from external access
```

### Secret Management

```bash
# Use Docker secrets or environment variables
docker run -e MT5_PASSWORD_FILE=/run/secrets/mt5_password \
           --secret mt5_password riskoptima-engine
```

## Scaling and High Availability

### Horizontal Scaling

```yaml
services:
  riskoptima-engine:
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
    # Load balancer required for multiple instances
```

### Database Integration

```yaml
services:
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=riskoptima
      - POSTGRES_USER=riskoptima
    volumes:
      - postgres_data:/var/lib/postgresql/data

  riskoptima-engine:
    depends_on:
      - postgres
    environment:
      - DATABASE_URL=postgresql://riskoptima:password@postgres/riskoptima
```

## Backup and Recovery

### Data Backup

```bash
# Backup volumes
docker run --rm -v riskoptima_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz -C /data .

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker run --rm -v riskoptima_data:/data -v $(pwd)/backups:/backup \
  alpine tar czf /backup/backup_$DATE.tar.gz -C /data .
```

### Disaster Recovery

```bash
# Restore from backup
docker run --rm -v riskoptima_data:/data -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/backup.tar.gz"

# Recreate containers
docker-compose down
docker-compose up -d
```

## Monitoring and Logging

### Centralized Logging

```yaml
services:
  riskoptima-engine:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  logstash:
    image: docker.elastic.co/logstash/logstash:8.5.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    depends_on:
      - elasticsearch
```

### Health Monitoring

```yaml
services:
  healthcheck:
    image: curlimages/curl
    command: ["--fail", "--silent", "http://riskoptima-engine:8000/health"]
    depends_on:
      - riskoptima-engine
    restart: always
```

This comprehensive Docker deployment guide provides multiple deployment strategies, from simple single-container setups to complex production environments with high availability and monitoring.