import random
import tkinter as tk
import mysql.connector
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser
import os
import sys
import subprocess
import cv2
import webview

# OpenCV Video Capture
video_path = "/Users/varunandhare/PycharmProjects/PythonProject/PythonProject/rk.mp4"  # Change to your video file path
cap = cv2.VideoCapture(video_path)



# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ektejivan001",
    database="movie_suggestion"
)

cursor = conn.cursor()

# Declare and initialize the mood variable
mood = ""


# Function to open a web link
def open_web_link(link):
    import webbrowser
    webbrowser.open(link)


# Define movie_url as a global variable
movie_url = ""

# Define movie_link as a global variable
movie_link = ""


def picker_page():
    window.destroy()
    import pickerpage

def info_page():
    window.destroy()
    import infopage

def upcoming_page():
    window.destroy()
    import upcoming

def nlp_page():
    window.destroy()
    import NLP

def review_page():
    window.destroy()
    import Moviereview

def chat_page():
    window.destroy()  # Close the current Tkinter window
    script_path = os.path.join('/Users/varunandhare/PycharmProjects/PythonProject/PythonProject/chatbot.py')  # Get the absolute path of chatbot.py
    subprocess.Popen([sys.executable, script_path])  # Run chatbot.py

# Function to suggest movies based on user's mood
def suggest_movie():
    # Use the global keyword to reference the outer 'movie_url' variable
    global movie_url

    # Use the global keyword to reference the outer 'mood' variable
    global mood
    mood = mood_entry.get()

    # Fetch movie details using the new function
    title, release_year, director, genres, ratings, poster_url = (mood)
    # title, poster_url = (mood)

    # Check if movie details were retrieved successfully
    if title is not None:
        result_label.config(text="I suggest you watch: " + title)
        load_and_display_poster(poster_url)
    else:
        result_label.config(text="Sorry, No any suggestions for that mood.")
        poster_label.config(image="")  # Clear the poster label

    # Store the movie link in a global variable
    global movie_link
    movie_link = movie_url

    # Then, later in the suggest_movie function or elsewhere in your code, you can assign it to movie_link
    movie_link = movie_url

    # Retrieve a random movie suggestion from the database
    cursor.execute("SELECT title, release_year, director, genre, poster_url, movie_url FROM movies WHERE genre=%s",
                   (mood,))
    result = cursor.fetchall()

    if result:
        title, release_year, director, genre, poster_url, movie_url = random.choice(result)
        movie_link = movie_url
        result_label.config(text="I suggest you watch: " + title)
        load_and_display_poster(poster_url)
    else:
        result_label.config(text="Sorry, No any suggestions for that mood.")
        poster_label.config(image="")  # Clear the poster label


# Function to load and display the movie poster
def load_and_display_poster(poster_url):
    try:
        # Send a GET request to fetch the image data
        response = requests.get(poster_url)
        # Create a PIL Image object from the image data
        image = Image.open(BytesIO(response.content))

        # Resize the image if needed
        # Adjust the width and height according to your preference
        width, height = 200, 300
        image = image.resize((width, height))

        # Convert the image to Tkinter PhotoImage format
        photo = ImageTk.PhotoImage(image)

        # Update the poster label with the new image
        poster_label.config(image=photo)
        poster_label.image = photo  # Store a reference to avoid garbage collection
    except Exception as e:
        print(f"Failed to load and display poster: {e}")


# Create the main window
window = tk.Tk()
window.title("Movie Suggestion")
window.geometry("1660x800")

# Load and resize the background image
background_image = Image.open("main.jpg")
background_image = background_image.resize((1450, 770))
background_photo = ImageTk.PhotoImage(background_image)

# Create a Label with the background image
background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Load Chhava poster from URL
poster_url = "https://i.pinimg.com/736x/45/37/9e/45379e75658d39bd42a97c1a873c4cc7.jpg"  # Replace with actual URL
response = requests.get(poster_url)
poster_image = Image.open(BytesIO(response.content))
poster_image = poster_image.resize((400, 500))  # Resize poster

poster_photo = ImageTk.PhotoImage(poster_image)

# Display the poster in the center
poster_label = tk.Label(window, image=poster_photo, bg="black")  # Black border effect
poster_label.place(relx=0.79, rely=0.6, anchor="center")  # Moves poster left

