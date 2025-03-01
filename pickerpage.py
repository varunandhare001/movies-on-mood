import tkinter as tk
from tkinter import StringVar, OptionMenu
import mysql.connector
import random
import requests
from PIL import Image, ImageTk
from io import BytesIO

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ektejivan001",
    database="movie_suggestion"
)

cursor = conn.cursor()

# Create a function to close the database connection
def close_connection():
    conn.close()

# Create a function to get movie suggestions based on user's responses
def get_movie_suggestions():
    # Get user responses
    mood = mood_var.get()
    genre = genre_var.get()
    director = director_var.get()
    release_year = release_year_var.get()

    # Filter the database based on user responses
    query = "SELECT title, poster_url FROM movies WHERE genre=%s AND director=%s AND release_year=%s"
    cursor.execute(query, (genre, director, release_year))
    result = cursor.fetchall()

    # Display a random movie suggestion
    if result:
        title, poster_url = random.choice(result)
        result_label.config(text="I suggest you watch: " + title)
        load_and_display_poster(poster_url)
    else:
        result_label.config(text="Sorry, I don't have any suggestions for your criteria.")
        # poster_label.config(image="")  # Clear the poster label

def home():
    window.destroy()
    import main
# poster_label = tk.Label()
# poster_label.place(x=1080,y=240)
# window = tk.Tk()
# window.title("Movie Suggestion")

# window.geometry("1660x800")

# Create the main window
window = tk.Tk()
window.title("Movie Picker")
window.geometry("1660x800")

background_image = Image.open("bg.jpg")
background_image = background_image.resize((1450, 770))
background_photo = ImageTk.PhotoImage(background_image)

# Create a Label with the background image
background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


poster_label = tk.Label()
poster_label.place(x=600, y=150)

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

# # Create the main window
# window = tk.Tk()
# window.title("Movie Picker")
# window.geometry("600x400")


# Instead of ttk.Combobox, use OptionMenu
title_lable = tk.Label(window,text= "THE MOVIE PICKER",width=26,height=1,bg="dark turquoise",fg="black", font=("Roman", 93))
title_lable.place(x=0,y=0)
# Mood question
mood_label = tk.Label(window, text="What is your mood today?",bg="gray27", fg="white", font=("Helvetica", 30))
mood_label.place(x=20,y=150)

moods = ["Happy", "Neutral", "Sad"]
mood_var = tk.StringVar(value=moods[0])

mood_menu = tk.OptionMenu(window, mood_var, *moods,)
mood_menu.place(x=430,y=160)

# Genre question
genre_label = tk.Label(window, text="Select a genre:",bg="gray27", fg="white", font=("Helvetica", 30))
genre_label.place(x=20,y=200)

genres = ["Action", "Drama", "Comedy", "Sci-Fi", "Romance", "Thriller"]
genre_var = tk.StringVar(value=genres[0])

genre_menu = tk.OptionMenu(window, genre_var, *genres)
genre_menu.place(x=430,y=210)

# Director question
director_label = tk.Label(window, text="Who is your favorite director?",bg="gray27", fg="white", font=("Helvetica", 30))
director_label.place(x=20,y=250)

directors = ["S. S Rajamauli", "Raj kumar hirani", "Director3", "Director4"]
director_var = tk.StringVar(value=directors[0])

director_menu = tk.OptionMenu(window, director_var, *directors)
director_menu.place(x=430,y=260)

# Release Year question
release_year_label = tk.Label(window, text="Select a release year:",bg="gray27", fg="white", font=("Helvetica", 30))
release_year_label.place(x=20,y=300)

release_years = ["2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015", "2009"]
release_year_var = tk.StringVar(value=release_years[0])

release_year_menu = tk.OptionMenu(window, release_year_var, *release_years)
release_year_menu.place(x=430,y=310)

# # Create and place the mood label and dropdown
# mood_label = tk.Label(window, text="What is your mood today?", font=("Helvetica", 12))
# mood_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# moods = ["Happy", "Neutral", "Sad"]
# mood_var = StringVar(window)
# mood_var.set(moods[0])  # Default mood
# mood_dropdown = OptionMenu(window, mood_var, *moods)
# mood_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# # Create and place the genre label and dropdown
# genre_label = tk.Label(window, text="Select a genre:", font=("Helvetica", 12))
# genre_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# genres = ["Action", "Comedy", "Drama", "Fantasy", "Horror", "Sci-Fi"]
# genre_var = StringVar(window)
# genre_var.set(genres[0])  # Default genre
# genre_dropdown = OptionMenu(window, genre_var, *genres)
# genre_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# # Create and place the director label and entry
# director_label = tk.Label(window, text="Enter director's name:", font=("Helvetica", 12))
# director_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

# director_var = StringVar(window)
# director_entry = tk.Entry(window, textvariable=director_var, font=("Helvetica", 12))
# director_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# # Create and place the release_year label and entry
# release_label = tk.Label(window, text="Enter Release year:", font=("Helvetica", 12))
# release_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

# release_year_var = StringVar(window)
# release_entry = tk.Entry(window, textvariable=release_year_var, font=("Helvetica", 12))
# release_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
# release_years = ["2022", "2021", "2020", "2019", "2018", "2017", "2016"]
# release_year_var = tk.StringVar(value=release_years[0])

# release_year_menu = tk.OptionMenu(window, textvariable=release_year_var, values=release_years)
# release_year_menu.place()

# Submit button
submit_button = tk.Button(window,width=30, text="Get Movie Suggestion", command=get_movie_suggestions, font=("Helvetica", 30))
submit_button.place(x=20,y=370)

home_button = tk.Button(window,width=30, text="HOME", command=home, font=("Helvetica", 30))
home_button.place(x=20,y=450)
# Result label
result_label = tk.Label(window, text="",bg="gray27", fg="white", font=("Helvetica", 30), wraplength=400)
result_label.place(x=20,y=500)

# Start the Tkinter main loop
window.mainloop()

# Close the database connection
conn.close()

# window.mainloop()
