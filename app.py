from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# API endpoint for getting random quotes (as an example of API usage)
QUOTE_API_URL = "https://api.quotable.io/random"

def get_random_quote():
    try:
        response = requests.get(QUOTE_API_URL)
        if response.status_code == 200:
            data = response.json()
            return data['content'], data['author']
    except:
        pass
    return "La connaissance est le pouvoir.", "Francis Bacon"

@app.route('/')
def home():
    quote, author = get_random_quote()
    return render_template('index.html', quote=quote, author=author)

@app.route('/ciel')
def ciel():
    quote, author = get_random_quote()
    return render_template('ciel.html', quote=quote, author=author)

@app.route('/snir')
def snir():
    quote, author = get_random_quote()
    return render_template('snir.html', quote=quote, author=author)

@app.route('/etudes-sup')
def etudes_sup():
    quote, author = get_random_quote()
    return render_template('etudes-sup.html', quote=quote, author=author)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
