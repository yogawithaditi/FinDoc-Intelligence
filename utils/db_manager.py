#!/usr/bin/env python3
"""
Database Manager - Conversation History & Financial Data Storage
=================================================================

Manages:
1. SQLite - Conversation history and chat sessions
2. DuckDB - Financial metrics and analytics

Author: Built for FinDoc Intelligence project
"""

import sqlite3
import duckdb
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import json


class DatabaseManager:
    """
    Manages all database operations for the application.
    """
    
    def __init__(self, db_dir: str = "data/db"):
        """
        Initialize database connections.
        
        Args:
            db_dir: Directory to store database files
        """
        self.db_dir = Path(db_dir)
        self.db_dir.mkdir(parents=True, exist_ok=True)
        
        # SQLite for conversations
        self.sqlite_path = self.db_dir / "conversations.db"
        self.init_sqlite()
        
        # DuckDB for financial analytics
        self.duckdb_path = self.db_dir / "financial_data.duckdb"
        self.duckdb_conn = duckdb.connect(str(self.duckdb_path))
        self.init_duckdb()
        
        print("✅ Database connections initialized")
    
    
    def init_sqlite(self):
        """Initialize SQLite database with required tables."""
        conn = sqlite3.connect(self.sqlite_path)
        cursor = conn.cursor()
        
        # Create conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_message TEXT,
                assistant_message TEXT,
                document_name TEXT,
                message_type TEXT
            )
        """)
        
        # Create documents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_type TEXT NOT NULL,
                upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                processed BOOLEAN DEFAULT 0,
                text_length INTEGER,
                document_type TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ SQLite tables initialized")
    
    
    def init_duckdb(self):
        """Initialize DuckDB with financial data schema."""
        
        # Create financial metrics table
        self.duckdb_conn.execute("""
            CREATE TABLE IF NOT EXISTS financial_metrics (
                id INTEGER PRIMARY KEY,
                document_id INTEGER,
                company_name VARCHAR,
                registration_number VARCHAR,
                lei_code VARCHAR,
                duns_number VARCHAR,
                credit_score DECIMAL,
                credit_rating VARCHAR,
                revenue DECIMAL,
                profit DECIMAL,
                total_assets DECIMAL,
                total_liabilities DECIMAL,
                debt_to_equity DECIMAL,
                current_ratio DECIMAL,
                extracted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("✅ DuckDB tables initialized")
    
    
    # ============================================================
    # CONVERSATION MANAGEMENT (SQLite)
    # ============================================================
    
    def save_conversation(
        self, 
        session_id: str, 
        user_message: str, 
        assistant_message: str,
        document_name: Optional[str] = None,
        message_type: str = "chat"
    ) -> int:
        """
        Save a conversation exchange.
        
        Args:
            session_id: Unique session identifier
            user_message: User's message
            assistant_message: Assistant's response
            document_name: Name of document being discussed
            message_type: Type of message (chat, query, extraction)
            
        Returns:
            Conversation ID
        """
        conn = sqlite3.connect(self.sqlite_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO conversations 
            (session_id, user_message, assistant_message, document_name, message_type)
            VALUES (?, ?, ?, ?, ?)
        """, (session_id, user_message, assistant_message, document_name, message_type))
        
        conversation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return conversation_id
    
    
    def get_conversation_history(
        self, 
        session_id: str, 
        limit: int = 50
    ) -> List[Dict]:
        """
        Retrieve conversation history for a session.
        
        Args:
            session_id: Session identifier
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of conversation dictionaries
        """
        conn = sqlite3.connect(self.sqlite_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timestamp, user_message, assistant_message, document_name, message_type
            FROM conversations
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (session_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Convert to list of dicts
        history = []
        for row in rows:
            history.append({
                'timestamp': row[0],
                'user_message': row[1],
                'assistant_message': row[2],
                'document_name': row[3],
                'message_type': row[4]
            })
        
        return list(reversed(history))  # Return in chronological order
    
    
    def clear_session_history(self, session_id: str):
        """Clear all conversations for a session."""
        conn = sqlite3.connect(self.sqlite_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM conversations WHERE session_id = ?", (session_id,))
        
        conn.commit()
        conn.close()
        print(f"🗑️ Cleared history for session: {session_id}")
    
    
    # ============================================================
    # DOCUMENT MANAGEMENT (SQLite)
    # ============================================================
    
    def save_document_metadata(
        self,
        filename: str,
        file_type: str,
        text_length: int = 0,
        document_type: Optional[str] = None
    ) -> int:
        """
        Save document metadata.
        
        Args:
            filename: Name of the uploaded file
            file_type: Type of file (pdf, image)
            text_length: Length of extracted text
            document_type: Classified document type
            
        Returns:
            Document ID
        """
        conn = sqlite3.connect(self.sqlite_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO documents 
            (filename, file_type, text_length, document_type, processed)
            VALUES (?, ?, ?, ?, 1)
        """, (filename, file_type, text_length, document_type))
        
        doc_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return doc_id
    
    
    def get_uploaded_documents(self, limit: int = 20) -> List[Dict]:
        """Get list of uploaded documents."""
        conn = sqlite3.connect(self.sqlite_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, filename, file_type, upload_timestamp, document_type
            FROM documents
            ORDER BY upload_timestamp DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        documents = []
        for row in rows:
            documents.append({
                'id': row[0],
                'filename': row[1],
                'file_type': row[2],
                'upload_timestamp': row[3],
                'document_type': row[4]
            })
        
        return documents
    
    
    # ============================================================
    # FINANCIAL DATA MANAGEMENT (DuckDB)
    # ============================================================
    
    def save_financial_metrics(self, metrics: Dict) -> int:
        """
        Save extracted financial metrics.
        
        Args:
            metrics: Dictionary of financial metrics
            
        Returns:
            Row ID
        """
        # Build INSERT query dynamically based on available metrics
        columns = []
        values = []
        
        metric_mapping = {
            'document_id': 'document_id',
            'company_name': 'company_name',
            'registration_number': 'registration_number',
            'lei_code': 'lei_code',
            'duns_number': 'duns_number',
            'credit_score': 'credit_score',
            'credit_rating': 'credit_rating',
            'revenue': 'revenue',
            'profit': 'profit',
            'total_assets': 'total_assets',
            'total_liabilities': 'total_liabilities',
            'debt_to_equity': 'debt_to_equity',
            'current_ratio': 'current_ratio'
        }
        
        for key, col_name in metric_mapping.items():
            if key in metrics and metrics[key] is not None:
                columns.append(col_name)
                values.append(metrics[key])
        
        if not columns:
            return -1
        
        placeholders = ','.join(['?' for _ in columns])
        query = f"""
            INSERT INTO financial_metrics ({','.join(columns)})
            VALUES ({placeholders})
        """
        
        self.duckdb_conn.execute(query, values)
        
        # Get last inserted ID
        result = self.duckdb_conn.execute("SELECT MAX(id) FROM financial_metrics").fetchone()
        return result[0] if result else -1
    
    
    def query_financial_data(self, sql_query: str) -> Tuple[List, List]:
        """
        Execute SQL query on financial data.
        
        Args:
            sql_query: SQL query string
            
        Returns:
            Tuple of (column_names, rows)
        """
        try:
            result = self.duckdb_conn.execute(sql_query).fetchall()
            columns = [desc[0] for desc in self.duckdb_conn.description]
            return columns, result
        except Exception as e:
            print(f"❌ Query error: {e}")
            return [], []
    
    
    def get_financial_summary(self, limit: int = 10) -> List[Dict]:
        """Get summary of all financial records."""
        query = f"""
            SELECT 
                company_name,
                credit_score,
                credit_rating,
                revenue,
                debt_to_equity,
                extracted_date
            FROM financial_metrics
            ORDER BY extracted_date DESC
            LIMIT {limit}
        """
        
        columns, rows = self.query_financial_data(query)
        
        summary = []
        for row in rows:
            summary.append(dict(zip(columns, row)))
        
        return summary
    
    
    def close(self):
        """Close all database connections."""
        if hasattr(self, 'duckdb_conn'):
            self.duckdb_conn.close()
        print("🔒 Database connections closed")


# Singleton instance
_db_instance = None

def get_db() -> DatabaseManager:
    """Get or create database manager instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager()
    return _db_instance