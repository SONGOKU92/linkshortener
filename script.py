from flask import Flask, request, redirect, jsonify, render_template_string
import random
import string
import os
import re  

app = Flask(__name__)

url_mapping = {}

def generate_short_id(num_chars=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=num_chars))

def is_valid_url(url):
    
    regex = re.compile(
        r'^(?:http|ftp)s?://'  
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  
        r'localhost|'  
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  
        r'(?::\d+)?'  
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)  
    return re.match(regex, url) is not None

@app.route('/')
def home():
    return render_template_string('''
     <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Raccourcir un lien</title>
        
    </head>
    <body>
        <div class="container">
            <h1>Réducteur d'URL</h1>
            <form action="/shorten" method="POST">
                <label for="url">Entrez une URL à raccourcir :</label>
                <input type="text" id="url" name="url" required>
                <input type="submit" value="Raccourcir">
            </form>
        </div>
        
    </body>
    </html>
    ''')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['url']
    
    if not is_valid_url(long_url):
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Erreur d'URL</title>
            
        </head>
        <body>
            <div class="container">
                <h1>Erreur !</h1>
                <p>Veuillez entrer une URL valide.</p>
                <a href="/" class="back-btn">Retourner à la page principale</a>
            </div>
            
        </body>
        </html>
        ''')

    short_id = generate_short_id()
    
    while short_id in url_mapping:
        short_id = generate_short_id()
        
    url_mapping[short_id] = long_url
     short_url = f"https://{request.host}/{short_id}"
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>URL raccourcie</title>
        
    </head>
    <body>
        <div class="container">
            <h1>URL raccourcie !</h1>
            <p>Votre URL courte : <a href="{{ short_url }}">{{ short_url }}</a></p>
            <p>Vous pouvez partager ce lien avec d'autres personnes.</p>
            <a href="/" class="back-btn">Raccourcir une autre URL</a>
        </div>
    
    </body>
    </html>
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
