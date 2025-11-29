import React from 'react';
import { Send, Loader, AlertCircle, X } from 'lucide-react';

const ChatInterface = ({
  messages,
  isLoading,
  query,
  onQueryChange,
  onSendMessage,
  onExampleQuestion,
  exampleQuestions,
  error,
  onClearChat,
  messagesEndRef
}) => {
  return (
    <div className="flex flex-col h-full bg-gradient-to-b from-transparent via-purple-900/20 to-purple-900/40">
      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto scrollbar-hide px-6 py-4 space-y-4">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center">
            <div className="mb-8">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full mx-auto mb-4 flex items-center justify-center">
                <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2 5a2 2 0 012-2h12a2 2 0 012 2v10a2 2 0 01-2 2H4a2 2 0 01-2-2V5z" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-white mb-2">Welcome to KB-Agent</h2>
              <p className="text-gray-300 mb-6">Ask questions about company policies and documents</p>
            </div>

            {/* Example Questions */}
            <div className="w-full max-w-2xl">
              <p className="text-gray-400 text-sm mb-3 font-medium">Try asking:</p>
              <div className="grid grid-cols-1 gap-2">
                {exampleQuestions.map((question, idx) => (
                  <button
                    key={idx}
                    onClick={() => onExampleQuestion(question)}
                    className="text-left p-3 rounded-lg bg-white/10 hover:bg-white/20 text-gray-200 text-sm transition-all border border-white/10 hover:border-white/30"
                  >
                    → {question}
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <div key={message.id} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div
                  className={`max-w-xs lg:max-w-md xl:max-w-lg px-4 py-3 rounded-lg ${
                    message.role === 'user'
                      ? 'bg-blue-500/80 text-white rounded-br-none'
                      : 'bg-white/10 text-gray-100 rounded-bl-none border border-white/20'
                  }`}
                >
                  <p className="text-sm font-medium">{message.content}</p>
                  
                  {/* Sources */}
                  {message.sources && message.sources.length > 0 && (
                    <div className="mt-2 pt-2 border-t border-white/20">
                      <p className="text-xs font-semibold opacity-75 mb-1">Sources:</p>
                      <div className="space-y-1">
                        {message.sources.map((source, idx) => (
                          <div key={idx} className="text-xs opacity-75">
                            📄 {source.title} ({source.section})
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  <p className="text-xs opacity-60 mt-2">{message.timestamp}</p>
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white/10 text-gray-100 px-4 py-3 rounded-lg rounded-bl-none border border-white/20">
                  <div className="flex items-center gap-2">
                    <Loader className="w-4 h-4 animate-spin" />
                    <p className="text-sm">Thinking...</p>
                  </div>
                </div>
              </div>
            )}
            
            {error && (
              <div className="flex justify-center">
                <div className="max-w-md bg-red-500/20 border border-red-500/50 text-red-200 px-4 py-3 rounded-lg flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                  <p className="text-sm">{error}</p>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input Area */}
      <div className="border-t border-white/10 bg-black/20 p-4">
        <form onSubmit={onSendMessage} className="space-y-3">
          <textarea
            value={query}
            onChange={(e) => onQueryChange(e.target.value)}
            placeholder="Ask me anything about company policies..."
            disabled={isLoading}
            className="w-full px-4 py-3 rounded-lg bg-white/10 text-white placeholder-gray-400 border border-white/20 focus:border-blue-500 focus:outline-none resize-none disabled:opacity-50"
            rows="3"
          />
          
          <div className="flex gap-2">
            <button
              type="submit"
              disabled={isLoading || !query.trim()}
              className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              <Send size={18} />
              Send Message
            </button>
            
            {messages.length > 0 && (
              <button
                type="button"
                onClick={onClearChat}
                disabled={isLoading}
                className="px-4 py-3 bg-white/10 hover:bg-white/20 text-gray-200 rounded-lg font-medium disabled:opacity-50 transition-all"
              >
                Clear
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
};

export default ChatInterface;
