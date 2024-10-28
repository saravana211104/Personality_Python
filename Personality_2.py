import speech_recognition as sr
from PIL import Image, ImageTk
import pyttsx3
import mysql.connector
from mysql.connector import Error
import io
import tkinter as tk
from tkinter import Label, Text, Scrollbar
import threading

# Initialize recognizer and text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init()

# Set speech rate (lower value means slower speech)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 50)  # Decrease the rate by 50 (you can adjust this value as needed)

print("Personalities:\nMSDhoni\nVirat Kohli\nMKStalin\nHitler\nMamta")

# Capture audio from the microphone
with sr.Microphone() as source:
    print("Say something")
    audio = r.listen(source)

# Function to retrieve image and text from the database
def retrieve_from_db(name):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="",
            database="file_storage_db"
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT image, text FROM files WHERE name = %s", (name,))
            result = cursor.fetchone()
            if result:
                image_data, text_data = result
                return image_data, text_data
            else:
                print(f"No data found for {name}")
                return None, None
    
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None, None
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to display image and text in Tkinter window
def display_in_window(image_data, text_data, name):
    root = tk.Tk()
    root.title(f"Information for {name}")

    # Convert image data to PIL image
    image = Image.open(io.BytesIO(image_data))
    image = image.resize((250, 250), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)

    # Create image label
    image_label = Label(root, image=photo)
    image_label.image = photo
    image_label.pack()

    # Create text widget with scrollbar
    text_widget = Text(root, wrap='word', height=15, width=50)
    text_widget.insert(tk.END, text_data)
    text_widget.config(state=tk.DISABLED)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = Scrollbar(root, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)

    root.mainloop()

# Function to perform text-to-speech
def text_to_speech(text_data):
    try:
        engine.say(text_data)
        engine.runAndWait()
    except Exception as e:
        print(f"An error occurred while converting text to speech: {e}")

# Try to recognize the speech using Google Web Speech API
try:
    text = r.recognize_google(audio)
    print("You said: " + text)
    text = text.lower()
    
    # Retrieve image and text from the database
    image_data, text_data = retrieve_from_db(text)
    
    if image_data and text_data:
        # Create a thread for the TTS function
        tts_thread = threading.Thread(target=text_to_speech, args=(text_data,))
        tts_thread.start()
        
        # Display the image and text in Tkinter window
        display_in_window(image_data, text_data, text)
        
        # Wait for the TTS thread to finish
        tts_thread.join()
    else:
        print(f"No data found for: {text}")

except sr.UnknownValueError:
    print("Google speech recognition couldn't understand the audio")
except sr.RequestError as e:
    print(f"Couldn't request results from Google Speech Recognition service; {e}")
