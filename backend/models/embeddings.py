"""
Embeddings and embedding-related utilities
"""

from typing import List, Tuple
import json
import os


class Embeddings:
    """Handles document embeddings for semantic search"""
    
    def __init__(self, model_name: str = 'simple'):
        """
        Initialize embeddings
        
        Args:
            model_name: Name of the embedding model
        """
        self.model_name = model_name
        self.embedding_cache = {}
    
    def embed_text(self, text: str) -> List[float]:
        """
        Create an embedding for text
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        # Check cache first
        if text in self.embedding_cache:
            return self.embedding_cache[text]
        
        # Create simple embedding based on character frequencies
        embedding = self._create_simple_embedding(text)
        
        # Cache the result
        self.embedding_cache[text] = embedding
        
        return embedding
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for multiple texts
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        return [self.embed_text(text) for text in texts]
    
    def similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0.0 to 1.0)
        """
        emb1 = self.embed_text(text1)
        emb2 = self.embed_text(text2)
        
        return self._cosine_similarity(emb1, emb2)
    
    def batch_similarity(self, text: str, texts: List[str]) -> List[float]:
        """
        Calculate similarity of one text against many
        
        Args:
            text: Query text
            texts: List of texts to compare against
            
        Returns:
            List of similarity scores
        """
        return [self.similarity(text, t) for t in texts]
    
    def _create_simple_embedding(self, text: str, dim: int = 128) -> List[float]:
        """
        Create a simple embedding for text
        
        In production, use actual embedding models like:
        - sentence-transformers
        - OpenAI embeddings API
        - Hugging Face embeddings
        
        Args:
            text: Text to embed
            dim: Embedding dimension
            
        Returns:
            Embedding vector
        """
        text = text.lower()
        
        # Initialize embedding vector
        embedding = [0.0] * dim
        
        # Character frequency-based embedding
        for i, char in enumerate(text[:dim]):
            embedding[i] = (ord(char) % 256) / 256.0
        
        # Word frequency bonus for important words
        keywords = ['policy', 'leave', 'work', 'remote', 'support', 'expense', 'onboard', 'hr']
        for keyword in keywords:
            if keyword in text:
                for i in range(min(dim, len(keyword))):
                    embedding[i] += 0.1
        
        # Normalize
        magnitude = (sum(x * x for x in embedding) ** 0.5) or 1.0
        embedding = [x / magnitude for x in embedding]
        
        return embedding
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Similarity score
        """
        if not vec1 or not vec2:
            return 0.0
        
        # Ensure same length
        min_len = min(len(vec1), len(vec2))
        vec1 = vec1[:min_len]
        vec2 = vec2[:min_len]
        
        # Dot product
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        
        # Magnitudes
        mag1 = (sum(a * a for a in vec1) ** 0.5) or 1.0
        mag2 = (sum(b * b for b in vec2) ** 0.5) or 1.0
        
        # Cosine similarity
        similarity = dot_product / (mag1 * mag2) if (mag1 * mag2) > 0 else 0.0
        
        # Normalize to 0-1
        return (similarity + 1.0) / 2.0
    
    def clear_cache(self) -> None:
        """Clear embedding cache"""
        self.embedding_cache.clear()
