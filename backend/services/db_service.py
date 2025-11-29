"""
Simple SQLite DB service for persisting documents and query logs.
"""
import sqlite3
import os
from typing import List, Dict, Any, Optional


class DBService:
    def __init__(self, db_path: str = './data/kb_agent.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                title TEXT,
                section TEXT,
                content TEXT
            )
            '''
        )

        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS logs (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                query TEXT,
                answered INTEGER,
                sources TEXT
            )
            '''
        )

        self.conn.commit()

    # Documents
    def get_documents(self) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute('SELECT id, title, section, content FROM documents')
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        cur = self.conn.cursor()
        for doc in documents:
            cur.execute(
                'INSERT OR REPLACE INTO documents (id, title, section, content) VALUES (?, ?, ?, ?)',
                (doc.get('id'), doc.get('title'), doc.get('section'), doc.get('content'))
            )
        self.conn.commit()

    # Logs
    def add_log(self, log_entry: Dict[str, Any]) -> None:
        cur = self.conn.cursor()
        import json
        cur.execute(
            'INSERT OR REPLACE INTO logs (id, timestamp, query, answered, sources) VALUES (?, ?, ?, ?, ?)',
            (
                log_entry.get('id'),
                log_entry.get('timestamp'),
                log_entry.get('query'),
                int(bool(log_entry.get('answered'))),
                json.dumps(log_entry.get('sources', []))
            )
        )
        self.conn.commit()

    def get_logs(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        q = 'SELECT id, timestamp, query, answered, sources FROM logs ORDER BY timestamp DESC'
        if limit:
            q += f' LIMIT {int(limit)}'
        cur.execute(q)
        rows = cur.fetchall()
        import json
        out = []
        for r in rows:
            sources = []
            try:
                sources = json.loads(r['sources']) if r['sources'] else []
            except Exception:
                sources = []
            out.append({
                'id': r['id'],
                'timestamp': r['timestamp'],
                'query': r['query'],
                'answered': bool(r['answered']),
                'sources': sources
            })
        return out

    def clear_logs(self) -> None:
        cur = self.conn.cursor()
        cur.execute('DELETE FROM logs')
        self.conn.commit()

    def export_logs_json(self) -> str:
        import json
        return json.dumps(self.get_logs(), indent=2)
