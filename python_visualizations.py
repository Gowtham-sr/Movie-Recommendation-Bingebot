import requests
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from spellchecker import SpellChecker

# Download NLTK stopwords if not already available
nltk.download('punkt')
nltk.download('stopwords')

# Constants
TMDB_API_KEY = '819b8debfc1fa09e2828b4ca6757c259'
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
POSTER_BASE_URL = 'https://image.tmdb.org/t/p/w500'

# Initialize VADER sentiment analyzer and SpellChecker
analyzer = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))
spell = SpellChecker()

def search_movie_by_name(movie_name):
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'query': movie_name,
        'page': 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    results = data.get('results', [])
    if results:
        return results[0]
    else:
        raise ValueError("Movie not found. Check the spelling or try a different name.")

def get_movie_reviews(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/reviews"
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en'
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    reviews = data.get('results', [])
    return reviews

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return ' '.join(filtered_tokens)

def compute_word_frequencies(reviews):
    review_texts = [preprocess_text(review['content']) for review in reviews if 'content' in review and review['content'].strip()]
    
    if not review_texts:
        raise ValueError("No valid review content found.")
    
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(review_texts)
    word_counts = np.sum(X.toarray(), axis=0)
    feature_names = vectorizer.get_feature_names_out()
    return dict(zip(feature_names, word_counts))

def plot_sentiment_pie_chart(reviews):
    if not reviews:
        print("No reviews available to plot sentiment.")
        return
    
    sentiments = [analyzer.polarity_scores(review['content'])['compound'] for review in reviews if 'content' in review]
    
    if not sentiments:
        print("No valid sentiment scores available to plot.")
        return
    
    # Categorize sentiments
    positive = sum(1 for score in sentiments if score > 0.05)
    neutral = sum(1 for score in sentiments if -0.05 <= score <= 0.05)
    negative = sum(1 for score in sentiments if score < -0.05)
    
    # Avoid division by zero and NaN values
    total = positive + neutral + negative
    if total == 0:
        print("No sentiments to plot.")
        return
    
    # Plot pie chart
    labels = 'Positive', 'Neutral', 'Negative'
    sizes = [positive, neutral, negative]
    colors = ['#4caf50', '#ffeb3b', '#f44336']
    explode = (0.1, 0, 0)  # explode 1st slice
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Sentiment Distribution of Reviews')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()


def get_movie_details(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en'
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    details = {
        'Title': data.get('title', 'N/A'),
        'Release Date': data.get('release_date', 'N/A'),
        'Genres': ', '.join(genre['name'] for genre in data.get('genres', [])),
        'Runtime': f"{data.get('runtime', 'N/A')} minutes",
        'Overview': data.get('overview', 'N/A'),
        'Director': 'N/A',
        'Cast': []
    }
    
    # Get the director and cast
    credits_url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits"
    credits_response = requests.get(credits_url, params=params)
    credits_data = credits_response.json()
    
    # Extract director
    for crew_member in credits_data.get('crew', []):
        if crew_member.get('job') == 'Director':
            details['Director'] = crew_member.get('name')
            break
    
    # Extract top 5 cast members
    cast_members = credits_data.get('cast', [])
    details['Cast'] = [member['name'] for member in cast_members[:5]]
    
    return details

def get_best_review(reviews):
    if not reviews:
        return "No reviews available."
    
    best_review = max(reviews, key=lambda r: analyzer.polarity_scores(r['content'])['compound'])
    return best_review['content']

def get_worst_review(reviews):
    if not reviews:
        return "No reviews available."
    
    worst_review = min(reviews, key=lambda r: analyzer.polarity_scores(r['content'])['compound'])
    return worst_review['content']

def correct_spelling(text):
    words = text.split()
    corrected_words = [spell.candidates(word).pop() if spell.candidates(word) else word for word in words]
    return ' '.join(corrected_words)

def display_summary(movie_name):
    movie_name_corrected = correct_spelling(movie_name)
    try:
        movie = search_movie_by_name(movie_name_corrected)
        movie_id = movie['id']
        movie_details = get_movie_details(movie_id)
        reviews = get_movie_reviews(movie_id)
        
        # Display movie summary
        print("\nMovie Summary:")
        print(f"Title: {movie_details['Title']}")
        print(f"Release Date: {movie_details['Release Date']}")
        print(f"Genres: {movie_details['Genres']}")
        print(f"Runtime: {movie_details['Runtime']}")
        print(f"Director: {movie_details['Director']}")
        print(f"Top Cast: {', '.join(movie_details['Cast'])}")
        print(f"Overview: {movie_details['Overview']}")
        
        # Display sentiment summary
        plot_sentiment_pie_chart(reviews)
        
        # List of available queries
        available_queries = {
            'best review': 'Get the best review based on sentiment',
            'worst review': 'Get the worst review based on sentiment',
            'director': 'Get the director of the movie',
            'runtime': 'Get the runtime of the movie',
            'length': 'Get the length of the movie',
            'actors': 'Get the top cast members',
            'cast': 'Get the top cast members',
            'genre': 'Get the genre(s) of the movie',
            'overview': 'Get the overview of the movie'
        }
        
        while True:
            query = input("\nAsk a question (type 'exit' to quit): ").strip().lower()
            query_corrected = correct_spelling(query)
            
            if query_corrected == 'exit':
                break
            
            if "best review" in query_corrected:
                print("\nBest Review:")
                print(get_best_review(reviews))
            elif "worst review" in query_corrected:
                print("\nWorst Review:")
                print(get_worst_review(reviews))
            elif "director" in query_corrected:
                print(f"Director: {movie_details['Director']}")
            elif "runtime" in query_corrected or "length" in query_corrected:
                print(f"Runtime: {movie_details['Runtime']}")
            elif "actors" in query_corrected or "cast" in query_corrected:
                print(f"Top Cast: {', '.join(movie_details['Cast'])}")
            elif "genre" in query_corrected:
                print(f"Genres: {movie_details['Genres']}")
            elif "overview" in query_corrected:
                print(f"Overview: {movie_details['Overview']}")
            else:
                print("Sorry, I didn't understand that query. Here are the things you can ask:")
                for key, value in available_queries.items():
                    print(f" - {key}: {value}")
    
    except ValueError as ve:
        print(f"Error: {ve}")

if __name__ == '__main__':
    movie_name = input("Enter the movie name: ")
    display_summary(movie_name)