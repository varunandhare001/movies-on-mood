import pandas as pd

data = {
    "title": ["Inception", "The Dark Knight", "Toy Story", "Interstellar", "The Matrix"],
    "summary": [
        "A thief who enters dreams to steal secrets",
        "A vigilante fights crime in Gotham City",
        "A cowboy doll feels replaced by a new toy",
        "A team of explorers travels through a wormhole in space",
        "A computer hacker learns about the true nature of reality"
    ],
    "Action": [1, 1, 0, 0, 1],
    "Drama": [1, 1, 0, 1, 0],
    "Comedy": [0, 0, 1, 0, 0],
    "Thriller": [1, 1, 0, 0, 1],
    "Sci-Fi": [1, 0, 0, 1, 1]
}

df = pd.DataFrame(data)
df.to_csv("movie_data.csv", index=False)  # Save in the same directory as NLP.py

print("CSV file created successfully!")
