import tkinter as tk
from tkinter import ttk
from tmdbv3api import TMDb, Movie
import requests
from PIL import Image, ImageTk
from io import BytesIO

# Set your TMDb API key here
tmdb_api_key = 'd685fb446a77b9fd709d051285006d36'  # Replace with your API key

# Initialize TMDb API
tmdb = TMDb()
tmdb.api_key = tmdb_api_key
movie_api = Movie()

def home():
    window.destroy()
    import main


def get_movie_details(movie_title):
    try:
        search_results = movie_api.search(movie_title)
        if search_results:
            movie_id = search_results[0].id
            movie_details = movie_api.details(movie_id)

            # Fetch credits separately
            credits = movie_api.credits(movie_id)

            title = movie_details.title
            release_year = movie_details.release_date[:4] if movie_details.release_date else "Unknown"
            director = ", ".join([crew.name for crew in credits.crew if crew.job == 'Director']) or "Unknown"
            genres = [genre.name for genre in movie_details.genres] if movie_details.genres else []
            ratings = movie_details.vote_average if movie_details.vote_average else "N/A"
            poster_url = f"https://image.tmdb.org/t/p/w500{movie_details.poster_path}" if movie_details.poster_path else None

            return title, release_year, director, genres, ratings, poster_url
        else:
            return None, None, None, None, None, None
    except Exception as e:
        print(f"Error fetching movie details: {e}")
        return None, None, None, None, None, None


def show_movie_details():
    movie_title = entry_movie.get().strip()

    if not movie_title:
        result_label.config(text="Please enter a movie title.")
        poster_label.config(image="")
        return

    title, release_year, director, genres, ratings, poster_url = get_movie_details(movie_title)

    if title:
        result_label.config(
            text=f"Title: {title}\nRelease Year: {release_year}\nDirector: {director}\nGenres: {', '.join(genres)}\nRatings: {ratings}"
        )
        if poster_url:
            load_and_display_poster(poster_url)
        else:
            poster_label.config(image="")  # Clear the poster if none exists
    else:
        result_label.config(text="Movie details not found.")
        poster_label.config(image="")  # Clear the poster


def load_and_display_poster(poster_url):
    try:
        response = requests.get(poster_url)
        response.raise_for_status()  # Raise an error if the request fails
        image = Image.open(BytesIO(response.content))

        # Resize the image to fit the GUI
        image = image.resize((200, 300), Image.Resampling.LANCZOS)

        # Convert the image to Tkinter format
        photo = ImageTk.PhotoImage(image)

        # Display the image
        poster_label.config(image=photo)
        poster_label.image = photo  # Keep a reference to avoid garbage collection
    except Exception as e:
        print(f"Failed to load poster: {e}")


# Create the main window
window = tk.Tk()
window.title("Movie Details Fetcher")
window.geometry("1660x800")

# Movie title label and entry
# Movie title label
label_movie = tk.Label(window, text="Enter Movie Title:", font=("Helvetica", 14))
label_movie.grid(row=0, column=1, pady=10, padx=10, sticky="e")

# Movie title entry
entry_movie = tk.Entry(window, width=40, font=("Helvetica", 14))
entry_movie.grid(row=0, column=2, pady=10, padx=10, sticky="w")

# Search button
btn_search = tk.Button(window, text="Search", command=show_movie_details, font=("Helvetica", 14))
btn_search.grid(row=0, column=3, pady=10, padx=10, sticky="w")

# Result label
result_label = tk.Label(window, text="", wraplength=600, justify="left", anchor="w", font=("Helvetica", 12))
result_label.grid(row=1, column=1, columnspan=2, pady=10, padx=10)

# Poster label
poster_label = tk.Label(window)
poster_label.grid(row=1, column=3, pady=10, padx=10)

# Home button (Centered)
home_button = tk.Button(window, width=30, text="HOME", command=home, font=("Helvetica", 20))
home_button.grid(row=2, column=1, columnspan=2, pady=40)


# Run the Tkinter main loop
window.mainloop()