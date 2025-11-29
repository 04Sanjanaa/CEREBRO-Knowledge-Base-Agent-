"""
Vector database utility for document embeddings and similarity search
"""

from typing import List, Dict, Any
import json
import os


class VectorDB:
    """Simple in-memory vector database for document storage and retrieval"""
    
    def __init__(self, db_path: str = './chroma_db'):
        """
        Initialize vector database
        
        Args:
            db_path: Path to store database files
        """
        self.db_path = db_path
        self.vectors = {}
        self.metadata = {}
        
        # Create database directory
        os.makedirs(db_path, exist_ok=True)
        
        # Load existing data
        self._load()
    
    def add_document(self, doc_id: str, content: str, metadata: Dict[str, Any] = None) -> None:
        """
        Add a document to the vector database
        
        Args:
            doc_id: Unique document identifier
            content: Document content
            metadata: Additional metadata (title, section, source, etc.)
        """
        # Simple hash-based representation (in production, use real embeddings)
        vector = self._create_simple_vector(content)
        
        self.vectors[doc_id] = vector
        self.metadata[doc_id] = {
            'content': content,
            'metadata': metadata or {},
            'created_at': str(self._get_timestamp())
        }
        
        self._save()
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for similar documents
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of similar documents with scores
        """
        query_vector = self._create_simple_vector(query)
        
        # Calculate similarity for each document
        similarities = []
        for doc_id, vector in self.vectors.items():
            score = self._calculate_similarity(query_vector, vector)
            if score > 0.0:
                similarities.append({
                    'doc_id': doc_id,
                    'score': score,
                    'metadata': self.metadata[doc_id]['metadata'],
                    'content': self.metadata[doc_id]['content']
                })
        
        # Sort by score and return top K
        similarities.sort(key=lambda x: x['score'], reverse=True)
        return similarities[:top_k]
    
    def get_document(self, doc_id: str) -> Dict[str, Any]:
        """
        Get a document by ID
        
        Args:
            doc_id: Document identifier
            
        Returns:
            Document data or None
        """
        if doc_id in self.metadata:
            return {
                'id': doc_id,
                'vector': self.vectors[doc_id],
                'content': self.metadata[doc_id]['content'],
                'metadata': self.metadata[doc_id]['metadata']
            }
        return None
    
    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document from the database
        
        Args:
            doc_id: Document identifier
            
        Returns:
            True if deleted, False if not found
        """
        if doc_id in self.vectors:
            del self.vectors[doc_id]
            del self.metadata[doc_id]
            self._save()
            return True
        return False
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """
        Get all documents in the database
        
        Returns:
            List of all documents
        """
        documents = []
        for doc_id in self.vectors.keys():
            doc = self.get_document(doc_id)
            if doc:
                documents.append(doc)
        return documents
    
    def clear(self) -> None:
        """Clear all documents from the database"""
        self.vectors = {}
        self.metadata = {}
        self._save()
    
    def _create_simple_vector(self, text: str) -> List[float]:
        """
        Create a simple vector from text
        In production, use actual embedding models
        
        Args:
            text: Text to vectorize
            
        Returns:
            Vector representation
        """
        # Simple implementation: use character frequency
        # In production, use sentence-transformers or similar
        text = text.lower()
        vector = [0.0] * 100
        
        for i, char in enumerate(text[:100]):
            vector[i] = ord(char) / 256.0
        
        return vector
    
    def _calculate_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Similarity score (0.0 to 1.0)
        """
        if not vec1 or not vec2:
            return 0.0
        
        # Ensure vectors are same length
        min_len = min(len(vec1), len(vec2))
        vec1 = vec1[:min_len]
        vec2 = vec2[:min_len]
        
        # Calculate dot product
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        
        # Calculate magnitudes
        mag1 = (sum(a * a for a in vec1) ** 0.5) or 1.0
        mag2 = (sum(b * b for b in vec2) ** 0.5) or 1.0
        
        # Cosine similarity
        similarity = dot_product / (mag1 * mag2) if (mag1 * mag2) > 0 else 0.0
        
        # Normalize to 0-1 range
        return (similarity + 1.0) / 2.0
    
    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now()
    
    def _save(self) -> None:
        """Save database to file"""
        try:
            data = {
                'vectors': {k: v for k, v in self.vectors.items()},
                'metadata': self.metadata
            }
            
            with open(os.path.join(self.db_path, 'db.json'), 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving vector database: {e}")
    
    def _load(self) -> None:
        """Load database from file"""
        db_file = os.path.join(self.db_path, 'db.json')
        
        if os.path.exists(db_file):
            try:
                with open(db_file, 'r') as f:
                    data = json.load(f)
                    self.vectors = data.get('vectors', {})
                    self.metadata = data.get('metadata', {})
            except Exception as e:
                print(f"Error loading vector database: {e}")
