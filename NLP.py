import requests
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import tkinter as tk
from tkinter import Label, Entry, Button
from PIL import Image, ImageTk
from io import BytesIO

# TMDB API Key
TMDB_API_KEY = "d685fb446a77b9fd709d051285006d36"

# Load movie dataset
data = pd.read_csv('movie_data.csv')

# Preprocess text data
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def home():
    window.destroy()
    import main

def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word.lower()) for word in tokens if word.isalpha()]
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)


data['clean_summary'] = data['summary'].apply(preprocess_text)

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(data['clean_summary'],
                                                    data.drop(['title', 'summary', 'clean_summary'], axis=1),
                                                    test_size=0.2, random_state=42)

# Build a pipeline for text classification
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('classifier', MultiOutputClassifier(MultinomialNB()))
])

# Train the model
pipeline.fit(X_train, y_train)


def search_movie_on_tmdb(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]['title'], data['results'][0]['poster_path']
    return None, None


def get_movie_recommendation():
    user_input = entry.get()
    processed_input = preprocess_text(user_input)
    predicted_genre = pipeline.predict([processed_input])
    predicted_movie, poster_path = search_movie_on_tmdb(user_input)

    if predicted_movie:
        result_label.config(text=f"Recommended Movie: {predicted_movie}")
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            response = requests.get(poster_url)
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img = img.resize((200, 300), Image.LANCZOS)
            poster_img = ImageTk.PhotoImage(img)
            poster_label.config(image=poster_img)
            poster_label.image = poster_img
    else:
        result_label.config(text="No movie found!")


# GUI Setup
window = tk.Tk()
window.title("Movie Details Fetcher")
window.geometry("1660x800")

Label(window, text="Enter Movie Description:").pack()
entry = Entry(window, width=50)
entry.pack()
Button(window, text="Find Movie", command=get_movie_recommendation).pack()

result_label = Label(window, text="")
result_label.pack()
poster_label = Label(window)
poster_label.pack()

home_button = tk.Button(window,width=30, text="HOME", command=home, font=("Helvetica", 30))
home_button.place(x=440,y=450)

window.mainloop()
