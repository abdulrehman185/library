"""Library Management System - Main Application."""

from src.library import Library
from src.utils import validate_isbn, validate_email, generate_member_id


def display_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("LIBRARY MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Add Book")
    print("2. Add Member")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Search Books")
    print("6. View Member Details")
    print("7. View Library Statistics")
    print("8. Exit")
    print("="*50)


def add_book(library: Library):
    """Add a new book to the library."""
    print("\n--- Add New Book ---")
    try:
        isbn = input("Enter ISBN: ").strip()
        if not validate_isbn(isbn):
            print("Invalid ISBN format!")
            return
        
        title = input("Enter Title: ").strip()
        author = input("Enter Author: ").strip()
        publisher = input("Enter Publisher: ").strip()
        year = int(input("Enter Publication Year: "))
        copies = int(input("Enter Number of Copies: "))
        
        if library.add_book(isbn, title, author, publisher, year, copies):
            print("✓ Book added successfully!")
        else:
            print("✗ Failed to add book. ISBN may already exist.")
    except ValueError:
        print("✗ Invalid input!")


def add_member(library: Library):
    """Add a new member to the library."""
    print("\n--- Add New Member ---")
    try:
        member_id = generate_member_id()
        name = input("Enter Full Name: ").strip()
        email = input("Enter Email: ").strip()
        
        if not validate_email(email):
            print("Invalid email format!")
            return
        
        phone = input("Enter Phone Number: ").strip()
        address = input("Enter Address: ").strip()
        
        if library.add_member(member_id, name, email, phone, address):
            print(f"✓ Member added successfully! Member ID: {member_id}")
        else:
            print("✗ Failed to add member.")
    except ValueError:
        print("✗ Invalid input!")


def borrow_book(library: Library):
    """Borrow a book from the library."""
    print("\n--- Borrow Book ---")
    try:
        member_id = input("Enter Member ID: ").strip()
        isbn = input("Enter Book ISBN: ").strip()
        
        success, message = library.borrow_book(member_id, isbn)
        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")
    except ValueError:
        print("✗ Invalid input!")


def return_book(library: Library):
    """Return a book to the library."""
    print("\n--- Return Book ---")
    try:
        member_id = input("Enter Member ID: ").strip()
        isbn = input("Enter Book ISBN: ").strip()
        
        success, message = library.return_book(member_id, isbn)
        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")
    except ValueError:
        print("✗ Invalid input!")


def search_books(library: Library):
    """Search for books in the library."""
    print("\n--- Search Books ---")
    try:
        query = input("Enter search term (title or author): ").strip()
        books = library.search_books(query)
        
        if books:
            print(f"\nFound {len(books)} book(s):")
            print("-" * 50)
            for book in books:
                print(f"Title: {book.title}")
                print(f"Author: {book.author}")
                print(f"ISBN: {book.isbn}")
                print(f"Availability: {book.available_copies}/{book.total_copies} copies")
                print("-" * 50)
        else:
            print("No books found matching your search.")
    except ValueError:
        print("✗ Invalid input!")


def view_member_details(library: Library):
    """View details of a library member."""
    print("\n--- View Member Details ---")
    try:
        member_id = input("Enter Member ID: ").strip()
        
        if member_id in library.members:
            member = library.members[member_id]
            print(f"\nMember ID: {member.member_id}")
            print(f"Name: {member.name}")
            print(f"Email: {member.email}")
            print(f"Phone: {member.phone}")
            print(f"Address: {member.address}")
            print(f"Borrowed Books: {member.get_borrowed_count()}")
            print(f"Outstanding Fines: ${member.total_fines:.2f}")
        else:
            print("Member not found.")
    except ValueError:
        print("✗ Invalid input!")


def view_statistics(library: Library):
    """Display library statistics."""
    print("\n--- Library Statistics ---")
    stats = library.get_library_stats()
    
    print(f"Total Members: {stats['total_members']}")
    print(f"Active Members: {stats['active_members']}")
    print(f"Unique Titles: {stats['unique_titles']}")
    print(f"Total Books in Inventory: {stats['total_books_inventory']}")
    print(f"Books Borrowed: {stats['borrowed_books']}")
    print(f"Books Available: {stats['available_books']}")


def main():
    """Main application loop."""
    library = Library()
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == "1":
            add_book(library)
        elif choice == "2":
            add_member(library)
        elif choice == "3":
            borrow_book(library)
        elif choice == "4":
            return_book(library)
        elif choice == "5":
            search_books(library)
        elif choice == "6":
            view_member_details(library)
        elif choice == "7":
            view_statistics(library)
        elif choice == "8":
            print("Thank you for using Library Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
