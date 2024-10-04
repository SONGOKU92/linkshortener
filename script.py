# Copyright (c) 2024 SONGOKU92
# See the file 'LICENSE' for copying permission.
# Licensed under the MIT License.

from flask import Flask, request, redirect, jsonify, render_template_string
import random
import string
import os  

app = Flask(__name__)

url_mapping = {}

def generate_short_id(num_chars=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=num_chars))

@app.route('/')
def home():
    return render_template_string('''
    <h1>Réducteur de lien</h1>
    <form action="/shorten" method="POST">
        <label for="url">Entrez une URL à raccourcir :</label><br>
        <input type="text" id="url" name="url" required><br>
        <input type="submit" value="Raccourcir">
    </form>
    ''')

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['url']
    short_id = generate_short_id()
    
    while short_id in url_mapping:
        short_id = generate_short_id()

    url_mapping[short_id] = long_url
    short_url = request.host_url + short_id
    return render_template_string('''
    <h1>URL raccourcie !</h1>
    <p>Votre URL courte : <a href="{{ short_url }}">{{ short_url }}</a></p>
    <p>Vous pouvez partager ce lien avec d'autres personnes.</p>
    <a href="/">Raccourcir une autre URL</a>
    ''', short_url=short_url)

@app.route('/<short_id>', methods=['GET'])
def redirect_to_long_url(short_id):
    long_url = url_mapping.get(short_id)
    if long_url:
        return redirect(long_url)
    else:
        return jsonify({'error': 'URL non trouvée'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=False)
