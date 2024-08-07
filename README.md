**Movie Recommendation Binge Bot**

**Project Description**
The Movie Recommendation Binge Bot is a web application that delivers personalized movie recommendations based on user input. 
Using Flask, the TMDB API, and VADER sentiment analysis, it offers a detailed and interactive experience with movie information, including trailers, runtime, lead actors, and review sentiment analysis.

**Features**
Personalized Movie Recommendations: Get movie suggestions based on a specific movie name.
Detailed Movie Information: Includes movie trailers, runtime, lead actors, and more.
Sentiment Analysis: Analyze movie reviews using VADER sentiment analysis to gauge the overall sentiment.
Natural Language Processing (NLP): Implements tokenization, stop words removal, text preprocessing, spelling correction, and more.
Visualization: Visualize sentiment distribution in reviews and frequently occurring words using word clouds.

**Project Structure**
app.py: The main Flask application file that defines the web routes and handles user requests.
nlp.py: Contains functions for text preprocessing, including tokenization, stop words removal, and more.
tmdb.py: Handles interaction with the TMDB API, fetching movie details, trailers, and reviews. It also performs sentiment analysis on the reviews.
python_visualizations.py: Contains functions for visualizing data, such as plotting sentiment distribution and generating word clouds from reviews.

**Technologies Used**
Flask: A lightweight WSGI web application framework in Python.
TMDB API: The Movie Database API to fetch movie information.
VADER Sentiment Analysis: A lexicon and rule-based sentiment analysis tool.
Natural Language Toolkit (NLTK): For various NLP tasks.
scikit-learn: For text feature extraction and more.
matplotlib: For creating visualizations.

**Usage**
Navigate to the home page and enter the name of a movie you like.
Click on the "Recommend" button to get personalized movie recommendations.
Explore detailed information about each recommended movie, including trailers, runtime, lead actors, and sentiment analysis of reviews.

**Future Enhancements**
Enhanced Sentiment Analysis: Incorporate more advanced sentiment analysis models like BERT or RoBERTa for deeper understanding.
Multi-language Support: Integrate language detection and translation tools to handle reviews in multiple languages.
Aspect-Based Sentiment Analysis: Analyze sentiments specific to different aspects (e.g., acting, plot, direction) rather than overall sentiment.

**Contributing**
We welcome contributions to enhance the functionality and features of the Movie Recommendation Binge Bot. Please feel free to submit pull requests or open issues for any bugs or feature requests.
