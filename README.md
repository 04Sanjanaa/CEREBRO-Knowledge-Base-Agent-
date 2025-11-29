# CEREBRO (KB-Agent System) 

Intelligent Knowledge Base Query System with React frontend and Flask backend.

## Features

- **Chat Interface**: Ask natural language questions about company policies
- **Document Management**: Browse and search indexed documents
- **Query Logging**: Track and export all queries with analytics
- **System Analytics**: Monitor system performance and query statistics
- **Semantic Search**: Keyword-based document retrieval
- **Multi-Source Citations**: View source documents for answers

## Tech Stack

### Frontend
- React 18 with Hooks
- Tailwind CSS for styling
- Lucide React for icons
- Axios for API communication

### Backend
- Flask REST API
- Python 3.9+
- SQLite database
- Vector-based search

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

┌──────────────────────────────────────────────────────┐
│                       USER (Frontend)                 │
│                 React Web Application                 │
│  - Chat Interface                                     │
│  - Document Browser                                   │
│  - Query Logs View                                    │
│  - System Info Dashboard                              │
└───────────────▲───────────────────────────────────────┘
                │  HTTPS API Calls (Axios)
                │  /api/query /api/search /api/logs
                │
┌───────────────┴───────────────────────────────────────┐
│                   BACKEND (Flask API)                 │
│  - Receives user query                                │
│  - Calls Search Service                                │
│  - Generates semantic matches                           │
│  - Formats & returns response                          │
│                                                        │
│   Endpoints:                                           │
│   • GET /api/documents                                 │
│   • POST /api/search                                   │
│   • POST /api/query                                    │
│   • GET /api/logs                                      │
│   • GET /api/stats                                     │
└───────────────▲───────────────────────────────────────┘
                │ Calls internal services
                │
┌───────────────┴───────────────────────────────────────┐
│                     SERVICES LAYER                     │
│                                                        │
│ 1. Search Service                                      │
│    - Loads embeddings                                  │
│    - Performs vector similarity search                 │
│    - Returns top-K document chunks                     │
│                                                        │
│ 2. Logger Service                                      │
│    - Saves every query                                 │
│    - Generates query analytics                         │
└───────────────▲───────────────────────────────────────┘
                │ Reads/Writes
                │
┌───────────────┴───────────────────────────────────────┐
│                     VECTOR DATABASE                    │
│         (Embeddings stored in SQLite / custom DB)      │
│   - Documents are pre-processed and embedded           │
│   - Vector index supports fast semantic queries        │
└───────────────▲───────────────────────────────────────┘
                │ Loaded using index_documents.py
                │
┌───────────────┴───────────────────────────────────────┐
│                   DOCUMENT STORAGE                     │
│        /data/documents/*.pdf / .txt / .md files        │
│   - Raw company policies                               │
│   - Onboarding manual                                  │
│   - Leave policy                                       │
│   - HR/IT guidelines                                   │
└────────────────────────────────────────────────────────┘

This architecture represents a full-stack Knowledge Base Agent built with a React
frontend and Flask backend. Users interact with the system through a chat interface, document browser, and analytics dashboard. All user queries are sent to the Flask API, which processes them through two service modules: the Search Service (responsible for semantic similarity search on vector embeddings) and the Logger Service (responsible for tracking and exporting query logs).

Documents are pre-processed using `index_documents.py`, which generates embeddings and stores them in the vector database. During a query, the system performs vector search to identify relevant document chunks and returns a structured response to the frontend. This ensures fast, accurate retrieval of policy and handbook information.


## Quick Start

### Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. **Install Python dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

2. **Create environment file**:
```bash
cp .env.example .env
```

3. **Run Flask server**:
```bash
python app.py
```

Server will start on `http://localhost:5000`

### Frontend Setup

1. **Install npm dependencies**:
```bash
cd frontend
npm install
```

2. **Start React development server**:
```bash
npm start
```

App will open at `http://localhost:3000`

## API Endpoints

### Health Check
- `GET /api/health` - Check API status

### Documents
- `GET /api/documents` - List all indexed documents
- `POST /api/search` - Search documents by query

### Queries
- `POST /api/query` - Submit a query and get response
- `GET /api/logs` - Get all query logs

### Analytics
- `GET /api/stats` - Get system statistics

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

1. **Ask a Question**: Type a question in the chat interface about company policies
2. **Browse Documents**: Visit the Documents tab to explore all available documents
3. **View Query History**: Check the Query Logs tab to see previous questions
4. **Monitor System**: Visit System Info to view statistics and system health

## Development

### Running Tests

Backend:
```bash
cd backend
python -m pytest
```

Frontend:
```bash
cd frontend
npm test
```

### Building for Production

Frontend:
```bash
cd frontend
npm run build
```

## Deployment

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

- [ ] Multi-language support
- [ ] Advanced NLP query processing
- [ ] Integration with external knowledge bases
- [ ] User authentication and roles
- [ ] Real-time document updates
- [ ] Mobile app version
- [ ] Advanced analytics dashboard

## Changelog

### Version 1.0.0
- Initial release
- Core chat interface
- Document browsing
- Query logging and analytics
- System monitoring
