"""
CEREBRO - AI Knowledge Base Agent
Main application entry point with LLM, Calendar, and Voice support
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os
from config import Config
from services.search_service import SearchService
from services.logger_service import LoggerService
from services.db_service import DBService
from services.llm_service import LLMService
from services.calendar_service import CalendarService
from flask import send_from_directory

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Initialize services
search_service = SearchService()
llm_service = LLMService()
calendar_service = CalendarService()

# Initialize DB service and logger
db_service = DBService(db_path=os.path.join('data', 'kb_agent.db'))
logger_service = LoggerService(db_service=db_service)

# Sample documents data (will be seeded into DB if empty)
SAMPLE_DOCUMENTS = [
    {
        'id': 'doc_001',
        'title': 'Annual Leave Policy',
        'section': 'HR Policies',
        'content': '''Annual Leave Policy:
        
• Full-time employees are entitled to 20 days of annual leave per year
• Leave accrues at 1.67 days per month
• Unused leave can be carried forward up to 5 days into the next year
• Leave requests must be submitted at least 2 weeks in advance
• Approval is subject to business needs and team availability
• Public holidays are separate from annual leave entitlement'''
    },
    {
        'id': 'doc_002',
        'title': 'New Employee Onboarding',
        'section': 'HR Operations',
        'content': '''Employee Onboarding Process:

Step 1: Pre-boarding (1 week before start date)
• HR sends welcome email with first-day details
• IT provisions laptop and accounts
• Manager prepares workspace and access cards

Step 2: Day 1
• Welcome orientation at 9 AM
• HR paperwork completion
• IT setup and system access
• Team introduction lunch

Step 3: Week 1
• Department orientation
• Assign onboarding buddy
• Initial training sessions
• Review role expectations

Step 4: Month 1
• Regular check-ins with manager
• Complete mandatory training modules
• 30-day review meeting'''
    },
    {
        'id': 'doc_003',
        'title': 'Remote Work Policy',
        'section': 'Workplace Policies',
        'content': '''Remote Work Policy:

Eligibility:
• Employees must complete 3 months probation
• Role must be suitable for remote work
• Manager approval required

Schedule:
• Hybrid: Up to 3 days remote per week
• Fully remote: Subject to approval and business needs
• Core hours: 10 AM - 3 PM (must be available)

Requirements:
• Stable internet connection (minimum 50 Mbps)
• Dedicated workspace
• Attendance at mandatory in-office meetings
• Response time: Within 2 hours during work hours

Equipment:
• Company provides laptop and necessary software
• Home office stipend: $500 annually'''
    },
    {
        'id': 'doc_004',
        'title': 'IT Support Guidelines',
        'section': 'IT Operations',
        'content': '''IT Support Process:

Self-Service Portal: support.company.com
• Password resets
• Software installation requests
• VPN troubleshooting guides

Helpdesk Contact:
• Email: itsupport@company.com
• Phone: Ext 5500 (8 AM - 6 PM)
• Slack: #it-support

Priority Levels:
• P1 (Critical): System down - 1 hour response
• P2 (High): Major functionality issue - 4 hours
• P3 (Medium): Minor issue - 1 business day
• P4 (Low): Enhancement request - 3 business days

Common Issues:
• VPN connectivity: Restart client, check credentials
• Email issues: Clear cache, check settings
• Laptop problems: Contact helpdesk immediately'''
    },
    {
        'id': 'doc_005',
        'title': 'Expense Reimbursement',
        'section': 'Finance Policies',
        'content': '''Expense Reimbursement Policy:

Eligible Expenses:
• Business travel (flights, hotels, transport)
• Client entertainment (meals, activities)
• Office supplies and equipment
• Professional development courses

Limits:
• Meals: $50 per day domestic, $75 international
• Hotels: Up to $200 per night
• Client entertainment: Requires manager pre-approval

Submission Process:
1. Log into expense portal: expenses.company.com
2. Upload receipts (required for expenses over $25)
3. Submit within 30 days of expense date
4. Manager approval required
5. Payment processed within 2 weeks

Non-eligible:
• Personal expenses
• Alcoholic beverages (unless client entertainment)
• Late fees or penalties'''
    }
]

# Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/documents', methods=['GET'])
def get_documents():
    """Get all indexed documents"""
    try:
        docs = db_service.get_documents()
        # Seed if empty
        if not docs:
            db_service.add_documents(SAMPLE_DOCUMENTS)
            docs = db_service.get_documents()

        return jsonify({
            'success': True,
            'count': len(docs),
            'documents': docs
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search():
    """Search documents with semantic search"""
    try:
        data = request.json
        query = data.get('query', '')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query cannot be empty'
            }), 400
        
        # Search documents
        results = search_service.search(query, SAMPLE_DOCUMENTS)
        
        return jsonify({
            'success': True,
            'query': query,
            'results': results,
            'count': len(results)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/query', methods=['POST'])
def handle_query():
    """Handle user query with LLM-powered responses"""
    try:
        data = request.json
        query = data.get('query', '')
        use_llm = data.get('use_llm', True)  # Use LLM by default
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query cannot be empty'
            }), 400
        
        # Ensure documents are loaded from DB and seed if necessary
        docs = db_service.get_documents()
        if not docs:
            db_service.add_documents(SAMPLE_DOCUMENTS)
            docs = db_service.get_documents()

        # Search for relevant documents
        search_results = search_service.search(query, docs)
        sources = [{'title': r['title'], 'section': r['section']} for r in search_results] if search_results else []
        
        # Use LLM if available and enabled, otherwise fallback to keyword matching
        if use_llm and llm_service.enabled:
            llm_result = llm_service.generate_response(query, search_results or docs, top_k=3)
            if llm_result['success']:
                response_text = llm_result['response']
            else:
                # Fallback to keyword-based response
                response_text = _generate_keyword_response(search_results, query)
        else:
            # Use keyword-based response
            response_text = _generate_keyword_response(search_results, query)
        
        # Log the query
        logger_service.log_query(query, bool(search_results), sources)
        
        return jsonify({
            'success': True,
            'query': query,
            'response': response_text,
            'sources': sources,
            'timestamp': datetime.now().isoformat(),
            'llm_enabled': llm_service.enabled
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def _generate_keyword_response(search_results, query):
    """Generate response using keyword matching (fallback)"""
    if not search_results:
        return 'The available documents do not contain this information. Please contact HR directly or check the employee portal for more details.'
    
    top_result = search_results[0]
    content_lines = top_result['content'].split('\n')
    
    # Extract bullet points and structured content
    bullet_lines = [line.strip() for line in content_lines if line.strip().startswith('•')]
    step_lines = [line.strip() for line in content_lines if 'Step' in line or 'step' in line]
    
    response_text = f"**{top_result['title']} ({top_result['section']})**\n\n"
    
    # Add bullet points
    if bullet_lines:
        response_text += '\n'.join(bullet_lines[:10])
    elif step_lines:
        response_text += '\n'.join(step_lines[:10])
    else:
        # Fallback to formatted lines
        relevant_lines = [line.strip() for line in content_lines if line.strip() and not line.startswith('**')]
        response_text += '\n'.join(relevant_lines[:10])
    
    # Add related documents at the end
    if len(search_results) > 1:
        related = ', '.join([r['title'] for r in search_results[1:]])
        response_text += f"\n\n[Related documents: {related}]"
    
    return response_text

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get query logs"""
    try:
        logs = logger_service.get_logs()
        return jsonify({
            'success': True,
            'count': len(logs),
            'logs': logs
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    logs = logger_service.get_logs()
    answered = sum(1 for log in logs if log.get('answered', False))
    
    return jsonify({
        'success': True,
        'stats': {
            'total_documents': len(SAMPLE_DOCUMENTS),
            'total_queries': len(logs),
            'answered_queries': answered,
            'response_rate': f"{(answered/len(logs)*100):.1f}%" if logs else "0%",
            'vector_db_status': 'Active',
            'query_logging': 'Active',
            'avg_response_time': '< 1 second'
        }
    }), 200

@app.route('/api/seed', methods=['POST'])
def seed_documents():
    """Force seed documents into the database (dev helper)"""
    try:
        db_service.add_documents(SAMPLE_DOCUMENTS)
        return jsonify({
            'success': True,
            'message': f'Seeded {len(SAMPLE_DOCUMENTS)} documents into the database'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/clear-logs', methods=['POST'])
def clear_logs():
    """Clear all query logs (dev helper)"""
    try:
        logger_service.clear_logs()
        return jsonify({
            'success': True,
            'message': 'All query logs have been cleared'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get upcoming company events"""
    try:
        result = calendar_service.get_upcoming_events()
        return jsonify({
            'success': result['success'],
            'events': result.get('events', []),
            'count': result.get('count', 0)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'events': []
        }), 500

@app.route('/api/holidays', methods=['GET'])
def get_holidays():
    """Get company holidays"""
    try:
        result = calendar_service.get_company_holidays()
        return jsonify({
            'success': result['success'],
            'holidays': result.get('holidays', []),
            'year': result.get('year')
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'holidays': []
        }), 500

@app.route('/api/voice', methods=['POST'])
def handle_voice():
    """Handle voice input transcription"""
    try:
        # Extract audio data or text from voice recognition
        data = request.json
        transcribed_text = data.get('text', '')
        
        if not transcribed_text:
            return jsonify({
                'success': False,
                'error': 'No text provided'
            }), 400
        
        # Process the transcribed text as a regular query
        # This would normally use speech-to-text API, but for now we receive pre-transcribed text
        return jsonify({
            'success': True,
            'transcribed': transcribed_text,
            'message': 'Voice input received. Processing as regular query.'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/info', methods=['GET'])
def app_info():
    """Show app information and available endpoints"""
    info_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>KB-Agent - API Info</title>
        <style>
            body { font-family: Arial, sans-serif; background: #0f172a; color: #e6eef8; padding: 20px; }
            h1 { color: #0b63ff; }
            h2 { color: #7dd3fc; margin-top: 20px; }
            .endpoint { background: rgba(255,255,255,0.05); padding: 12px; margin: 8px 0; border-radius: 6px; border-left: 3px solid #0b63ff; }
            .method { font-weight: bold; color: #10b981; }
            code { background: rgba(0,0,0,0.3); padding: 2px 6px; border-radius: 3px; }
            a { color: #0b63ff; text-decoration: none; }
            a:hover { text-decoration: underline; }
            ul { list-style-position: inside; }
        </style>
    </head>
    <body>
        <h1>📚 KB-Agent - Knowledge Base Query System</h1>
        <p>A lightweight knowledge base system with semantic search, query logging, and embeddings.</p>
        
        <h2>🚀 Quick Links</h2>
        <ul>
            <li><a href="/">→ Web UI (Chat Interface)</a></li>
            <li><a href="/api/health">→ Health Check</a></li>
            <li><a href="/api/documents">→ All Documents</a></li>
            <li><a href="/api/logs">→ Query Logs</a></li>
            <li><a href="/api/stats">→ Statistics</a></li>
        </ul>
        
        <h2>📡 API Endpoints</h2>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/</code>
            <p>Serve the lightweight web UI (single-file HTML)</p>
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/api/health</code>
            <p>Check if the API is running and healthy.</p>
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/api/documents</code>
            <p>Get all indexed documents (from SQLite database).</p>
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> <code>/api/search</code>
            <p>Search documents with keyword + embedding hybrid scoring.</p>
            <p><strong>Body:</strong> <code>{"query": "your question"}</code></p>
            <p>Returns relevance scores (keyword, embedding, combined).</p>
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> <code>/api/query</code>
            <p>Submit a query and get an AI-formatted response with sources.</p>
            <p><strong>Body:</strong> <code>{"query": "your question"}</code></p>
            <p>Logs the query automatically.</p>
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/api/logs</code>
            <p>Retrieve all query logs (persisted in SQLite).</p>
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/api/stats</code>
            <p>Get system statistics: document count, query count, response rate, etc.</p>
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> <code>/api/seed</code>
            <p><strong>Dev Helper:</strong> Force-seed sample documents into the database.</p>
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> <code>/api/clear-logs</code>
            <p><strong>Dev Helper:</strong> Clear all query logs.</p>
        </div>
        
        <h2>🏗️ Architecture</h2>
        <ul>
            <li><strong>Backend:</strong> Flask + SQLite for persistence</li>
            <li><strong>Search:</strong> Keyword-based + embedding similarity (hybrid scoring)</li>
            <li><strong>Frontend:</strong> Minimal static HTML + Fetch API (no Node.js required)</li>
            <li><strong>Logging:</strong> SQLite with JSON serialization of sources</li>
            <li><strong>Embedding Model:</strong> Character-frequency based (simple demo; use sentence-transformers in production)</li>
        </ul>
        
        <h2>📦 Sample Documents</h2>
        <ul>
            <li><strong>Annual Leave Policy</strong> - Entitlements and procedures</li>
            <li><strong>Employee Onboarding</strong> - 4-step process</li>
            <li><strong>Remote Work Policy</strong> - Eligibility, schedule, equipment</li>
            <li><strong>IT Support Guidelines</strong> - Channels, priorities, common issues</li>
            <li><strong>Expense Reimbursement</strong> - Eligible expenses, limits, submission</li>
        </ul>
        
        <h2>🛠️ Development</h2>
        <p><strong>Backend running on:</strong> <code>http://localhost:5000</code></p>
        <p><strong>Database:</strong> <code>./data/kb_agent.db</code> (SQLite)</p>
        <p><strong>Logs:</strong> <code>./logs/backend.log</code></p>
        
        <p style="margin-top: 30px; font-size: 12px; color: #9fb7d9;">
            Built with Flask, SQLite, and simple embeddings. See README.md for more info.
        </p>
    </body>
    </html>
    '''
    return info_html, 200, {'Content-Type': 'text/html'}

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


# Serve minimal static frontend
@app.route('/', methods=['GET'])
def serve_index():
    try:
        return send_from_directory('static', 'index.html')
    except Exception:
        return jsonify({'success': False, 'error': 'Static UI not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