title_label = tk.Label(window, width=26, height=1, text="_______________________________", bg="dark turquoise",
                       fg="black", font=("Roman", 93))
title_label.place(x=0, y=0)

title1_label = tk.Label(window, width=26, text="MOVIES ON MOOD", bg="dark turquoise", fg="black", font=("Roman", 70))
title1_label.place(x=575, y=0)

mood_label = tk.Label(window, text="Enter your mood:", bg="slategray1", fg="black", font=("Helvetica", 25))
mood_label.place(x=15, y=135)

mood_entry = tk.Entry(window, bg="slategray1", fg="black", font=("Helvetica", 20))
mood_entry.place(x=15, y=195)

# Create and place the suggest button
# suggest_button = tk.Button(window,width=20, text="Suggest Movie", command=suggest_movie,bg="slategray1", font=("Helvetica", 19))
# suggest_button.place(x=15,y=260)


suggest_button = tk.Button(window, width=20, text="Suggest Movie", bg="slategray1", fg="black", font=("Helvetica", 19),
                           command=suggest_movie)
suggest_button.place(x=15, y=260)

# Create and place the result label
result_label = tk.Label(window, text="", bg="slategray1", fg="black", font=("Helvetica", 25))
result_label.place(x=15, y=317)

inst_label = tk.Label(window, text="Click on the poster to play the movie", bg="slategray1", fg="black",
                      font=("Helvetica", 25))
inst_label.place(x=15, y=370)

here_label = tk.Label(window, text="MOVIE\nPOSTER\nHERE", bg="slategray1", fg="black", font=("Helvetica", 25))
here_label.place(x=600, y=220)

genre_label = tk.Label(window, text="Available Moods list: ", bg="slategray1", fg="black", font=("Helvetica", 18))
genre_label.place(x=290, y=135)

genres = ["Action", "Comedy", "romantic", "horror", "drama"]
genre_var = tk.StringVar(value=genres[0])

genre_menu = tk.OptionMenu(window, genre_var, *genres, )
genre_menu.place(x=325, y=175)

poster_label = tk.Label(window)
poster_label.place(x=550, y=130)

# Add a click event handler to open the movie link when the poster is clicked
def on_poster_click(event):
    global movie_link

    # Fetch the movie link from the database
    cursor.execute("SELECT movie_url FROM movies WHERE genre=%s", (mood,))
    result = cursor.fetchone()

    if result:
        movie_link = result[0]  # Assuming the movie_url is in the first column
        open_web_link(movie_link)
    else:
        print("Movie link not found in the database.")


poster_label.bind("<Button-1>", on_poster_click)

poster_label.bind("<Button-1>", on_poster_click)

pickerButton = tk.Button(window, text='Movie Picker', font=('Helvetica', 17), bg='firebrick1', cursor='hand2',
                         command=picker_page)
pickerButton.place(x=15, y=40)

tmdbButton = tk.Button(window, text='Get movie info', font=('Helvetica', 17), bg='firebrick1', cursor='hand2',
                       command=info_page)
tmdbButton.place(x=170, y=40)

upcomingButton = tk.Button(window, width=30, text='Upcoming Movies', font=('Helvetica', 25), bg='firebrick1',
                           cursor='hand2', command=upcoming_page)
upcomingButton.place(x=205, y=585)

nlpButton = tk.Button(window, width=30, text='GET a Movie by description', font=('Helvetica', 17), bg='firebrick1',
                           cursor='hand2', command=nlp_page)
nlpButton.place(x=340, y=40)

chatButton = tk.Button(window, text='Chatbot', font=('Helvetica', 17), bg='firebrick1',
                           cursor='hand2', command=chat_page)
chatButton.place(x=700, y=40)

reviewButton = tk.Button(window, width=30, text='Top Movie reviewers', font=('Helvetica', 25), bg='firebrick1',
                           cursor='hand2', command=review_page)
reviewButton.place(x=905, y=130)
# create a upcoming movies section where posters will show up
# and fully control of admin to this section
# three movies will show up on the section when the main file will run

# Run the GUI main loop
window.mainloop()

# Close the database connection
conn.close()