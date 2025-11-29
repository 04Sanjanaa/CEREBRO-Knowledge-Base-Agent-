"""
LLM Service - OpenAI Integration
Provides intelligent responses using OpenAI GPT models
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self, api_key=None, model="gpt-3.5-turbo"):
        """Initialize OpenAI client"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        
        if not self.api_key:
            self.client = None
            self.enabled = False
        else:
            self.client = OpenAI(api_key=self.api_key)
            self.enabled = True
    
    def generate_response(self, query, documents, top_k=3):
        """
        Generate intelligent response using LLM
        Args:
            query: User question
            documents: List of relevant documents
            top_k: Number of top documents to include
        Returns:
            dict with response and metadata
        """
        if not self.enabled:
            return {
                'success': False,
                'error': 'OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.'
            }
        
        try:
            # Format documents for context
            doc_context = self._format_documents(documents[:top_k])
            
            # Create system prompt
            system_prompt = """You are CEREBRO, a helpful corporate knowledge base assistant. 
Your role is to answer employee questions about company policies accurately and concisely.
Use the provided company documents to answer questions.
If information is not in the documents, say you don't have that information.
Keep responses clear, professional, and well-organized."""
            
            # Create user prompt
            user_prompt = f"""Question: {query}

Relevant Company Documents:
{doc_context}

Please provide a helpful answer based on the documents above."""
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            
            return {
                'success': True,
                'response': answer,
                'model': self.model,
                'tokens_used': response.usage.total_tokens
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'LLM Error: {str(e)}'
            }
    
    def _format_documents(self, documents):
        """Format documents for LLM context"""
        if not documents:
            return "No relevant documents found."
        
        formatted = []
        for doc in documents:
            formatted.append(f"""
Document: {doc.get('title', 'Unknown')}
Category: {doc.get('section', 'General')}
Content:
{doc.get('content', 'No content')}
---""")
        
        return '\n'.join(formatted)


# Initialize default service
llm_service = LLMService()
