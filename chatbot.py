from flask import Flask, request, jsonify, render_template
import webbrowser

app = Flask(__name__)

# Predefined movie recommendations
movie_recommendations = {
    "harry potter": "I recommend 'Harry Potter and the Prisoner of Azkaban'! It's a fan favorite.",
    "marvel": "You should watch 'Avengers: Endgame'. A great conclusion to the saga!",
    "batman": "Try 'The Dark Knight' – one of the best superhero movies ever!",
    "romance": "If you love romance, 'The Notebook' is a must-watch!",
    "comedy": "You'd love 'Superbad' or 'The Hangover' for a good laugh!"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "").lower()
    response = movie_recommendations.get(user_input, "I can recommend movies! Ask me about any genre or movie.")
    return jsonify({"response": response})

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000/')  # Auto-open webpage
    app.run(debug=True)
