# Installation

This guide will help you install the ATLAS Framework and set up your development environment.

## Prerequisites

Before installing ATLAS Framework, ensure you have the following prerequisites:

- Python 3.10 or higher
- pip (Python package installer)
- Git (optional, for development installation)

For production deployments, you'll also need:

- Docker and Docker Compose (for containerized deployment)
- Kubernetes (for orchestrated deployment)
- Neo4j 5.x (for graph database)
- Redis 7.x (for caching and message queue)

## Installation Options

There are several ways to install ATLAS Framework:

1. [PyPI Installation](#pypi-installation) (recommended for users)
2. [Development Installation](#development-installation) (recommended for contributors)
3. [Docker Installation](#docker-installation) (recommended for production)
4. [Kubernetes Installation](#kubernetes-installation) (recommended for enterprise)

## PyPI Installation

The simplest way to install ATLAS Framework is via pip:

```bash
pip install atlas-framework
```

This will install the latest stable version of ATLAS Framework and all its dependencies.

For a specific version:

```bash
pip install atlas-framework==1.0.0
```

## Development Installation

For development or to contribute to ATLAS Framework, clone the repository and install in development mode:

```bash
# Clone the repository
git clone https://github.com/atlas-framework/atlas.git
cd atlas

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

## Docker Installation

ATLAS Framework provides official Docker images for easy deployment:

```bash
# Pull the latest image
docker pull ghcr.io/atlas-framework/atlas:latest

# Run the container
docker run -p 8000:8000 -p 8001:8001 \
  -v ./config:/app/config \
  -v ./data:/app/data \
  ghcr.io/atlas-framework/atlas:latest
```

For a complete development environment with all services, use Docker Compose:

```bash
# Clone the repository
git clone https://github.com/atlas-framework/atlas.git
cd atlas

# Start all services
docker-compose up -d

# Access the API at http://localhost:8000
# Access the documentation at http://localhost:8001
```

## Kubernetes Installation

For enterprise deployments, ATLAS Framework provides Kubernetes manifests:

```bash
# Clone the repository
git clone https://github.com/atlas-framework/atlas.git
cd atlas

# Apply the base configuration
kubectl apply -k k8s/base

# Or apply environment-specific configuration
kubectl apply -k k8s/overlays/production
```

For more details on Kubernetes deployment, see the [Kubernetes Deployment Guide](../deployment/kubernetes.md).

## Verifying Installation

After installation, verify that ATLAS Framework is working correctly:

```bash
# Check the installed version
atlas --version

# Run a simple test
atlas test

# Start the API server
atlas serve
```

You should see output indicating the version and successful test completion.

## Configuration

After installation, you'll need to configure ATLAS Framework. Create a configuration file at `~/.atlas/config.json` or specify a custom path:

```json
{
  "version": "1.0",
  "metadata": {
    "name": "My ATLAS Configuration",
    "description": "Configuration for my taxonomy project",
    "created": "2025-01-15T10:00:00Z"
  },
  "node_types": {
    "energy_term": {
      "description": "Energy terminology nodes",
      "labels": ["EnergyTerm", "TaxonomyNode"],
      "default_properties": {
        "extraction_confidence": 0.8,
        "validation_status": "pending"
      },
      "required_fields": ["term_name", "definition", "fuel_group"]
    }
  },
  "global_settings": {
    "default_cache_ttl": 300,
    "max_behavior_execution_time": 60,
    "validation_strictness": "medium"
  }
}
```

For more details on configuration options, see the [Configuration Guide](configuration.md).

## Environment Variables

ATLAS Framework uses the following environment variables:

| Variable | Description | Default |
| --- | --- | --- |
| `ATLAS_ENV` | Environment (development, testing, production) | `development` |
| `ATLAS_LOG_LEVEL` | Logging level | `INFO` |
| `ATLAS_CONFIG_PATH` | Path to configuration file | `~/.atlas/config.json` |
| `NEO4J_URI` | URI for Neo4j connection | `bolt://localhost:7687` |
| `NEO4J_USER` | Username for Neo4j connection | `neo4j` |
| `NEO4J_PASSWORD` | Password for Neo4j connection | `password` |
| `REDIS_URL` | URL for Redis connection | `redis://localhost:6379/0` |
| `OPENAI_API_KEY` | API key for OpenAI services | None |
| `TAILSCALE_AUTHKEY` | Auth key for Tailscale VPN | None |

You can set these variables in your environment or in a `.env` file in your project directory.

## Next Steps

Now that you have installed ATLAS Framework, you can:

- Follow the [Quick Start Guide](quick-start.md) to create your first project
- Learn about [Configuration Options](configuration.md)
- Explore [Examples](../examples/basic-usage.md) to see ATLAS Framework in action

## Troubleshooting

### Common Issues

#### Installation Fails with Dependency Error

If installation fails due to dependency conflicts:

```bash
pip install atlas-framework --no-dependencies
pip install -r https://raw.githubusercontent.com/atlas-framework/atlas/main/requirements.txt
```

#### Neo4j Connection Issues

If you encounter Neo4j connection issues:

1. Ensure Neo4j is running: `docker ps | grep neo4j`
2. Check connection parameters: `atlas check-connection --neo4j`
3. Verify credentials in your configuration

#### Permission Denied Errors

If you encounter permission errors:

```bash
# Install with user permissions
pip install --user atlas-framework

# Or use a virtual environment
python -m venv venv
source venv/bin/activate
pip install atlas-framework
```

For more troubleshooting help, see the [FAQ](../community/faq.md) or [open an issue](https://github.com/atlas-framework/atlas/issues/new) on GitHub.

