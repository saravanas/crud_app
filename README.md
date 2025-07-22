# CRUD Application with GUI

A Python-based CRUD (Create, Read, Update, Delete) application with a graphical user interface built using Tkinter. The application follows best practices for data management, has a clean architecture, and is maintainable for future development.

## Features

- Create, Read, Update, and Delete records
- SQLite database for data storage
- User-friendly graphical interface
- Input validation
- Error handling
- Logging
- Unit tests

## Project Structure

```
.
├── src/
│   ├── models/
│   │   └── database.py
│   ├── ui/
│   │   └── app.py
│   └── main.py
├── tests/
│   └── test_database.py
└── README.md
```

## Requirements

- Python 3.x
- Tkinter (usually comes with Python)
- SQLite3 (usually comes with Python)

## Installation

1. Clone the repository
2. Navigate to the project directory
3. (Optional) Create a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

## Running the Application

1. Navigate to the `src` directory
2. Run the main script:
   ```
   python main.py
   ```

## Running Tests

From the project root directory:
```
python -m unittest discover tests
```

## Features

- **Create Records**: Add new records with name, email, and phone number
- **Read Records**: View all records in a scrollable table
- **Update Records**: Select and modify existing records
- **Delete Records**: Remove records from the database
- **Input Validation**: Ensures data integrity
- **Error Handling**: Graceful handling of errors with user feedback
- **Logging**: Tracks operations and errors for debugging

## Code Structure

- `database.py`: Handles all database operations
- `app.py`: Contains the GUI implementation
- `main.py`: Application entry point
- `test_database.py`: Unit tests for database operations

## Best Practices Implemented

- Separation of concerns (data, UI, business logic)
- Proper error handling and validation
- Comprehensive logging
- Unit testing
- PEP 8 style guidelines
- Type hints for better code readability
- Documentation (comments, docstrings, README)
