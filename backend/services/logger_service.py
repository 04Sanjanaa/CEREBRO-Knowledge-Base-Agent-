"""
Logger service for query logging and analytics
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any
import uuid


class LoggerService:
    """Handles query logging and analytics. Uses DBService when provided, else falls back to JSON file.
    """

    def __init__(self, log_dir: str = './logs', db_service=None):
        """
        Initialize the logger service

        Args:
            log_dir: Directory to store log files (used if db_service is None)
            db_service: Optional DBService instance for persistence
        """
        self.log_dir = log_dir
        self.log_file = os.path.join(log_dir, 'queries.json')
        self.queries = []
        self.db = db_service

        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)

        # Load existing logs (from DB if available)
        if self.db:
            try:
                self.queries = self.db.get_logs() or []
            except Exception:
                self.queries = []
        else:
            self._load_logs()
    
    def log_query(self, query: str, answered: bool, sources: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Log a user query
        
        Args:
            query: User query text
            answered: Whether the query was answered
            sources: List of source documents used
            
        Returns:
            Log entry
        """
        log_entry = {
            'id': str(uuid.uuid4())[:8],
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'answered': answered,
            'sources': sources
        }
        
        self.queries.append(log_entry)

        # Persist
        if self.db:
            try:
                self.db.add_log(log_entry)
            except Exception as e:
                # fallback to file
                self._save_logs()
        else:
            self._save_logs()

        return log_entry
    
    def get_logs(self, limit: int = None) -> List[Dict[str, Any]]:
        """
        Get query logs
        
        Args:
            limit: Maximum number of logs to return (None for all)
            
        Returns:
            List of query logs
        """
        if self.db:
            return self.db.get_logs(limit)
        logs = sorted(self.queries, key=lambda x: x['timestamp'], reverse=True)
        return logs[:limit] if limit else logs
    
    def get_logs_by_date(self, date: str) -> List[Dict[str, Any]]:
        """
        Get logs from a specific date
        
        Args:
            date: Date in format YYYY-MM-DD
            
        Returns:
            List of logs from that date
        """
        if self.db:
            return [log for log in self.db.get_logs() if log['timestamp'].startswith(date)]
        return [log for log in self.queries if log['timestamp'].startswith(date)]
    
    def get_analytics(self) -> Dict[str, Any]:
        """
        Get analytics from logs
        
        Returns:
            Analytics data
        """
        logs = self.get_logs()
        total_queries = len(logs)
        answered_queries = sum(1 for log in logs if log.get('answered', False))
        
        # Calculate response rate
        response_rate = (answered_queries / total_queries * 100) if total_queries > 0 else 0
        
        # Count source usage
        source_usage = {}
        for log in logs:
            for source in log.get('sources', []):
                title = source.get('title', 'Unknown')
                source_usage[title] = source_usage.get(title, 0) + 1
        
        # Get top queries
        query_frequency = {}
        for log in logs:
            query = log['query'].lower()
            query_frequency[query] = query_frequency.get(query, 0) + 1
        
        top_queries = sorted(query_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_queries': total_queries,
            'answered_queries': answered_queries,
            'response_rate': f"{response_rate:.1f}%",
            'top_sources': sorted(source_usage.items(), key=lambda x: x[1], reverse=True)[:3],
            'top_queries': top_queries,
            'first_query': logs[-1]['timestamp'] if logs else None,
            'last_query': logs[0]['timestamp'] if logs else None
        }
    
    def clear_logs(self) -> None:
        """Clear all logs"""
        self.queries = []
        if self.db:
            self.db.clear_logs()
        else:
            self._save_logs()
    
    def export_logs(self, format: str = 'json') -> str:
        """
        Export logs in specified format
        
        Args:
            format: Export format (json or csv)
            
        Returns:
            Exported data as string
        """
        if format == 'json':
            if self.db:
                return self.db.export_logs_json()
            return json.dumps(self.queries, indent=2)
        elif format == 'csv':
            import csv
            from io import StringIO
            
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=['id', 'timestamp', 'query', 'answered', 'sources'])
            writer.writeheader()
            
            for log in self.queries:
                log_copy = log.copy()
                log_copy['sources'] = json.dumps(log_copy['sources'])
                writer.writerow(log_copy)
            
            return output.getvalue()
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _load_logs(self) -> None:
        """Load logs from file"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    self.queries = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.queries = []
    
    def _save_logs(self) -> None:
        """Save logs to file"""
        try:
            with open(self.log_file, 'w') as f:
                json.dump(self.queries, f, indent=2)
        except IOError as e:
            print(f"Error saving logs: {e}")
