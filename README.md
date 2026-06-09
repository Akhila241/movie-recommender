# 🎬 Movie Recommender

A content-based movie recommendation system that suggests 5 similar movies with live posters fetched from TMDB API.

## Live Demo
[Click here to view the live app](https://movie-recommender-2-yfko.onrender.com)

## Tech Stack
- **ML:** scikit-learn (TF-IDF Vectorization, Cosine Similarity)
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **API:** TMDB API (live movie posters)
- **Deployment:** Render

## Features
- Content based filtering recommendation engine
- Live movie posters fetched from TMDB API
- Autocomplete search across 4809 movies
- Popular movies homepage
- Poster caching for fast load times
- Case insensitive search

## How it works
1. Movie metadata — title, genre, cast, director, overview — is combined into tags
2. TF-IDF vectorizes the tags into numerical vectors
3. Cosine similarity finds the 5 most similar movies
4. TMDB API fetches live posters for each recommendation

## ML Concepts Used
- Content Based Filtering
- TF-IDF Vectorization
- Cosine Similarity

## Dataset
TMDB 5000 Movies Dataset — 4809 movies

## How to Run Locally
1. Clone the repo
git clone https://github.com/Akhila241/movie-recommender.git
2. Install dependencies
pip install -r requirements.txt
3. Add your TMDB API key in app.py
4. Build recommendation engine
python recommend.py
5. Run the app
python app.py

6. Open `http://127.0.0.1:5000`

## Project Structure

├── app.py              # Flask backend + TMDB API integration
├── recommend.py        # ML recommendation engine
├── model_info.json     # Cached model data
├── requirements.txt    # Dependencies
├── render.yaml         # Render deployment config
└── templates/
└── index.html      # Frontend

## Author
Akhila — [GitHub](https://github.com/Akhila241)