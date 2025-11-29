# Docker Deployment Guide

This guide explains how to build and run KB-Agent using Docker and Docker Compose.

## Prerequisites

1. **Docker Desktop** (Windows/Mac): https://www.docker.com/products/docker-desktop
2. **Docker Engine** (Linux): https://docs.docker.com/engine/install/

Verify installation:
```bash
docker --version
docker compose --version
```

## Quick Start

### 1. Build and Start Services

From the project root directory:

```bash
cd /path/to/AI_Agent
docker compose up --build
```

This will:
- Build the backend Flask image (using `backend/Dockerfile`)
- Build the frontend nginx image (using `frontend/Dockerfile`)
- Start both services with automatic restart on failure
- Expose:
  - Backend: `http://localhost:5000`
  - Frontend: `http://localhost:3000`

### 2. Access the Application

**Option A: Backend Web UI (recommended for now)**
```
http://localhost:5000
```
This serves the lightweight static UI (no Node.js required).

**Option B: Info Page**
```
http://localhost:5000/info
```
View all available API endpoints and documentation.

**Option C: React Frontend (after npm build)**
```
http://localhost:3000
```
Only available if the React build succeeds (requires Node.js during build).

### 3. Test the API

```bash
# Health check
curl http://localhost:5000/api/health

# List documents
curl http://localhost:5000/api/documents

# Submit a query
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query":"How much annual leave am I entitled to?"}'

# Check logs
curl http://localhost:5000/api/logs

# Get stats
curl http://localhost:5000/api/stats
```

## Docker Compose Configuration

The `docker-compose.yml` file defines two services:

### Backend Service
- **Image**: Built from `backend/Dockerfile`
- **Port**: 5000
- **Volumes**: 
  - `./backend:/app` (live code reload)
  - `./logs:/app/logs` (persistent logs)
- **Environment**: `FLASK_ENV=production`

### Frontend Service
- **Image**: Built from `frontend/Dockerfile`
- **Port**: 3000 (mapped to 80 internally)
- **Volumes**: 
  - `./frontend:/app:ro` (read-only)
- **Depends On**: backend (waits for backend to start)

## Common Commands

### Start Services
```bash
docker compose up
```

### Start in Background
```bash
docker compose up -d
```

### Stop Services
```bash
docker compose down
```

### View Logs
```bash
# All services
docker compose logs -f

# Backend only
docker compose logs -f kb_agent_backend

# Frontend only
docker compose logs -f kb_agent_frontend
```

### Rebuild Images
```bash
docker compose up --build
```

### Remove Everything (including volumes)
```bash
docker compose down -v
```

## Troubleshooting

### Port Already in Use
If port 5000 or 3000 is already in use:

```bash
# Find process using port
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill process or change port in docker-compose.yml
```

### Backend Container Fails to Start
```bash
# Check logs
docker compose logs kb_agent_backend

# Common issues:
# - Port 5000 already in use
# - Database file permissions
# - Missing Python dependencies
```

### Frontend Build Fails
The frontend uses a multi-stage build:
1. Node.js builds the React app
2. Nginx serves the built files

If Node.js is not available during build:
```bash
# Build backend only
docker build -t kb-agent-backend ./backend
docker run -p 5000:5000 kb-agent-backend
```

### Database Not Persisting
Ensure the `./data` and `./logs` directories exist and are writable:

```bash
mkdir -p data logs
chmod 755 data logs
```

## Production Deployment

For production, consider:

1. **Use a WSGI Server**: Replace Flask's development server with Gunicorn or Waitress.

2. **Environment Variables**: Create a `.env` file:
```
FLASK_ENV=production
SECRET_KEY=your-secure-key
DATABASE_URL=sqlite:///data/kb_agent.db
```

3. **Reverse Proxy**: Use nginx or Apache in front of Flask.

4. **SSL/TLS**: Use Let's Encrypt for HTTPS.

5. **Persistent Volume**: Use Docker volumes for database and logs:
```yaml
volumes:
  kb_data:
  kb_logs:
```

6. **Health Checks**: Add health checks in docker-compose.yml:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## Example Production docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    container_name: kb_agent_backend
    ports:
      - "5000:5000"
    volumes:
      - kb_data:/app/data
      - kb_logs:/app/logs
    environment:
      FLASK_ENV: production
      SECRET_KEY: ${SECRET_KEY}
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build: ./frontend
    container_name: kb_agent_frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: always

volumes:
  kb_data:
  kb_logs:
```

## Multi-Environment Setup

### Development (docker-compose.yml)
- Debug mode enabled
- Live code reloading
- Verbose logging

### Production (docker-compose.prod.yml)
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Further Reading

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Flask Production Deployment](https://flask.palletsprojects.com/en/2.3.x/deployment/)
