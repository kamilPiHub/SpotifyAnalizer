from dotenv import load_dotenv # type: ignore
load_dotenv() # To załaduje zmienne z pliku .env

import os
import requests
import urllib.parse
from flask import Flask, request, redirect, session, jsonify
from flask_cors import CORS # type: ignore
from datetime import datetime

# --- Konfiguracja ---
app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"]) # Zezwól na zapytania z Reacta

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
# WAŻNE: Redirect URI musi być taki sam jak w panelu Spotify
REDIRECT_URI = "http://127.0.0.1:5000/callback"
# URL frontendu, na który przekierujemy po zalogowaniu
FRONTEND_URL = "http://localhost:3000" 

# Spotify API URLs
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"
SCOPE = "user-read-private user-read-email user-top-read user-read-recently-played"

# --- Trasy Autoryzacji ---

@app.route("/login")
def login():
    """Przekierowuje użytkownika do strony autoryzacji Spotify."""
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "show_dialog": True,
    }
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)

@app.route("/api/check-auth")
def check_auth():
    """Sprawdza, czy użytkownik jest zalogowany (ma ważny token w sesji)."""
    headers = get_spotify_headers() # Używamy istniejącej funkcji pomocniczej
    if not headers:
        # Jeśli nie ma nagłówków (użytkownik niezalogowany), zwróć błąd
        return jsonify({"error": "Not authenticated"}), 401 
    
    # Jeśli są nagłówki, oznacza to, że sesja jest aktywna
    return jsonify({"message": "User is authenticated"}), 200

@app.route("/callback")
def callback():
    """Obsługuje callback od Spotify, wymienia kod na token i przekierowuje do frontendu."""
    if 'error' in request.args:
        return redirect(f"{FRONTEND_URL}/?error={request.args['error']}")

    if 'code' in request.args:
        req_body = {
            "code": request.args["code"],
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        session["access_token"] = token_info["access_token"]
        session["refresh_token"] = token_info["refresh_token"]
        session["expires_at"] = datetime.now().timestamp() + token_info["expires_in"]

        # KLUCZOWA ZMIANA: Przekieruj do dashboardu w aplikacji React
        return redirect(f"{FRONTEND_URL}/dashboard")

@app.route("/logout")
def logout():
    """Wylogowuje użytkownika, czyszcząc sesję."""
    session.clear()
    return jsonify({"message": "Logged out successfully"})

# --- API Endpoints dla Frontendu ---

def get_spotify_headers():
    """Funkcja pomocnicza do tworzenia nagłówków z tokenem."""
    if "access_token" not in session or session.get("expires_at", 0) < datetime.now().timestamp():
        # W praktyce tu powinna być logika odświeżania tokena, ale na razie upraszczamy
        return None 
    
    access_token = session.get("access_token")
    return {"Authorization": f"Bearer {access_token}"}

@app.route("/api/profile")
def get_profile():
    """API endpoint do pobierania profilu użytkownika."""
    headers = get_spotify_headers()
    if not headers:
        return jsonify({"error": "Not authenticated"}), 401
    
    response = requests.get(API_BASE_URL + "me", headers=headers)
    return jsonify(response.json())

@app.route("/api/top-tracks")
def get_top_tracks():
    """API endpoint do pobierania topowych utworów."""
    headers = get_spotify_headers()
    if not headers:
        return jsonify({"error": "Not authenticated"}), 401
    
    params = {
        "time_range": request.args.get("time_range", "medium_term"),
        "limit": request.args.get("limit", 20)
    }
    response = requests.get(API_BASE_URL + "me/top/tracks", headers=headers, params=params)
    return jsonify(response.json())

@app.route("/api/top-artists")
def get_top_artists():
    """API endpoint do pobierania topowych artystów."""
    headers = get_spotify_headers()
    if not headers:
        return jsonify({"error": "Not authenticated"}), 401
    
    params = {
        "time_range": request.args.get("time_range", "medium_term"),
        "limit": request.args.get("limit", 20)
    }
    response = requests.get(API_BASE_URL + "me/top/artists", headers=headers, params=params)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(port=5000, debug=True)