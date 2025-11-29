"""
Search service for document retrieval and query processing
Implements keyword-based semantic search algorithm with optional embedding hybrid ranking
"""

from datetime import datetime
from typing import List, Dict, Any

# Try to import embeddings model
try:
    from models.embeddings import Embeddings
except Exception:
    Embeddings = None


class SearchService:
    """Handles document searching and retrieval"""
    
    def __init__(self):
        """Initialize the search service"""
        self.min_score = 0.3
        self.top_k = 3
        # Embeddings for hybrid ranking
        try:
            self.embeddings = Embeddings() if Embeddings else None
        except Exception:
            self.embeddings = None
    
    def search(self, query: str, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Search documents using keyword matching algorithm and optional embedding similarity
        
        Args:
            query: User search query
            documents: List of documents to search through
            
        Returns:
            List of relevant documents sorted by relevance score
        """
        if not query or not documents:
            return []
        
        # Normalize query
        query_words = self._normalize_text(query).split()
        
        # Score each document
        scored_documents = []
        for doc in documents:
            keyword_score = self._calculate_score(query_words, doc)

            # Embedding similarity (0.0-1.0) when available
            emb_score = 0.0
            if self.embeddings:
                try:
                    emb_score = self.embeddings.similarity(query, doc.get('content', ''))
                except Exception:
                    emb_score = 0.0

            # Combine keyword and embedding scores (weights: keyword 0.7, embedding 0.3)
            combined_score = min(1.0, (keyword_score * 0.7) + (emb_score * 0.3))

            if combined_score >= self.min_score:
                scored_documents.append({
                    'id': doc['id'],
                    'title': doc['title'],
                    'section': doc['section'],
                    'content': doc['content'],
                    'keyword_score': round(keyword_score, 4),
                    'embedding_score': round(emb_score, 4),
                    'score': round(combined_score, 4),
                    'relevance': self._get_relevance_label(combined_score)
                })
        
        # Sort by score (descending)
        scored_documents.sort(key=lambda x: x['score'], reverse=True)
        
        # Return top K results
        return scored_documents[:self.top_k]
    
    def _calculate_score(self, query_words: List[str], document: Dict[str, Any]) -> float:
        """
        Calculate relevance score for a document
        
        Args:
            query_words: Normalized query words
            document: Document to score
            
        Returns:
            Relevance score (0.0 to 1.0)
        """
        if not query_words:
            return 0.0
        
        # Normalize document text
        doc_text = self._normalize_text(f"{document['title']} {document['section']} {document['content']}")
        doc_words = set(doc_text.split())
        
        # Calculate word match ratio
        matches = sum(1 for word in query_words if word in doc_words)
        word_match_score = matches / len(query_words)
        
        # Calculate phrase match bonus
        doc_lower = document.get('content','').lower()
        query_phrase = ' '.join(query_words)
        phrase_bonus = 0.0
        
        if query_phrase in doc_lower:
            phrase_bonus = 0.3
        
        # Title/section bonus
        title_section = f"{document.get('title','')} {document.get('section','')}".lower()
        title_bonus = 0.0
        for word in query_words:
            if word in title_section.split():
                title_bonus += 0.15
        
        # Calculate final score
        final_score = min(1.0, (word_match_score * 0.6) + phrase_bonus + min(title_bonus, 0.25))
        
        return final_score
    
    def _normalize_text(self, text: str) -> str:
        """
        Normalize text for searching
        
        Args:
            text: Text to normalize
            
        Returns:
            Normalized text (lowercase, minimal special chars)
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation but keep spaces and common separators
        import string
        text = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def _get_relevance_label(self, score: float) -> str:
        """
        Get relevance label based on score
        
        Args:
            score: Relevance score
            
        Returns:
            Relevance label
        """
        if score >= 0.8:
            return "Very High"
        elif score >= 0.6:
            return "High"
        elif score >= 0.4:
            return "Medium"
        else:
            return "Low"
    
    def filter_by_section(self, documents: List[Dict[str, Any]], section: str) -> List[Dict[str, Any]]:
        """
        Filter documents by section
        
        Args:
            documents: List of documents
            section: Section to filter by
            
        Returns:
            Filtered documents
        """
        return [d for d in documents if d.get('section', '').lower() == section.lower()]
    
    def get_document_by_id(self, documents: List[Dict[str, Any]], doc_id: str) -> Dict[str, Any]:
        """
        Get a document by its ID
        
        Args:
            documents: List of documents
            doc_id: Document ID to find
            
        Returns:
            Document or None if not found
        """
        for doc in documents:
            if doc.get('id') == doc_id:
                return doc
        return None
