import sqlite3
from datetime import datetime

class PayHealthDatabase:
    def __init__(self, db_name='payhealth.db'):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def initialize_database(self):
        try:
            self.connect()
            cursor = self.conn.cursor()

            cursor.execute("DROP TABLE IF EXISTS user_info;")
            cursor.execute("DROP TABLE IF EXISTS error_info;")

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    email TEXT
                );
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS error_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    field_name TEXT,
                    error_type TEXT,
                    error_date DATETIME
                );
            ''')

            self.conn.commit()
            print("Database and tables created successfully.")
        except Exception as e:
            print(f"An error occurred during database initialization: {e}")

        finally:
            self.disconnect()

    def save_error_info(self, field_name, error_type):
        try:
            self.connect()
            current_timestamp = datetime.now()

            self.conn.execute('''
                INSERT INTO error_info (field_name, error_type, error_date)
                VALUES (?, ?, ?);
            ''', (field_name, error_type, current_timestamp))

            self.conn.commit()
            print("Error info saved successfully.")
        except Exception as e:
            print(f"An error occurred while saving error info: {e}")

        finally:
            self.disconnect()

    def get_error_records_by_field_name(self, field_name):
        try:
            self.connect()
            cursor = self.conn.cursor()

            cursor.execute('''
                SELECT * FROM error_info
                WHERE field_name = ?;
            ''', (field_name,))

            records = cursor.fetchall()
            return records

        except Exception as e:
            print(f"An error occurred while retrieving error records: {e}")
            return []

        finally:
            self.disconnect()        
