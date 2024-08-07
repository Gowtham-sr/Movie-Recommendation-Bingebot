from flask import Flask, render_template, request, jsonify
from tmdb import get_movie_recommendations

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        movie_name = data.get('movie_name')
        if not movie_name:
            return jsonify([]), 400
        recommendations = get_movie_recommendations(movie_name)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
