import pandas as pd
import ast

# Load datasets
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

# Merge on title
movies = movies.merge(credits, on='title')

print("Shape:", movies.shape)
print("\nColumns:", movies.columns.tolist())
print("\nFirst movie title:", movies['title'].iloc[0])
print("\nGenres of first movie (raw):", movies['genres'].iloc[0])
print("\nTotal movies:", len(movies))
print("\nSample overview:")
print(movies['overview'].iloc[0])