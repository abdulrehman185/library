"""Main library management system."""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from src.book import Book
from src.member import Member
from src.database import Database


class Library:
    """Main library management system."""
    
    BORROWING_PERIOD_DAYS = 14
    DAILY_FINE = 1.0  # Fine per day for overdue books
    
    def __init__(self, db_path: str = "data/library.db"):
        """Initialize the library system.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.database = Database(db_path)
        self.books: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}
        self._load_from_db()
    
    def _load_from_db(self) -> None:
        """Load books and members from database into memory."""
        conn = self.database.get_connection()
        cursor = conn.cursor()
        
        # Load books
        cursor.execute('SELECT * FROM books')
        for row in cursor.fetchall():
            book = Book(
                row['isbn'], row['title'], row['author'],
                row['publisher'], row['publication_year'], row['total_copies']
            )
            book.available_copies = row['available_copies']
            self.books[row['isbn']] = book
        
        # Load members
        cursor.execute('SELECT * FROM members')
        for row in cursor.fetchall():
            member = Member(row['member_id'], row['name'], row['email'], 
                           row['phone'], row['address'])
            member.is_active = bool(row['is_active'])
            member.total_fines = row['total_fines']
            self.members[row['member_id']] = member
        
        conn.close()
    
    def add_book(self, isbn: str, title: str, author: str, 
                 publisher: str, publication_year: int, total_copies: int = 1) -> bool:
        """Add a book to the library.
        
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
        if isbn in self.books:
            return False
        
        if self.database.add_book(isbn, title, author, publisher, publication_year, total_copies):
            book = Book(isbn, title, author, publisher, publication_year, total_copies)
            self.books[isbn] = book
            return True
        return False
    
    def search_books(self, query: str) -> List[Book]:
        """Search books by title or author.
        
        Args:
            query: Search query
            
        Returns:
            List of matching books
        """
        results = self.database.search_books(query)
        return [self.books[row['isbn']] for row in results if row['isbn'] in self.books]
    
    def add_member(self, member_id: str, name: str, email: str, 
                   phone: str, address: str) -> bool:
        """Add a member to the library.
        
        Args:
            member_id: Member ID
            name: Member name
            email: Member email
            phone: Member phone
            address: Member address
            
        Returns:
            True if successful, False otherwise
        """
        if member_id in self.members:
            return False
        
        if self.database.add_member(member_id, name, email, phone, address):
            member = Member(member_id, name, email, phone, address)
            self.members[member_id] = member
            return True
        return False
    
    def borrow_book(self, member_id: str, isbn: str) -> tuple[bool, str]:
        """Borrow a book from the library.
        
        Args:
            member_id: Member ID
            isbn: Book ISBN
            
        Returns:
            Tuple of (success, message)
        """
        if member_id not in self.members:
            return False, "Member not found"
        
        if isbn not in self.books:
            return False, "Book not found"
        
        member = self.members[member_id]
        book = self.books[isbn]
        
        if not member.is_active:
            return False, "Member is not active"
        
        if not book.borrow_copy():
            return False, "Book not available"
        
        member.add_borrowed_book(isbn)
        due_date = datetime.now() + timedelta(days=self.BORROWING_PERIOD_DAYS)
        
        if self.database.record_borrowing(member_id, isbn, due_date):
            return True, f"Book '{book.title}' borrowed successfully. Due date: {due_date.date()}"
        
        # Revert changes if database operation failed
        book.return_copy()
        member.remove_borrowed_book(isbn)
        return False, "Failed to record borrowing"
    
    def return_book(self, member_id: str, isbn: str) -> tuple[bool, str]:
        """Return a book to the library.
        
        Args:
            member_id: Member ID
            isbn: Book ISBN
            
        Returns:
            Tuple of (success, message)
        """
        if member_id not in self.members:
            return False, "Member not found"
        
        if isbn not in self.books:
            return False, "Book not found"
        
        member = self.members[member_id]
        book = self.books[isbn]
        
        if not member.remove_borrowed_book(isbn):
            return False, "This book was not borrowed by this member"
        
        book.return_copy()
        fine = self._calculate_fine(member_id, isbn)
        
        if fine > 0:
            member.add_fine(fine)
        
        if self.database.record_return(member_id, isbn, fine):
            message = f"Book '{book.title}' returned successfully"
            if fine > 0:
                message += f". Fine applied: ${fine:.2f}"
            return True, message
        
        return False, "Failed to record return"
    
    def _calculate_fine(self, member_id: str, isbn: str) -> float:
        """Calculate fine for an overdue book.
        
        Args:
            member_id: Member ID
            isbn: Book ISBN
            
        Returns:
            Fine amount
        """
        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT due_date FROM borrowing_records
            WHERE member_id = ? AND isbn = ? AND return_date IS NULL
            ORDER BY borrow_date DESC LIMIT 1
        ''', (member_id, isbn))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return 0.0
        
        due_date = datetime.fromisoformat(result['due_date'])
        if datetime.now() > due_date:
            days_overdue = (datetime.now() - due_date).days
            return days_overdue * self.DAILY_FINE
        
        return 0.0
    
    def get_library_stats(self) -> Dict:
        """Get library statistics.
        
        Returns:
            Dictionary with library statistics
        """
        total_books = sum(book.total_copies for book in self.books.values())
        borrowed_books = sum(book.total_copies - book.available_copies for book in self.books.values())
        
        return {
            "total_members": len(self.members),
            "active_members": sum(1 for m in self.members.values() if m.is_active),
            "total_books_inventory": total_books,
            "borrowed_books": borrowed_books,
            "available_books": total_books - borrowed_books,
            "unique_titles": len(self.books)
        }
