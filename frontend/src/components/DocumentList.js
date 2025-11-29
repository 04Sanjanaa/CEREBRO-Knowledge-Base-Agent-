import React, { useState } from 'react';
import { Search, FileText, BookOpen, ArrowRight } from 'lucide-react';

const DocumentList = ({ documents }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDoc, setSelectedDoc] = useState(null);

  const filteredDocs = documents.filter(doc =>
    doc.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    doc.section.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const groupedBySection = filteredDocs.reduce((acc, doc) => {
    if (!acc[doc.section]) {
      acc[doc.section] = [];
    }
    acc[doc.section].push(doc);
    return acc;
  }, {});

  return (
    <div className="flex flex-col h-full bg-gradient-to-b from-transparent via-purple-900/20 to-purple-900/40">
      {/* Search Bar */}
      <div className="border-b border-white/10 p-4 bg-black/20">
        <div className="relative">
          <Search className="absolute left-3 top-3 text-gray-400" size={20} />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search documents..."
            className="w-full pl-10 pr-4 py-2 rounded-lg bg-white/10 text-white placeholder-gray-400 border border-white/20 focus:border-blue-500 focus:outline-none"
          />
        </div>
      </div>

      {/* Documents View */}
      <div className="flex-1 overflow-y-auto scrollbar-hide">
        {selectedDoc ? (
          // Document Detail View
          <div className="p-6 space-y-4">
            <button
              onClick={() => setSelectedDoc(null)}
              className="text-blue-300 hover:text-blue-200 text-sm font-medium flex items-center gap-1 mb-4"
            >
              ← Back to List
            </button>

            <div className="bg-white/10 rounded-lg p-6 border border-white/20">
              <div className="flex items-start gap-3 mb-4">
                <FileText className="text-blue-400 flex-shrink-0 mt-1" size={28} />
                <div className="flex-1">
                  <h2 className="text-2xl font-bold text-white">{selectedDoc.title}</h2>
                  <p className="text-sm text-gray-400 mt-1">{selectedDoc.section}</p>
                </div>
              </div>

              <div className="bg-black/30 rounded p-4 text-gray-200 text-sm whitespace-pre-wrap font-mono">
                {selectedDoc.content}
              </div>
            </div>
          </div>
        ) : filteredDocs.length > 0 ? (
          // Document List View
          <div className="p-6 space-y-4">
            {Object.entries(groupedBySection).map(([section, docs]) => (
              <div key={section}>
                <h3 className="text-sm font-semibold text-gray-300 mb-3 px-3">{section}</h3>
                <div className="space-y-2">
                  {docs.map((doc) => (
                    <button
                      key={doc.id}
                      onClick={() => setSelectedDoc(doc)}
                      className="w-full text-left p-4 rounded-lg bg-white/10 hover:bg-white/20 border border-white/20 hover:border-blue-400/50 transition-all group"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex items-start gap-3 flex-1">
                          <FileText className="text-blue-400 flex-shrink-0 mt-1" size={20} />
                          <div className="flex-1 min-w-0">
                            <h4 className="font-semibold text-white group-hover:text-blue-300 transition-colors">
                              {doc.title}
                            </h4>
                            <p className="text-xs text-gray-400 mt-1">
                              {doc.content.substring(0, 100)}...
                            </p>
                          </div>
                        </div>
                        <ArrowRight className="text-gray-500 group-hover:text-blue-400 flex-shrink-0 mt-1 transition-colors" size={18} />
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        ) : (
          // Empty State
          <div className="h-full flex flex-col items-center justify-center text-center">
            <BookOpen className="w-16 h-16 text-gray-500 mb-4 opacity-50" />
            <p className="text-gray-400 text-sm">No documents found</p>
          </div>
        )}
      </div>

      {/* Footer Stats */}
      <div className="border-t border-white/10 bg-black/20 px-6 py-3 text-sm text-gray-400">
        Showing {filteredDocs.length} of {documents.length} documents
      </div>
    </div>
  );
};

export default DocumentList;
