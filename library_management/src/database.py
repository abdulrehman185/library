"""Database operations for the library system."""

import sqlite3
import os
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class Database:
    """Handle all database operations for the library system."""
    
    def __init__(self, db_path: str = "data/library.db"):
        """Initialize database connection.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
        self.init_db()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection.
        
        Returns:
            SQLite database connection
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self) -> None:
        """Initialize database with required tables."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create books table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                isbn TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                publisher TEXT,
                publication_year INTEGER,
                total_copies INTEGER DEFAULT 1,
                available_copies INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create members table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                member_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                address TEXT,
                membership_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                total_fines REAL DEFAULT 0.0
            )
        ''')
        
        # Create borrowing records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS borrowing_records (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id TEXT NOT NULL,
                isbn TEXT NOT NULL,
                borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date TIMESTAMP,
                return_date TIMESTAMP,
                fine_paid REAL DEFAULT 0.0,
                FOREIGN KEY (member_id) REFERENCES members(member_id),
                FOREIGN KEY (isbn) REFERENCES books(isbn)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_book(self, isbn: str, title: str, author: str, 
                 publisher: str, publication_year: int, total_copies: int = 1) -> bool:
        """Add a book to the database.
        
        Args:
            isbn: Book ISBN
            title: Book title
            author: Book author
            publisher: Book publisher
            publication_year: Year of publication
            total_copies: Total copies to add
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO books (isbn, title, author, publisher, publication_year, total_copies, available_copies)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (isbn, title, author, publisher, publication_year, total_copies, total_copies))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_book(self, isbn: str) -> Optional[Dict]:
        """Get book details from database.
        
        Args:
            isbn: Book ISBN
            
        Returns:
            Book record as dictionary or None
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE isbn = ?', (isbn,))
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None
    
    def search_books(self, query: str) -> List[Dict]:
        """Search books by title or author.
        
        Args:
            query: Search query
            
        Returns:
            List of matching books
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM books 
            WHERE title LIKE ? OR author LIKE ?
        ''', (f"%{query}%", f"%{query}%"))
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    
    def add_member(self, member_id: str, name: str, email: str, phone: str, address: str) -> bool:
        """Add a member to the database.
        
        Args:
            member_id: Member ID
            name: Member name
            email: Member email
            phone: Member phone
            address: Member address
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO members (member_id, name, email, phone, address)
                VALUES (?, ?, ?, ?, ?)
            ''', (member_id, name, email, phone, address))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_member(self, member_id: str) -> Optional[Dict]:
        """Get member details from database.
        
        Args:
            member_id: Member ID
            
        Returns:
            Member record as dictionary or None
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM members WHERE member_id = ?', (member_id,))
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None
    
    def record_borrowing(self, member_id: str, isbn: str, due_date: datetime) -> bool:
        """Record a book borrowing event.
        
        Args:
            member_id: Member ID
            isbn: Book ISBN
            due_date: Due date for return
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO borrowing_records (member_id, isbn, due_date)
                VALUES (?, ?, ?)
            ''', (member_id, isbn, due_date))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False
    
    def record_return(self, member_id: str, isbn: str, fine_paid: float = 0.0) -> bool:
        """Record a book return event.
        
        Args:
            member_id: Member ID
            isbn: Book ISBN
            fine_paid: Fine amount paid (if any)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE borrowing_records 
                SET return_date = CURRENT_TIMESTAMP, fine_paid = ?
                WHERE member_id = ? AND isbn = ? AND return_date IS NULL
            ''', (fine_paid, member_id, isbn))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False
