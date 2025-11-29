import React, { useState } from 'react';
import { Clock, Download, Trash2, CheckCircle2, XCircle } from 'lucide-react';

const QueryLogs = ({ logs }) => {
  const [filterAnswered, setFilterAnswered] = useState(null);
  const [sortBy, setSortBy] = useState('recent');

  const filteredLogs = logs.filter(log => {
    if (filterAnswered === null) return true;
    return log.answered === filterAnswered;
  });

  const sortedLogs = [...filteredLogs].sort((a, b) => {
    if (sortBy === 'recent') {
      return new Date(b.timestamp) - new Date(a.timestamp);
    } else if (sortBy === 'oldest') {
      return new Date(a.timestamp) - new Date(b.timestamp);
    }
    return 0;
  });

  const exportLogs = (format) => {
    let content = '';
    let filename = '';

    if (format === 'json') {
      content = JSON.stringify(sortedLogs, null, 2);
      filename = `kb-agent-logs-${new Date().toISOString().split('T')[0]}.json`;
    } else if (format === 'csv') {
      content = 'ID,Timestamp,Query,Answered,Sources\n';
      sortedLogs.forEach(log => {
        const sources = log.sources.map(s => `${s.title}`).join(';');
        content += `"${log.id}","${log.timestamp}","${log.query.replace(/"/g, '""')}","${log.answered}","${sources}"\n`;
      });
      filename = `kb-agent-logs-${new Date().toISOString().split('T')[0]}.csv`;
    }

    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="flex flex-col h-full bg-gradient-to-b from-transparent via-purple-900/20 to-purple-900/40">
      {/* Controls */}
      <div className="border-b border-white/10 p-4 bg-black/20 space-y-3">
        <div className="flex gap-2 flex-wrap">
          <button
            onClick={() => setFilterAnswered(null)}
            className={`px-3 py-1 rounded text-sm font-medium transition-all ${
              filterAnswered === null
                ? 'bg-blue-500 text-white'
                : 'bg-white/10 text-gray-300 hover:bg-white/20'
            }`}
          >
            All ({logs.length})
          </button>
          <button
            onClick={() => setFilterAnswered(true)}
            className={`px-3 py-1 rounded text-sm font-medium transition-all flex items-center gap-1 ${
              filterAnswered === true
                ? 'bg-green-500/70 text-white'
                : 'bg-white/10 text-gray-300 hover:bg-white/20'
            }`}
          >
            <CheckCircle2 size={14} />
            Answered ({logs.filter(l => l.answered).length})
          </button>
          <button
            onClick={() => setFilterAnswered(false)}
            className={`px-3 py-1 rounded text-sm font-medium transition-all flex items-center gap-1 ${
              filterAnswered === false
                ? 'bg-red-500/70 text-white'
                : 'bg-white/10 text-gray-300 hover:bg-white/20'
            }`}
          >
            <XCircle size={14} />
            Not Answered ({logs.filter(l => !l.answered).length})
          </button>
        </div>

        <div className="flex gap-2">
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-3 py-1 rounded text-sm bg-white/10 text-gray-300 border border-white/20 focus:border-blue-500 focus:outline-none"
          >
            <option value="recent">Most Recent</option>
            <option value="oldest">Oldest First</option>
          </select>

          <button
            onClick={() => exportLogs('json')}
            className="px-3 py-1 rounded text-sm bg-white/10 text-gray-300 hover:bg-white/20 border border-white/20 transition-all flex items-center gap-1"
          >
            <Download size={14} /> Export JSON
          </button>

          <button
            onClick={() => exportLogs('csv')}
            className="px-3 py-1 rounded text-sm bg-white/10 text-gray-300 hover:bg-white/20 border border-white/20 transition-all flex items-center gap-1"
          >
            <Download size={14} /> Export CSV
          </button>
        </div>
      </div>

      {/* Logs List */}
      <div className="flex-1 overflow-y-auto scrollbar-hide">
        {sortedLogs.length > 0 ? (
          <div className="p-4 space-y-3">
            {sortedLogs.map((log) => (
              <div
                key={log.id}
                className="bg-white/10 border border-white/20 rounded-lg p-4 hover:bg-white/15 transition-all"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-xs font-mono text-gray-400 bg-black/30 px-2 py-1 rounded">
                        {log.id}
                      </span>
                      {log.answered ? (
                        <CheckCircle2 className="text-green-400" size={16} />
                      ) : (
                        <XCircle className="text-red-400" size={16} />
                      )}
                    </div>

                    <p className="text-white font-medium mb-2 line-clamp-2">{log.query}</p>

                    <div className="flex items-center gap-2 text-xs text-gray-400 mb-2">
                      <Clock size={14} />
                      {new Date(log.timestamp).toLocaleString()}
                    </div>

                    {log.sources && log.sources.length > 0 && (
                      <div className="text-xs text-gray-400 space-y-1">
                        <p className="font-semibold">Sources:</p>
                        <div className="flex flex-wrap gap-2">
                          {log.sources.map((source, idx) => (
                            <span
                              key={idx}
                              className="bg-blue-500/20 text-blue-300 px-2 py-1 rounded border border-blue-400/30"
                            >
                              {source.title}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="h-full flex flex-col items-center justify-center text-center">
            <Clock className="w-16 h-16 text-gray-500 mb-4 opacity-50" />
            <p className="text-gray-400 text-sm">No query logs yet</p>
          </div>
        )}
      </div>

      {/* Stats Footer */}
      {sortedLogs.length > 0 && (
        <div className="border-t border-white/10 bg-black/20 px-4 py-3 text-sm text-gray-400">
          <div className="flex justify-between">
            <span>Showing {sortedLogs.length} of {logs.length} queries</span>
            <span>
              Answered: {logs.filter(l => l.answered).length} ({logs.length > 0 ? Math.round((logs.filter(l => l.answered).length / logs.length) * 100) : 0}%)
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default QueryLogs;
