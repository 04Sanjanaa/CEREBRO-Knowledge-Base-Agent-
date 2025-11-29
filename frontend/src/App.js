import React, { useState, useEffect, useRef } from 'react';
import {
  Send,
  MessageSquare,
  FileText,
  BarChart3,
  Settings,
  Loader,
  AlertCircle,
  CheckCircle2,
  Clock,
  BookOpen
} from 'lucide-react';
import api from './services/api';
import ChatInterface from './components/ChatInterface';
import DocumentList from './components/DocumentList';
import QueryLogs from './components/QueryLogs';
import SystemInfo from './components/SystemInfo';

function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [documents, setDocuments] = useState([]);
  const [queryLogs, setQueryLogs] = useState([]);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState(null);
  const messagesEndRef = useRef(null);

  const exampleQuestions = [
    'How much annual leave am I entitled to?',
    'What is the process for remote work approval?',
    'How do I submit an expense for reimbursement?',
    'What should I do on my first day of onboarding?',
    'Who do I contact for IT support?'
  ];

  // Fetch documents and logs on mount
  useEffect(() => {
    loadDocuments();
    loadLogs();
    loadStats();

    // Poll for updates every 30 seconds
    const interval = setInterval(() => {
      loadLogs();
      loadStats();
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  // Auto-scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadDocuments = async () => {
    try {
      const response = await api.get('/api/documents');
      if (response.data.success) {
        setDocuments(response.data.documents);
        setError(null);
      }
    } catch (err) {
      setError('Failed to load documents');
      console.error(err);
    }
  };

  const loadLogs = async () => {
    try {
      const response = await api.get('/api/logs');
      if (response.data.success) {
        setQueryLogs(response.data.logs);
      }
    } catch (err) {
      console.error('Failed to load logs:', err);
    }
  };

  const loadStats = async () => {
    try {
      const response = await api.get('/api/stats');
      if (response.data.success) {
        setStats(response.data.stats);
      }
    } catch (err) {
      console.error('Failed to load stats:', err);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: query,
      timestamp: new Date().toLocaleTimeString(),
      sources: []
    };

    setMessages(prev => [...prev, userMessage]);
    setQuery('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await api.post('/api/query', { query });

      if (response.data.success) {
        const assistantMessage = {
          id: Date.now() + 1,
          role: 'assistant',
          content: response.data.response,
          timestamp: new Date().toLocaleTimeString(),
          sources: response.data.sources
        };

        setMessages(prev => [...prev, assistantMessage]);
        
        // Reload logs after successful query
        setTimeout(() => {
          loadLogs();
          loadStats();
        }, 500);
      } else {
        setError(response.data.error || 'Failed to process query');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to send message');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleExampleQuestion = (question) => {
    setQuery(question);
  };

  const handleClearChat = () => {
    setMessages([]);
    setError(null);
  };

  return (
    <div className="h-screen bg-gradient-to-br from-purple-600 via-purple-700 to-indigo-800 flex flex-col">
      {/* Header */}
      <header className="bg-black/30 backdrop-blur-md border-b border-white/10 px-6 py-4 shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-purple-500 rounded-lg flex items-center justify-center">
              <BookOpen className="text-white" size={24} />
            </div>
            <h1 className="text-2xl font-bold text-white">KB-Agent</h1>
          </div>
          <p className="text-gray-300 text-sm">Intelligent Knowledge Base System</p>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Tab Content */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {activeTab === 'chat' && (
            <ChatInterface
              messages={messages}
              isLoading={isLoading}
              query={query}
              onQueryChange={setQuery}
              onSendMessage={handleSendMessage}
              onExampleQuestion={handleExampleQuestion}
              exampleQuestions={exampleQuestions}
              error={error}
              onClearChat={handleClearChat}
              messagesEndRef={messagesEndRef}
            />
          )}

          {activeTab === 'documents' && (
            <DocumentList documents={documents} />
          )}

          {activeTab === 'logs' && (
            <QueryLogs logs={queryLogs} />
          )}

          {activeTab === 'stats' && (
            <SystemInfo stats={stats} totalLogs={queryLogs.length} />
          )}
        </div>
      </div>

      {/* Bottom Tab Navigation */}
      <nav className="bg-black/40 backdrop-blur-md border-t border-white/10 px-6 py-4 flex gap-4">
        <button
          onClick={() => setActiveTab('chat')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
            activeTab === 'chat'
              ? 'bg-blue-500/80 text-white shadow-lg'
              : 'text-gray-300 hover:bg-white/10'
          }`}
        >
          <MessageSquare size={20} />
          Chat
        </button>
        <button
          onClick={() => setActiveTab('documents')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
            activeTab === 'documents'
              ? 'bg-blue-500/80 text-white shadow-lg'
              : 'text-gray-300 hover:bg-white/10'
          }`}
        >
          <FileText size={20} />
          Documents
        </button>
        <button
          onClick={() => setActiveTab('logs')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
            activeTab === 'logs'
              ? 'bg-blue-500/80 text-white shadow-lg'
              : 'text-gray-300 hover:bg-white/10'
          }`}
        >
          <Clock size={20} />
          Query Logs
        </button>
        <button
          onClick={() => setActiveTab('stats')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
            activeTab === 'stats'
              ? 'bg-blue-500/80 text-white shadow-lg'
              : 'text-gray-300 hover:bg-white/10'
          }`}
        >
          <BarChart3 size={20} />
          System Info
        </button>
      </nav>
    </div>
  );
}

export default App;
