import tkinter as tk
from tkinter import simpledialog, filedialog
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

def select_files():
    global image_path, text_path, file_name
    # Open file dialog to select an image file
    image_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.jpg *.png *.jpeg *.gif")])
    # Open file dialog to select a text file
    text_path = filedialog.askopenfilename(title="Select Text File", filetypes=[("Text files", "*.txt")])
    # Prompt user to enter the file name
    file_name = simpledialog.askstring("Input", "Enter the name of the file:")
    # Display selected file paths and file name
    if image_path:
        print(f"Selected image file: {image_path}")
    if text_path:
        print(f"Selected text file: {text_path}")
    if file_name:
        print(f"File name: {file_name}")

def store_files_in_db():
    if not image_path or not text_path or not file_name:
        print("Please select both an image and a text file and enter the file name.")
        return
    
    try:
        # Read image file as binary
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
        
        # Read text file
        with open(text_path, 'r') as txt_file:
            text_data = txt_file.read()
        
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="",
            database='file_storage_db'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            # Insert files into the table with the file name
            cursor.execute("INSERT INTO files (name, image, text) VALUES (%s, %s, %s)", (file_name, img_data, text_data))
            connection.commit()
            print("Files have been stored in the database.")
    
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def exit_app():
    root.destroy()

# Run the function to create the database and table
create_database()

# Create main window
root = tk.Tk()
root.title("File Selector")

# Add buttons to select files and store them in the database
btn_select_files = tk.Button(root, text="Select Files", command=select_files)
btn_select_files.pack(pady=20)

btn_store_files = tk.Button(root, text="Store Files in Database", command=store_files_in_db)
btn_store_files.pack(pady=20)

# Add exit button to close the application
btn_exit = tk.Button(root, text="Exit", command=exit_app)
btn_exit.pack(pady=20)

# Global variables to hold file paths and name
image_path = None
text_path = None
file_name = None

# Run the Tkinter event loop
root.mainloop()
