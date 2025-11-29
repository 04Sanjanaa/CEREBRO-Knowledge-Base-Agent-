# KB-Agent Setup Guide

Complete step-by-step guide to set up and run KB-Agent.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Backend Setup](#backend-setup)
3. [Frontend Setup](#frontend-setup)
4. [Running the System](#running-the-system)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- 2GB RAM minimum
- 500MB disk space

### Software Requirements

#### Python
- **Version**: 3.9 or higher
- **Download**: https://www.python.org/downloads/
- **Verification**: 
  ```bash
  python --version
  pip --version
  ```

#### Node.js & npm
- **Version**: 16 LTS or higher
- **Download**: https://nodejs.org/
- **Verification**:
  ```bash
  node --version
  npm --version
  ```

#### Git (Optional but recommended)
- **Download**: https://git-scm.com/
- **Verification**:
  ```bash
  git --version
  ```

---

## Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd path/to/AI_Agent/backend
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies installed:
- Flask 2.3.3
- Flask-CORS 4.0.0
- Werkzeug 2.3.7
- python-dotenv 1.0.0

### Step 4: Create Environment File

```bash
cd ..
copy .env.example .env    # Windows
cp .env.example .env      # macOS/Linux
```

Edit `.env` and update configuration if needed:
```
FLASK_ENV=development
FLASK_PORT=5000
FLASK_DEBUG=True
```

### Step 5: Verify Installation

```bash
cd backend
python -c "import flask; print(f'Flask {flask.__version__} installed')"
```

---

## Frontend Setup

### Step 1: Navigate to Frontend Directory

```bash
cd path/to/AI_Agent/frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

This installs:
- React 18.2.0
- React DOM 18.2.0
- Tailwind CSS (via CDN in production)
- Lucide React 0.263.1
- Axios 1.5.0

### Step 3: Verify Installation

```bash
npm list react
npm list axios
```

### Step 4: Build Configuration (Optional)

Create `.env` file in frontend directory:
```
REACT_APP_API_URL=http://localhost:5000
```

---

## Running the System

### Option 1: Two Terminal Windows

**Terminal 1 - Backend:**
```bash
cd path/to/AI_Agent/backend
# Activate virtual environment if created
python app.py
```

Expected output:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

**Terminal 2 - Frontend:**
```bash
cd path/to/AI_Agent/frontend
npm start
```

Expected output:
```
compiled successfully!
You can now view kb-agent-frontend in the browser.
  Local:  http://localhost:3000
```

### Option 2: Background Processes

**Windows (PowerShell):**
```bash
# Terminal 1
Start-Process python "path\to\AI_Agent\backend\app.py"

# Terminal 2
cd path\to\AI_Agent\frontend
npm start
```

**macOS/Linux:**
```bash
# Terminal 1
cd path/to/AI_Agent/backend && python app.py &

# Terminal 2
cd path/to/AI_Agent/frontend && npm start &
```

---

## Verification

### Backend Verification

1. **API Health Check**
   ```bash
   curl http://localhost:5000/api/health
   ```
   
   Expected response:
   ```json
   {"status": "healthy", "timestamp": "..."}
   ```

2. **Get Documents**
   ```bash
   curl http://localhost:5000/api/documents
   ```
   
   Should return 5 sample documents

3. **Test Query**
   ```bash
   curl -X POST http://localhost:5000/api/query \
     -H "Content-Type: application/json" \
     -d '{"query": "annual leave"}'
   ```

### Frontend Verification

1. **Access Application**
   - Open browser and go to `http://localhost:3000`
   - Should see KB-Agent interface with 4 tabs

2. **Test Chat Interface**
   - Type a question in the chat input
   - Click "Send Message" or press Enter
   - Should receive a response with sources

3. **Test Document Browsing**
   - Click "Documents" tab
   - Should list 5 company policy documents
   - Click on a document to view details

4. **Test Query Logs**
   - Click "Query Logs" tab
   - Should show all queries made
   - Can export as JSON or CSV

5. **Test System Info**
   - Click "System Info" tab
   - Should show system statistics and status

---

## Configuration

### Backend Configuration (.env)

```
# Server
FLASK_ENV=development              # development or production
FLASK_DEBUG=True                   # Enable debug mode
FLASK_HOST=0.0.0.0                # Host address
FLASK_PORT=5000                   # Port number

# Frontend
REACT_APP_API_URL=http://localhost:5000

# Database
DATABASE_URL=sqlite:///kb_agent.db

# Search
SEARCH_TOP_K=3                     # Number of results to return
SEARCH_THRESHOLD=0.5               # Minimum relevance score

# Logging
LOG_LEVEL=INFO                     # DEBUG, INFO, WARNING, ERROR
LOG_FILE=./logs/kb_agent.log

# Security (change in production!)
SECRET_KEY=change-this-in-production
```

---

## Troubleshooting

### Backend Issues

#### "ModuleNotFoundError: No module named 'flask'"
```bash
# Ensure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt
```

#### "Port 5000 already in use"
```bash
# Change port in .env
FLASK_PORT=5001

# Or kill process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :5000
kill -9 <PID>
```

#### "CORS errors" when accessing from frontend
- Ensure FLASK_CORS is installed: `pip install flask-cors`
- Check CORS_ORIGINS in .env configuration

### Frontend Issues

#### "npm: command not found"
- Ensure Node.js is installed
- Add Node.js to PATH if needed
- Restart terminal

#### "Port 3000 already in use"
```bash
# Kill process using port 3000
# Windows (PowerShell):
Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess | Stop-Process

# macOS/Linux:
lsof -i :3000
kill -9 <PID>
```

#### "Cannot GET /" error
- Ensure `npm start` is running in frontend directory
- Wait 30 seconds for React to compile
- Check browser console for errors

#### "API calls failing"
- Verify backend is running: `curl http://localhost:5000/api/health`
- Check REACT_APP_API_URL in .env matches backend URL
- Check browser console for CORS errors

### General Issues

#### "Blank page or 404 errors"
1. Clear browser cache (Ctrl+Shift+Delete)
2. Restart both backend and frontend
3. Check console for errors (F12)

#### "Slow performance"
1. Check available disk space
2. Reduce number of indexed documents
3. Increase SEARCH_THRESHOLD to reduce search results
4. Monitor memory usage

#### "Can't connect to localhost"
1. Try `127.0.0.1` instead of `localhost`
2. Disable firewall temporarily to test
3. Check if services are actually running

---

## Development Tips

### Hot Reload
- Frontend automatically reloads on file changes
- Backend requires manual restart

### Debug Mode
- Backend: Set `FLASK_DEBUG=True` in .env
- Frontend: Open DevTools (F12) and check Console tab

### Database Reset
- Delete `kb_agent.db` to reset database
- Clear `./logs/queries.json` to reset query logs
- Clear `./chroma_db` to reset vector database

### Testing API
Use tools like:
- Postman: https://www.postman.com/
- Insomnia: https://insomnia.rest/
- Thunder Client (VS Code extension)

---

## Next Steps

1. **Deploy**: See DEPLOYMENT.md for production setup
2. **Customize**: Add your own company documents
3. **Extend**: Add new features or modify search algorithm
4. **Monitor**: Set up logging and monitoring

---

## Support

If you encounter issues:

1. Check this troubleshooting guide
2. Review API.md documentation
3. Check console/log files for error messages
4. Try restarting both services
5. Open a GitHub issue with error details
