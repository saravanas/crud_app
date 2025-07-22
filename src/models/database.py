import sqlite3
import logging
from typing import List, Dict, Any, Optional

class Database:
    def __init__(self, db_file: str = "records.db"):
        """Initialize database connection."""
        self.db_file = db_file
        self.setup_logging()
        self.setup_database()
    
    def setup_logging(self):
        """Configure logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def setup_database(self):
        """Create the database and tables if they don't exist."""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
            self.logger.info("Database setup completed successfully")
        except sqlite3.Error as e:
            self.logger.error(f"Database setup error: {str(e)}")
            raise

    def create_record(self, data: Dict[str, Any]) -> int:
        """Create a new record in the database."""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO records (name, email, phone) VALUES (?, ?, ?)",
                    (data['name'], data['email'], data.get('phone', ''))
                )
                conn.commit()
                self.logger.info(f"Created record with ID: {cursor.lastrowid}")
                return cursor.lastrowid
        except sqlite3.Error as e:
            self.logger.error(f"Error creating record: {str(e)}")
            raise

    def read_record(self, record_id: int) -> Optional[Dict[str, Any]]:
        """Read a record from the database."""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM records WHERE id = ?", (record_id,))
                record = cursor.fetchone()
                if record:
                    return {
                        'id': record[0],
                        'name': record[1],
                        'email': record[2],
                        'phone': record[3],
                        'created_at': record[4]
                    }
                return None
        except sqlite3.Error as e:
            self.logger.error(f"Error reading record: {str(e)}")
            raise

    def read_all_records(self) -> List[Dict[str, Any]]:
        """Read all records from the database."""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM records")
                records = cursor.fetchall()
                return [{
                    'id': record[0],
                    'name': record[1],
                    'email': record[2],
                    'phone': record[3],
                    'created_at': record[4]
                } for record in records]
        except sqlite3.Error as e:
            self.logger.error(f"Error reading all records: {str(e)}")
            raise

    def update_record(self, record_id: int, data: Dict[str, Any]) -> bool:
        """Update a record in the database."""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE records SET name = ?, email = ?, phone = ? WHERE id = ?",
                    (data['name'], data['email'], data.get('phone', ''), record_id)
                )
                conn.commit()
                success = cursor.rowcount > 0
                if success:
                    self.logger.info(f"Updated record with ID: {record_id}")
                return success
        except sqlite3.Error as e:
            self.logger.error(f"Error updating record: {str(e)}")
            raise

    def delete_record(self, record_id: int) -> bool:
        """Delete a record from the database."""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
                conn.commit()
                success = cursor.rowcount > 0
                if success:
                    self.logger.info(f"Deleted record with ID: {record_id}")
                return success
        except sqlite3.Error as e:
            self.logger.error(f"Error deleting record: {str(e)}")
            raise
