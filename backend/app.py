import os
from dotenv import load_dotenv
import spotipy

from flask import Flask, session, jsonify
from flask_cookie_decode import CookieDecode
from spotipy.oauth2 import SpotifyOAuth
from flask_cors import CORS, cross_origin

load_dotenv()
CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
username = os.getenv('SPOTIFY_USERNAME')
SCOPEs = 'user-read-private user-read-email user-top-read playlist-read-private playlist-modify-public playlist-modify-private'

# Create the Flask application
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config.update({'SECRET_KEY': 'MY_SECRET_KEY'})
cookie = CookieDecode()
cookie.init_app(app)

def get_auth_manager():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPEs,
        cache_handler=spotipy.cache_handler.FlaskSessionCacheHandler(session)
    )

def get_auth_url():
    return get_auth_manager().get_authorize_url()

@app.route('/get_logged')
@cross_origin()
def get_session():
    if (session and session.get('user')):
        return jsonify(dict(session))
    else:
        return jsonify({'logged_in': False, 'auth_url': get_auth_url()})

@app.route('/clear_session')
@cross_origin()
def clear_session():
    session.clear()
    return jsonify({'session': 'cleared'})

@app.route('/login')
@cross_origin()
def login():
    auth_manager = get_auth_manager()
    if session.get('user'):
        data = jsonify(dict(session).get('user')['user_info'])
        return data

    sp = spotipy.Spotify(auth_manager=auth_manager)
    user_info = sp.me()
    simple_user_info = {
        "logged_in": True,
        "user_info": {
            "display_name": user_info["display_name"],
            "id": user_info["id"],
            "uri": user_info["uri"],
            "profile_url": user_info["external_urls"]["spotify"]
        }
    }
    session['user'] = simple_user_info
    return jsonify(dict(session).get('user'))

if __name__ == '__main__':
    app.run()