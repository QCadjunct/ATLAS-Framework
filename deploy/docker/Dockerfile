# ATLAS Framework - Production Dockerfile
# Multi-stage build for optimized production container

# ============================================================================
# Build Stage - Install dependencies and build application
# ============================================================================

FROM python:3.11-slim as builder

# Set build arguments
ARG POETRY_VERSION=1.7.1
ARG BUILDPLATFORM
ARG TARGETPLATFORM

# Set environment variables for build
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Install system dependencies required for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==$POETRY_VERSION

# Create application directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Configure Poetry and install dependencies
RUN poetry config virtualenvs.create true \
    && poetry install --only=main --no-root \
    && rm -rf $POETRY_CACHE_DIR

# Copy source code
COPY src/ ./src/
COPY README.md LICENSE ./

# Install the application
RUN poetry install --only=main

# ============================================================================
# Runtime Stage - Create minimal production image
# ============================================================================

FROM python:3.11-slim as runtime

# Set runtime arguments
ARG APP_VERSION=latest
ARG BUILD_DATE
ARG VCS_REF

# Add metadata labels
LABEL org.opencontainers.image.title="ATLAS Framework" \
      org.opencontainers.image.description="Agentic Taxonomy Learning and Synthesis Framework" \
      org.opencontainers.image.version="$APP_VERSION" \
      org.opencontainers.image.created="$BUILD_DATE" \
      org.opencontainers.image.revision="$VCS_REF" \
      org.opencontainers.image.vendor="ATLAS Framework Team" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.source="https://github.com/atlas-framework/atlas" \
      org.opencontainers.image.documentation="https://atlas-framework.github.io/atlas/"

# Set runtime environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    ATLAS_ENV=production \
    ATLAS_LOG_LEVEL=INFO \
    ATLAS_CONFIG_PATH=/app/config/atlas.json

# Install runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Required for Neo4j driver
    libssl3 \
    # Required for networking
    ca-certificates \
    # Required for Tailscale (if used)
    iptables \
    # Utilities
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd --gid 1000 atlas \
    && useradd --uid 1000 --gid atlas --shell /bin/bash --create-home atlas

# Create application directories
RUN mkdir -p /app/config /app/data /app/logs /app/cache \
    && chown -R atlas:atlas /app

# Copy virtual environment from builder
COPY --from=builder --chown=atlas:atlas /app/.venv /app/.venv

# Copy application code from builder
COPY --from=builder --chown=atlas:atlas /app/src /app/src
COPY --from=builder --chown=atlas:atlas /app/README.md /app/LICENSE /app/

# Copy configuration files
COPY --chown=atlas:atlas docker/config/ /app/config/
COPY --chown=atlas:atlas docker/scripts/ /app/scripts/

# Make scripts executable
RUN chmod +x /app/scripts/*.sh

# Switch to non-root user
USER atlas

# Set working directory
WORKDIR /app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import atlas; print('ATLAS Framework is healthy')" || exit 1

# Expose ports
EXPOSE 8000 8001

# Set default command
CMD ["/app/scripts/start.sh"]

# ============================================================================
# Development Stage - Extended image for development
# ============================================================================

FROM runtime as development

# Switch back to root for development setup
USER root

# Install development dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Development tools
    vim \
    less \
    htop \
    # Git for development
    git \
    # Network debugging
    netcat-openbsd \
    telnet \
    # Process debugging
    strace \
    && rm -rf /var/lib/apt/lists/*

# Copy development virtual environment from builder
COPY --from=builder --chown=atlas:atlas /app/.venv /app/.venv

# Install development dependencies
RUN /app/.venv/bin/pip install \
    ipython \
    jupyter \
    pytest \
    pytest-cov \
    black \
    isort \
    flake8 \
    mypy

# Copy development configuration
COPY --chown=atlas:atlas docker/config/development/ /app/config/

# Create development directories
RUN mkdir -p /app/notebooks /app/experiments \
    && chown -R atlas:atlas /app/notebooks /app/experiments

# Switch back to atlas user
USER atlas

# Set development environment
ENV ATLAS_ENV=development \
    ATLAS_LOG_LEVEL=DEBUG

# Development command
CMD ["/app/scripts/start-dev.sh"]

# ============================================================================
# Testing Stage - Image for running tests
# ============================================================================

FROM development as testing

# Switch to root for test setup
USER root

# Install additional testing dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # For integration tests
    redis-tools \
    # For Neo4j tests
    cypher-shell \
    && rm -rf /var/lib/apt/lists/*

# Copy test files
COPY --chown=atlas:atlas tests/ /app/tests/
COPY --chown=atlas:atlas pytest.ini /app/

# Switch back to atlas user
USER atlas

# Set testing environment
ENV ATLAS_ENV=testing \
    ATLAS_LOG_LEVEL=DEBUG \
    PYTEST_CURRENT_TEST=""

# Test command
CMD ["/app/scripts/run-tests.sh"]

# ============================================================================
# Production Optimized Stage - Minimal production image
# ============================================================================

FROM runtime as production

# Additional production optimizations
USER root

# Remove unnecessary packages and clean up
RUN apt-get autoremove -y \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/*

# Optimize Python bytecode
RUN python -m compileall /app/src/

# Set production security settings
RUN echo "atlas ALL=(ALL) NOPASSWD: /app/scripts/health-check.sh" >> /etc/sudoers

# Switch back to atlas user
USER atlas

# Production environment settings
ENV ATLAS_ENV=production \
    ATLAS_LOG_LEVEL=INFO \
    ATLAS_METRICS_ENABLED=true \
    ATLAS_SECURITY_ENABLED=true

# Production startup command
CMD ["/app/scripts/start-production.sh"]

