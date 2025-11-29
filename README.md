# CEREBRO (KB-Agent System) 

Intelligent Knowledge Base Query System with React frontend and Flask backend.

## Overview

CEREBRO is a full-stack Knowledge Base Agent that allows employees to ask natural-language questions about company policies.
The system searches through HR documents, handbooks, and guidelines using vector similarity to retrieve the most relevant answers.

This agent supports:
-Natural language queries
-Document search
-Log analytics
-System metrics
-Multi-document embeddings

## Features

### Core Functionality
-Chat-based Query Interface for policy questions
-Semantic Vector Search using embeddings
-Document Browser to explore indexed content
-Query Logging with timestamps & metadata
-System Analytics Dashboard
-Source Citations for transparency

### Additional Capabilities
-Fast vector search (ChromaDB / FAISS)
-Modular backend architecture
-Fully responsive React UI
-Separate frontend & backend deployment


### Limitations 
-Only answers questions from indexed documents
-No generative reasoning (not GPT-style answers)
-English-only and limited to current document set
-Not optimized for thousands of documents
-No user accounts or role-based access
-Requires re-indexing when adding new documents

## Tech Stack

### Frontend
- React 18 with Hooks
- Tailwind CSS for styling
- Lucide React for icons
- Axios for API communication
- Deployment: Vercel

### Backend
- Flask REST API
- Python 3.9+
- SQLite database
- Vector-based search
- Deployment Render

## Project Structure

```
AI_Agent/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── config.py              # Configuration management
│   ├── models/
│   │   ├── __init__.py
│   │   └── embeddings.py      # Embedding utilities
│   ├── services/
│   │   ├── __init__.py
│   │   ├── search_service.py  # Document search logic
│   │   └── logger_service.py  # Query logging
│   ├── utils/
│   │   ├── __init__.py
│   │   └── vector_db.py       # Vector database
│   └── data/
│       └── documents/         # Document storage
├── frontend/
│   ├── public/
│   │   └── index.html         # HTML entry point
│   ├── src/
│   │   ├── index.js           # React entry point
│   │   ├── index.css          # Global styles
│   │   ├── App.js             # Main component
│   │   ├── components/
│   │   │   ├── ChatInterface.js
│   │   │   ├── DocumentList.js
│   │   │   ├── QueryLogs.js
│   │   │   └── SystemInfo.js
│   │   └── services/
│   │       └── api.js         # API client
│   └── package.json           # NPM dependencies
├── scripts/
│   ├── index_documents.py     # Document indexing script
│   └── export_logs.py         # Log export utility
├── docs/
│   ├── API.md                 # API documentation
│   ├── SETUP.md               # Setup guide
│   └── DEPLOYMENT.md          # Deployment guide
├── .env.example               # Environment variables template
├── requirements.txt           # Python dependencies
└── README.md                  # This file

```

## Architecture Diagram    
                        ┌───────────────────────────────┐
                        │            USER (UI)           │
                        │      React Frontend (Vercel)   │
                        │  • Chat Interface              │
                        │  • Document Browser            │
                        │  • Query Logs Dashboard        │
                        └───────────────────────────────┘
                                      │
                                      ▼
                        ┌───────────────────────────────┐
                        │      HTTPS API CALLS (Axios)   │
                        │   /api/query  /api/search      │
                        │   /api/logs   /api/documents   │
                        └───────────────────────────────┘
                                      │
                                      ▼
                        ┌───────────────────────────────┐
                        │       BACKEND (Flask API)      │
                        │   • Receives queries           │
                        │   • Calls Search Engine        │
                        │   • Formats + returns results  │
                        │   Endpoints:                   │
                        │      GET  /api/logs            │
                        │      GET  /api/stats           │
                        │      POST /api/query           │
                        │      POST /api/search          │
                        └───────────────────────────────┘
                                      │
                                      ▼
                        ┌───────────────────────────────┐
                        │        SERVICES LAYER          │
                        │  1. Search Service             │
                        │     • Loads embeddings         │
                        │     • Performs vector search   │
                        │     • Returns top-K results    │
                        │                               │
                        │  2. Logger Service             │
                        │     • Stores every query       │
                        │     • Generates analytics      │
                        └───────────────────────────────┘
                                      │
                                      ▼
                        ┌───────────────────────────────┐
                        │       VECTOR DATABASE          │
                        │     (ChromaDB / FAISS)         │
                        │  • Stores embeddings           │
                        │  • Fast similarity search      │
                        │  • Index built using           │
                        │    index_documents.py          │
                        └───────────────────────────────┘
                                      │
                                      ▼
                        ┌───────────────────────────────┐
                        │       DOCUMENT STORAGE         │
                        │   • /data/documents/*.pdf      │
                        │   • /txt /md /docx files       │
                        │   • Raw HR & policy data       │
                        └───────────────────────────────┘


This architecture represents a full-stack Knowledge Base Agent built with a React
frontend and Flask backend. Users interact with the system through a chat interface, document browser, and analytics dashboard. All user queries are sent to the Flask API, which processes them through two service modules: the Search Service (responsible for semantic similarity search on vector embeddings) and the Logger Service (responsible for tracking and exporting query logs).

Documents are pre-processed using `index_documents.py`, which generates embeddings and stores them in the vector database. During a query, the system performs vector search to identify relevant document chunks and returns a structured response to the frontend. This ensures fast, accurate retrieval of policy and handbook information.


## Quick Start

### Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

 cd backend
 pip install -r requirements.txt
 cp .env.example .env
 python app.py


Server will start on `http://localhost:5000`

### Frontend Setup

cd frontend
npm install
npm start


## API Endpoints

### Queries
- POST /api/query — ask a question
- POST /api/search — search documents

### Documents
- GET /api/documents

### Logs
- GET /api/logs

### System
- GET /api/stats
- GET /api/health

## Sample Documents

The system includes 5 sample company policy documents:

1. **Annual Leave Policy** - Leave entitlements and procedures
2. **Employee Onboarding** - Onboarding process and timeline
3. **Remote Work Policy** - Remote work guidelines and requirements
4. **IT Support Guidelines** - IT support channels and procedures
5. **Expense Reimbursement** - Reimbursement policy and limits

## Configuration

See `.env.example` for all available configuration options:

- `FLASK_PORT`: Backend server port (default: 5000)
- `REACT_APP_API_URL`: API base URL for frontend
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)
- `SEARCH_TOP_K`: Number of search results to return
- And more...

## Usage

1. Open the web UI
2. Ask a natural-language policy question
3. System performs vector search
4. Top relevant sections returned with citations
5. View logs and system stats in the dashboard


## Deployment

- Backend Tests
cd backend
pytest

- Frontend Tests
cd frontend
npm test

- Detailed steps in docs/DEPLOYMENT.md.

# Deployment Platforms:

- Frontend → Vercel
- Backend → Render
See `docs/DEPLOYMENT.md` for detailed deployment instructions.

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, questions, or issues:
- Open an issue on GitHub
- Contact the development team
- Check the documentation in `docs/`

## Roadmap

- Multi-language support
- Advanced NLP query processing
- Integration with external knowledge bases
- User authentication and roles
- Real-time document updates
- Mobile app version
- Advanced analytics dashboard

## Changelog

### Version 1.0.0
- Initial release
- Core chat interface
- Document browsing
- Query logging and analytics
- System monitoring
