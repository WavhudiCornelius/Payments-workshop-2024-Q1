import sqlite3

def create_database_and_tables():
    # Connect to the SQLite database (this will create a new database if it doesn't exist)
    conn = sqlite3.connect('payhealth.db')
    cursor = conn.cursor()

    # Create user_info table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            email TEXT
        );
    ''')

    # Create error_info table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS error_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            field_name TEXT,
            error_type TEXT,
            FOREIGN KEY (user_id) REFERENCES user_info (id)
        );
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database_and_tables()
    print("Database 'payhealth.db' and tables 'user_info' and 'error_info' created successfully.")
