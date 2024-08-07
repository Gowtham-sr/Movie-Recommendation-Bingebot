import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

TMDB_API_KEY = '819b8debfc1fa09e2828b4ca6757c259'
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
POSTER_BASE_URL = 'https://image.tmdb.org/t/p/w500'

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def search_movie(movie_name):
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'query': movie_name
    }
    response = requests.get(url, params=params)
    return response.json().get('results', [])

def get_movie_trailer(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/videos"
    params = {
        'api_key': TMDB_API_KEY
    }
    response = requests.get(url, params=params)
    videos = response.json().get('results', [])
    
    for video in videos:
        if video['site'] == 'YouTube' and video['type'] == 'Trailer':
            return f"https://www.youtube.com/watch?v={video['key']}"
    
    return None

def get_movie_details(movie_id):
    runtime_url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    runtime_response = requests.get(runtime_url, params={'api_key': TMDB_API_KEY})
    runtime = runtime_response.json().get('runtime', 'Unknown')
    
    cast_url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits"
    cast_response = requests.get(cast_url, params={'api_key': TMDB_API_KEY})
    cast = cast_response.json().get('cast', [])
    lead_actor = cast[0]['name'] if cast else "Unknown"

    return runtime, lead_actor

def get_movie_reviews(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/reviews"
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en'
    }
    response = requests.get(url, params=params)
    return response.json().get('results', [])

def analyze_review_sentiments(reviews):
    sentiments = []
    for review in reviews:
        text = review.get('content', '')
        sentiment_score = analyzer.polarity_scores(text)
        sentiments.append({
            'author': review.get('author', 'Unknown'),
            'content': text,
            'sentiment': sentiment_score
        })
    return sentiments

def get_movie_recommendations(movie_name):
    movie = search_movie(movie_name)
    if not movie:
        return []
    movie_id = movie[0]['id']
    
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/recommendations"
    params = {
        'api_key': TMDB_API_KEY
    }
    response = requests.get(url, params=params)
    recommendations = response.json().get('results', [])
    
    recommendation_data = []
    for recommendation in recommendations:
        rec_id = recommendation['id']
        trailer_link = get_movie_trailer(rec_id)
        runtime, lead_actor = get_movie_details(rec_id)
        reviews = get_movie_reviews(rec_id)
        review_sentiments = analyze_review_sentiments(reviews)
        
        average_sentiment = (
            sum(sentiment['sentiment']['compound'] for sentiment in review_sentiments) / len(review_sentiments)
            if review_sentiments else 0
        )
        
        recommendation_data.append({
            'title': recommendation['title'],
            'overview': recommendation['overview'],
            'poster_path': f"{POSTER_BASE_URL}{recommendation['poster_path']}" if recommendation['poster_path'] else None,
            'trailer_link': trailer_link,
            'duration': f"{runtime} minutes" if runtime else "N/A",
            'lead_actor': lead_actor,
            'review_sentiments': review_sentiments,
            'average_sentiment': average_sentiment
        })
    
    return recommendation_data
