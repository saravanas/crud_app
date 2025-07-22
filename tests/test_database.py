import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """Set up test database."""
        self.db = Database('test.db')
        
    def tearDown(self):
        """Clean up test database."""
        if os.path.exists('test.db'):
            os.remove('test.db')
            
    def test_create_record(self):
        """Test creating a record."""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '1234567890'
        }
        record_id = self.db.create_record(data)
        self.assertIsInstance(record_id, int)
        
        # Verify the record was created
        record = self.db.read_record(record_id)
        self.assertEqual(record['name'], data['name'])
        self.assertEqual(record['email'], data['email'])
        self.assertEqual(record['phone'], data['phone'])
        
    def test_update_record(self):
        """Test updating a record."""
        # First create a record
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '1234567890'
        }
        record_id = self.db.create_record(data)
        
        # Update the record
        updated_data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'phone': '0987654321'
        }
        success = self.db.update_record(record_id, updated_data)
        self.assertTrue(success)
        
        # Verify the update
        record = self.db.read_record(record_id)
        self.assertEqual(record['name'], updated_data['name'])
        self.assertEqual(record['email'], updated_data['email'])
        self.assertEqual(record['phone'], updated_data['phone'])
        
    def test_delete_record(self):
        """Test deleting a record."""
        # First create a record
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '1234567890'
        }
        record_id = self.db.create_record(data)
        
        # Delete the record
        success = self.db.delete_record(record_id)
        self.assertTrue(success)
        
        # Verify the record was deleted
        record = self.db.read_record(record_id)
        self.assertIsNone(record)

if __name__ == '__main__':
    unittest.main()
