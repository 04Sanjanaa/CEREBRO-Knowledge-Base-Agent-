import React from 'react';
import {
  Database,
  Activity,
  AlertCircle,
  CheckCircle2,
  Zap,
  Clock
} from 'lucide-react';

const SystemInfo = ({ stats, totalLogs }) => {
  const statusItems = stats ? [
    {
      label: 'Vector DB',
      value: stats.vector_db_status,
      icon: Database,
      color: 'text-blue-400'
    },
    {
      label: 'Query Logging',
      value: stats.query_logging,
      icon: Activity,
      color: 'text-green-400'
    },
    {
      label: 'Response Time',
      value: stats.avg_response_time,
      icon: Zap,
      color: 'text-yellow-400'
    }
  ] : [];

  const metrics = stats ? [
    { label: 'Total Documents', value: stats.total_documents, icon: '📄' },
    { label: 'Total Queries', value: stats.total_queries, icon: '🔍' },
    { label: 'Answered Queries', value: stats.answered_queries, icon: '✅' },
    { label: 'Response Rate', value: stats.response_rate, icon: '📊' }
  ] : [];

  return (
    <div className="flex flex-col h-full bg-gradient-to-b from-transparent via-purple-900/20 to-purple-900/40 overflow-y-auto scrollbar-hide">
      <div className="p-6 space-y-6">
        {/* System Status */}
        <section>
          <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <Activity className="text-blue-400" size={24} />
            System Status
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {statusItems.map((item, idx) => (
              <div
                key={idx}
                className="bg-white/10 border border-white/20 rounded-lg p-4 flex items-center gap-3"
              >
                <item.icon className={`${item.color} flex-shrink-0`} size={24} />
                <div className="flex-1 min-w-0">
                  <p className="text-xs text-gray-400">{item.label}</p>
                  <p className="text-sm font-semibold text-white">{item.value}</p>
                </div>
                <CheckCircle2 className="text-green-400 flex-shrink-0" size={18} />
              </div>
            ))}
          </div>
        </section>

        {/* Key Metrics */}
        <section>
          <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <AlertCircle className="text-purple-400" size={24} />
            Key Metrics
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {metrics.map((metric, idx) => (
              <div
                key={idx}
                className="bg-white/10 border border-white/20 rounded-lg p-4"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs text-gray-400 mb-1">{metric.label}</p>
                    <p className="text-2xl font-bold text-white">{metric.value}</p>
                  </div>
                  <span className="text-3xl opacity-50">{metric.icon}</span>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* System Information */}
        <section>
          <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <Clock className="text-cyan-400" size={24} />
            System Information
          </h2>
          <div className="bg-white/10 border border-white/20 rounded-lg p-4 space-y-3">
            <div className="flex justify-between items-center pb-3 border-b border-white/10">
              <span className="text-sm text-gray-400">Version</span>
              <span className="text-sm font-medium text-white">1.0.0</span>
            </div>
            <div className="flex justify-between items-center pb-3 border-b border-white/10">
              <span className="text-sm text-gray-400">Backend API</span>
              <span className="text-sm font-medium text-green-400">Active</span>
            </div>
            <div className="flex justify-between items-center pb-3 border-b border-white/10">
              <span className="text-sm text-gray-400">Vector Database</span>
              <span className="text-sm font-medium text-green-400">Connected</span>
            </div>
            <div className="flex justify-between items-center pb-3 border-b border-white/10">
              <span className="text-sm text-gray-400">Last Updated</span>
              <span className="text-sm font-medium text-white">
                {new Date().toLocaleString()}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-400">Total Queries Processed</span>
              <span className="text-sm font-medium text-white">{totalLogs}</span>
            </div>
          </div>
        </section>

        {/* Help Section */}
        <section>
          <h2 className="text-lg font-bold text-white mb-4">Quick Help</h2>
          <div className="bg-blue-500/20 border border-blue-500/50 rounded-lg p-4">
            <ul className="space-y-2 text-sm text-gray-200">
              <li>• Use the <strong>Chat tab</strong> to ask questions about company policies</li>
              <li>• Check <strong>Documents tab</strong> to browse all available documents</li>
              <li>• Review <strong>Query Logs</strong> to see your search history</li>
              <li>• Export logs as JSON or CSV for further analysis</li>
            </ul>
          </div>
        </section>
      </div>
    </div>
  );
};

export default SystemInfo;
