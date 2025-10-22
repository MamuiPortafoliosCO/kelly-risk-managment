# RiskOptima Engine Dockerfile
# Multi-stage build for Python/Rust application

# Stage 1: Rust build stage
FROM rust:1.70-slim as rust-builder

# Install required dependencies for Rust compilation
RUN apt-get update && apt-get install -y \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory for Rust
WORKDIR /app

# Copy Rust project files
COPY Cargo.toml Cargo.lock ./
COPY src/lib.rs ./src/

# Build the Rust library
RUN cargo build --release --lib

# Stage 2: Python build stage
FROM python:3.11-slim as python-builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast Python package management
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy Python project files
COPY pyproject.toml uv.lock ./

# Copy the built Rust library
COPY --from=rust-builder /app/target/release/deps/lib*_core*.rlib /tmp/rust-deps/
COPY --from=rust-builder /app/target/release/deps/lib*_core*.rmeta /tmp/rust-deps/

# Install Python dependencies
RUN uv sync --no-install-project

# Copy source code
COPY src/ ./src/

# Build the Python package with Rust extension
RUN uv build

# Stage 3: Runtime stage
FROM python:3.11-slim as runtime

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    # MT5 dependencies (if running on Linux with Wine - optional)
    wine \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash riskoptima

# Set working directory
WORKDIR /app

# Copy built application from builder stage
COPY --from=python-builder /app/dist/*.whl ./
COPY --from=python-builder /app/src/ ./src/

# Install the built wheel
RUN pip install *.whl && rm *.whl

# Copy additional files
COPY README.md ./
COPY example_mt5_data.csv ./

# Create data directories
RUN mkdir -p /app/data /app/logs /app/uploads && \
    chown -R riskoptima:riskoptima /app

# Switch to non-root user
USER riskoptima

# Environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1
ENV RUST_BACKTRACE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import risk_optima_engine; print('Health check passed')" || exit 1

# Expose ports
EXPOSE 8000 8501

# Default command
CMD ["python", "-m", "risk_optima_engine", "full", "--host", "0.0.0.0"]