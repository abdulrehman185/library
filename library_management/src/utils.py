"""Utility functions for the library system."""

from datetime import datetime


def format_date(date_obj: datetime) -> str:
    """Format datetime object to string.
    
    Args:
        date_obj: Datetime object
        
    Returns:
        Formatted date string
    """
    if isinstance(date_obj, str):
        return date_obj
    return date_obj.strftime("%Y-%m-%d %H:%M:%S")


def validate_isbn(isbn: str) -> bool:
    """Validate ISBN format (simplified).
    
    Args:
        isbn: ISBN string
        
    Returns:
        True if valid, False otherwise
    """
    return isinstance(isbn, str) and len(isbn) >= 10


def validate_email(email: str) -> bool:
    """Validate email format (simplified).
    
    Args:
        email: Email string
        
    Returns:
        True if valid, False otherwise
    """
    return "@" in email and "." in email


def generate_member_id() -> str:
    """Generate a unique member ID.
    
    Returns:
        Generated member ID
    """
    import uuid
    return f"MEM{uuid.uuid4().hex[:8].upper()}"
