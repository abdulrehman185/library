"""Member model and management for the library system."""

from datetime import datetime
from typing import Optional


class Member:
    """Represents a member of the library."""
    
    def __init__(
        self,
        member_id: str,
        name: str,
        email: str,
        phone: str,
        address: str
    ):
        """Initialize a Member object.
        
        Args:
            member_id: Unique member identifier
            name: Full name of the member
            email: Email address
            phone: Phone number
            address: Physical address
        """
        self.member_id = member_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.membership_date = datetime.now()
        self.is_active = True
        self.borrowed_books = []
        self.total_fines = 0.0
    
    def __repr__(self) -> str:
        """String representation of the member."""
        return f"Member({self.member_id}, {self.name})"
    
    def add_borrowed_book(self, book_id: str) -> None:
        """Add a borrowed book to member's list.
        
        Args:
            book_id: ID of the borrowed book
        """
        if book_id not in self.borrowed_books:
            self.borrowed_books.append(book_id)
    
    def remove_borrowed_book(self, book_id: str) -> bool:
        """Remove a returned book from member's list.
        
        Args:
            book_id: ID of the returned book
            
        Returns:
            True if book was in the list, False otherwise
        """
        if book_id in self.borrowed_books:
            self.borrowed_books.remove(book_id)
            return True
        return False
    
    def get_borrowed_count(self) -> int:
        """Get the count of currently borrowed books.
        
        Returns:
            Number of borrowed books
        """
        return len(self.borrowed_books)
    
    def add_fine(self, amount: float) -> None:
        """Add a fine to the member's account.
        
        Args:
            amount: Fine amount to add
        """
        self.total_fines += amount
    
    def pay_fine(self, amount: float) -> bool:
        """Pay a fine from the member's account.
        
        Args:
            amount: Fine amount to pay
            
        Returns:
            True if payment was successful, False if amount exceeds fine
        """
        if amount <= self.total_fines:
            self.total_fines -= amount
            return True
        return False
