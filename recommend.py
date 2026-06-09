import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle


movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')
movies = movies.merge(credits, on='title')


movies = movies[['title', 'overview', 'genres', 'cast', 'crew']]


def extract_names(obj, top=None):
    try:
        items = ast.literal_eval(obj)
        names = [i['name'] for i in items]
        # top=3 means only take first 3 (for cast — top 3 actors only)
        return names[:top] if top else names
    except:
        return []


def get_director(obj):
    
    try:
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                return [i['name']]  
        return []
    except:
        return []


movies['genres'] = movies['genres'].apply(extract_names)


movies['cast'] = movies['cast'].apply(lambda x: extract_names(x, top=3))


movies['crew'] = movies['crew'].apply(get_director)


movies['overview'] = movies['overview'].fillna('')

def combine_tags(row):
    return ' '.join(
        row['overview'].split() +        # plot words
        row['genres'] +                   # genre names
        row['cast'] +                     # actor names
        row['crew']                       # director name
    )

movies['tags'] = movies.apply(combine_tags, axis=1)


movies = movies[['title', 'tags']]
print("Sample tags for Avatar:")
print(movies['tags'].iloc[0][:200])  

tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
vectors = tfidf.fit_transform(movies['tags'])


print("\nVector shape:", vectors.shape)

similarity = cosine_similarity(vectors)
print("\nSimilarity matrix shape:", similarity.shape)

def recommend(movie_title):
    
    try:
        idx = movies[movies['title'] == movie_title].index[0]
    except:
        return []

    
    scores = list(enumerate(similarity[idx]))

    
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    
    top5 = scores[1:6]

    recommendations = []
    for i, score in top5:
        recommendations.append({
            'title': movies.iloc[i]['title'],
            'score': round(score * 100, 1)
        })
    return recommendations


print("\nRecommendations for Avatar:")
for r in recommend('Avatar'):
    print(f"  {r['title']} — {r['score']}% match")

print("\nRecommendations for The Dark Knight:")
for r in recommend('The Dark Knight'):
    print(f"  {r['title']} — {r['score']}% match")


with open('movies.pkl', 'wb') as f:
    pickle.dump(movies, f)

with open('similarity.pkl', 'wb') as f:
    pickle.dump(similarity, f)

print("\nSaved movies.pkl and similarity.pkl!")