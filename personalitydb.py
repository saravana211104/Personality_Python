import mysql.connector
from mysql.connector import Error

def create_database():
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password=""
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            # Create a new database
            cursor.execute("CREATE DATABASE IF NOT EXISTS file_storage_db")
            print("Database 'file_storage_db' created or already exists.")
            
            # Connect to the new database
            connection.database = 'file_storage_db'
            
            # Create a new table with an additional name column
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    image LONGBLOB,
                    text LONGTEXT
                )
            """)
            print("Table 'files' with 'name' column created or already exists.")
    
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Run the function to create the database and table
create_database()
