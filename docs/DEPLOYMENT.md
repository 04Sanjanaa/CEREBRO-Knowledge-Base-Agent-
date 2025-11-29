# KB-Agent Deployment Guide

Guide for deploying KB-Agent to production environments.

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Configuration](#environment-configuration)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Production Best Practices](#production-best-practices)
6. [Monitoring and Maintenance](#monitoring-and-maintenance)

---

## Pre-Deployment Checklist

- [ ] Code tested locally
- [ ] All environment variables configured
- [ ] Secret keys changed from defaults
- [ ] Error logging enabled
- [ ] Performance tested with production data
- [ ] Security reviewed (dependencies, permissions)
- [ ] Backups configured
- [ ] Monitoring setup
- [ ] Documentation updated
- [ ] Team trained on operations

---

## Environment Configuration

### Production .env File

Create a `.env` file with production settings:

```
# Flask Production Settings
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=<use-a-strong-random-key>

# Frontend
REACT_APP_API_URL=https://your-domain.com/api

# Database
DATABASE_URL=postgresql://user:password@db.example.com/kb_agent
# Or: DATABASE_URL=mysql://user:password@db.example.com/kb_agent

# Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True

# CORS - restrict to your domain
CORS_ORIGINS=https://your-domain.com

# Logging
LOG_LEVEL=WARNING
LOG_FILE=/var/log/kb-agent/app.log

# Search
SEARCH_TOP_K=5
SEARCH_THRESHOLD=0.6
```

### Generate Secure Secret Key

```python
import secrets
print(secrets.token_hex(32))
```

---

## Docker Deployment

### Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create logs directory
RUN mkdir -p logs

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "app.py"]
```

### Frontend Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Build application
COPY . .
RUN npm run build

# Production image
FROM node:18-alpine

WORKDIR /app

# Install serve to run the app
RUN npm install -g serve

# Copy built files from builder
COPY --from=build /app/build ./build

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]
```

### Docker Compose

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: kb_agent
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: kb_agent
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U kb_agent"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Backend API
  backend:
    build: ./backend
    environment:
      FLASK_ENV: production
      DATABASE_URL: postgresql://kb_agent:${DB_PASSWORD}@db:5432/kb_agent
      SECRET_KEY: ${SECRET_KEY}
      CORS_ORIGINS: http://frontend:3000
    ports:
      - "5000:5000"
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./logs:/app/logs
      - ./chroma_db:/app/chroma_db
    restart: unless-stopped

  # Frontend
  frontend:
    build: ./frontend
    environment:
      REACT_APP_API_URL: http://localhost:5000
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - backend
      - frontend
    restart: unless-stopped

volumes:
  postgres_data:
```

### Build and Run with Docker Compose

```bash
# Set environment variables
export DB_PASSWORD=<strong-password>
export SECRET_KEY=<generated-key>

# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Cloud Deployment

### AWS Deployment

#### Option 1: Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize project
eb init kb-agent --platform python-3.9

# Create environment
eb create production

# Deploy
eb deploy

# Open in browser
eb open
```

#### Option 2: EC2 + RDS

1. **Launch EC2 Instance**
   - AMI: Ubuntu Server 22.04 LTS
   - Instance Type: t3.medium (minimum)
   - Security Group: Allow ports 80, 443, 5000

2. **Install Software**
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install python3.9 python3-pip nodejs npm postgresql-client -y
   ```

3. **Configure Application**
   - Clone repository
   - Setup environment variables
   - Install dependencies

4. **Setup Web Server**
   - Use Nginx as reverse proxy
   - Use Gunicorn for WSGI server
   - Use Systemd for process management

### Heroku Deployment

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create kb-agent

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=<generated-key>
heroku config:set DATABASE_URL=<postgres-url>

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### Google Cloud Deployment

```bash
# Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Create project
gcloud projects create kb-agent

# Deploy with App Engine
gcloud app deploy

# Deploy with Cloud Run
gcloud run deploy kb-agent --source . --platform managed
```

---

## Production Best Practices

### Security

1. **HTTPS Only**
   - Use SSL/TLS certificates (Let's Encrypt)
   - Force HTTPS redirect
   - Set HSTS header

2. **API Security**
   - Implement rate limiting
   - Add API authentication (JWT/OAuth)
   - Validate all inputs
   - Use security headers

3. **Database Security**
   - Use strong passwords
   - Restrict database access
   - Enable encryption at rest
   - Regular backups with encryption

4. **Secrets Management**
   - Use environment variables
   - Never commit secrets
   - Use secret management service
   - Rotate keys regularly

### Performance

1. **Caching**
   - Implement document caching
   - Cache search results
   - Use Redis for session caching

2. **Database Optimization**
   - Add indexes for frequently searched fields
   - Optimize query performance
   - Use connection pooling

3. **Frontend Optimization**
   - Minify CSS/JS
   - Lazy load components
   - Use CDN for static files
   - Enable gzip compression

### Monitoring

1. **Application Monitoring**
   - Setup error tracking (Sentry)
   - Monitor performance metrics
   - Track API response times

2. **Infrastructure Monitoring**
   - Monitor CPU/Memory usage
   - Monitor disk space
   - Monitor network traffic
   - Setup alerts for thresholds

3. **Logging**
   - Centralize logs (ELK stack, CloudWatch)
   - Log all API requests
   - Log authentication/authorization events
   - Retain logs for compliance period

---

## Nginx Configuration

Create `nginx.conf`:

```nginx
upstream backend {
    server backend:5000;
}

upstream frontend {
    server frontend:3000;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # API routes
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
}
```

---

## Monitoring and Maintenance

### Health Checks

```bash
# API health
curl https://your-domain.com/api/health

# Database connection
# Implement endpoint to check DB
```

### Regular Maintenance

- **Daily**: Monitor error logs
- **Weekly**: Review performance metrics
- **Monthly**: Update dependencies
- **Quarterly**: Security audit
- **Yearly**: Disaster recovery test

### Scaling

As load increases:

1. **Horizontal Scaling**
   - Run multiple backend instances
   - Use load balancer
   - Use stateless session storage

2. **Vertical Scaling**
   - Increase instance size
   - Increase memory allocation
   - Use better performing hardware

3. **Database Scaling**
   - Read replicas
   - Sharding for large datasets
   - Caching layer (Redis)

---

## Backup and Recovery

### Automated Backups

```bash
# PostgreSQL backup
pg_dump kb_agent > backup-$(date +%Y%m%d).sql

# Document storage backup
tar -czf documents-backup-$(date +%Y%m%d).tar.gz ./data/documents/

# Full application backup
tar -czf kb-agent-backup-$(date +%Y%m%d).tar.gz .
```

### Recovery Procedure

1. Restore database from backup
2. Restore document files
3. Verify application health
4. Run migrations if needed
5. Monitor for issues

---

## Rollback Procedure

```bash
# If deployment fails
git revert <commit-hash>
git push

# Docker rollback
docker-compose down
docker-compose up -d
```

---

## Support and Documentation

- Deployment Issues: Check Docker logs and application logs
- Performance Issues: Review monitoring dashboards
- Data Issues: Check backup and recovery procedures

---

## Compliance and Security

- Implement data encryption
- Add audit logging
- GDPR compliance for user data
- Regular penetration testing
- Dependency vulnerability scanning
