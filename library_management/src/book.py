"""Book model and management for the library system."""

from datetime import datetime
from typing import Optional


class Book:
    """Represents a book in the library."""
    
    def __init__(
        self,
        isbn: str,
        title: str,
        author: str,
        publisher: str,
        publication_year: int,
        total_copies: int = 1
    ):
        """Initialize a Book object.
        
        Args:
            isbn: International Standard Book Number
            title: Title of the book
            author: Author of the book
            publisher: Publisher of the book
            publication_year: Year of publication
            total_copies: Total copies available
        """
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.publication_year = publication_year
        self.total_copies = total_copies
        self.available_copies = total_copies
        self.created_at = datetime.now()
    
    def __repr__(self) -> str:
        """String representation of the book."""
        return f"Book({self.title}, {self.author}, {self.isbn})"
    
    def borrow_copy(self) -> bool:
        """Borrow a copy of the book.
        
        Returns:
            True if borrowing was successful, False otherwise
        """
        if self.available_copies > 0:
            self.available_copies -= 1
            return True
        return False
    
    def return_copy(self) -> bool:
        """Return a copy of the book.
        
        Returns:
            True if return was successful, False otherwise
        """
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            return True
        return False
    
    def get_availability(self) -> dict:
        """Get availability information of the book.
        
        Returns:
            Dictionary with availability details
        """
        return {
            "total": self.total_copies,
            "available": self.available_copies,
            "borrowed": self.total_copies - self.available_copies
        }
