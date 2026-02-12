# Library Management System

A comprehensive Python-based library management system for managing books, members, and borrowing/returning operations.

## Features

- **Book Management**: Add, update, and remove books from the library inventory
- **Member Management**: Register and manage library members
- **Borrowing System**: Track book borrowing and returning with due dates
- **Fine Management**: Calculate and manage fines for overdue books
- **Search Functionality**: Search books by title, author, or ISBN
- **Reports**: Generate library statistics and reports

## Project Structure

```
library_management/
├── src/
│   ├── __init__.py
│   ├── book.py           # Book model and management
│   ├── member.py         # Member model and management
│   ├── library.py        # Main library system
│   ├── database.py       # Database operations
│   └── utils.py          # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_book.py
│   ├── test_member.py
│   └── test_library.py
├── main.py               # Entry point
├── requirements.txt      # Dependencies
└── README.md
```

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

## Requirements

- Python 3.8+
- SQLite3 (included with Python)

## Testing

Run tests using pytest:
```bash
pytest tests/
```

## License

MIT License

# library
