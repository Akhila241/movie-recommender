import pickle
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


with open('movies.pkl', 'rb') as f:
    movies = pickle.load(f)

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)


TMDB_API_KEY = "244bee97ec625907ce29dedee644534d"  

import json
import os

# Cache file to store poster URLs so we don't call API repeatedly
CACHE_FILE = 'poster_cache.json'

# Load existing cache
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, 'r') as f:
        poster_cache = json.load(f)
else:
    poster_cache = {}

def get_poster(movie_title):
    # Check cache first — if we already fetched this poster, return it instantly
    if movie_title in poster_cache:
        return poster_cache[movie_title]
    
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
        response = requests.get(url, timeout=5)  # timeout after 5 seconds
        data = response.json()

        if data['results']:
            poster_path = data['results'][0]['poster_path']
            if poster_path:
                full_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                # Save to cache so next time it's instant
                poster_cache[movie_title] = full_url
                with open(CACHE_FILE, 'w') as f:
                    json.dump(poster_cache, f)
                return full_url

        poster_cache[movie_title] = None
        return None
    except:
        return None
def recommend(movie_title):
    try:
        idx = movies[movies['title'].str.lower() == movie_title.lower()].index[0]
    except:
        return []

    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    top5 = scores[1:6]

    recommendations = []
    for i, score in top5:
        title = movies.iloc[i]['title']
        poster = get_poster(title)
        recommendations.append({
            'title': title,
            'score': round(score * 100, 1),
            'poster': poster
        })
    return recommendations


@app.route('/')
def home():
    movie_list = movies['title'].tolist()
    return render_template('index.html', movies=movie_list)

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    movie_title = data['movie']

    results = recommend(movie_title)

    if not results:
        return jsonify({'error': 'Movie not found'}), 404

    # Also fetch the searched movie's poster
    searched_poster = get_poster(movie_title)

    return jsonify({
        'recommendations': results,
        'searched_poster': searched_poster,
        'searched_title': movie_title
    })

@app.route('/popular', methods=['GET'])
def popular():
    popular_movies = [
        'Inception', 'Interstellar', 'The Dark Knight',
        'Avatar', 'Titanic', 'The Avengers'
    ]
    result = []
    for title in popular_movies:
        poster = get_poster(title)
        result.append({'title': title, 'poster': poster})
    return jsonify({'popular': result})

if __name__ == '__main__':
    app.run(debug=True)