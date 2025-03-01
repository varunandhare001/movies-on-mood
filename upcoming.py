import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io
import webbrowser

# TMDB API Key (Replace with your own key)
API_KEY = "d685fb446a77b9fd709d051285006d36"
TMDB_URL = "https://api.themoviedb.org/3/movie/upcoming?api_key={}&language=en-US&page=1".format(API_KEY)
BOOKING_URL = "https://in.bookmyshow.com/mumbai/movies/"


# Function to fetch movie data
def fetch_movies():
    try:
        response = requests.get(TMDB_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.exceptions.Timeout:
        return "Connection Timeout. Please try again later."
    except requests.exceptions.RequestException as e:
        if "429" in str(e):
            return "TMDB is blocking requests. Try again later."
        return "Network Error: " + str(e)


# Function to open booking link
def book_ticket(movie_name):
    webbrowser.open(BOOKING_URL + movie_name.replace(" ", "-").lower())

def home():
    window.destroy()
    import main

# GUI Setup
window = tk.Tk()
window.title("Upcoming Movies")
window.geometry("1660x800")

frame = tk.Frame(window)
frame.pack(fill=tk.BOTH, expand=True)

movies = fetch_movies()

if isinstance(movies, str):
    error_label = tk.Label(frame, text=movies, font=("Arial", 14), fg="red")
    error_label.pack(pady=20)
else:
    for movie in movies[:5]:  # Display top 5 upcoming movies
        movie_frame = tk.Frame(frame, pady=10)
        movie_frame.pack(fill=tk.X)

        # Fetch movie poster
        poster_url = "https://image.tmdb.org/t/p/w500" + str(movie.get("poster_path", ""))
        try:
            img_data = requests.get(poster_url).content
            img = Image.open(io.BytesIO(img_data))
            img = img.resize((100, 150))
            img = ImageTk.PhotoImage(img)
        except Exception:
            img = None

        # Poster label
        poster_label = tk.Label(movie_frame, image=img) if img else tk.Label(movie_frame, text="No Image")
        poster_label.image = img  # Keep reference to prevent garbage collection
        poster_label.pack(side=tk.LEFT, padx=10)

        # Movie details
        details = tk.Frame(movie_frame)
        details.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        title_label = tk.Label(details, text=movie["title"], font=("Arial", 14, "bold"))
        title_label.pack(anchor="w")

        release_label = tk.Label(details, text=f"Release Date: {movie['release_date']}", font=("Arial", 12))
        release_label.pack(anchor="w")

        overview_label = tk.Label(details, text=movie["overview"], font=("Arial", 10), wraplength=500, justify="left")
        overview_label.pack(anchor="w", pady=5)

        # Booking button
        book_button = tk.Button(details, text="Book Tickets", command=lambda m=movie['title']: book_ticket(m))
        book_button.pack(anchor="w", pady=5)

home_button = tk.Button(window,width=30, text="HOME", command=home, font=("Helvetica", 30))
home_button.place(x=440,y=300)

window.mainloop()