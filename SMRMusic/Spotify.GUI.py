import streamlit as st
from transformers import pipeline
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import webbrowser
import http.server
import socketserver
import urllib.parse
from camera_mood_detector import get_camera_mood
import moviepy.editor as mp

# --- Streamlit Config ---
st.set_page_config(page_title="🎶 MoodCast Spotify", layout="centered")

# --- Mood Terimleri ---
MOOD_TERMS = {
    "happy": ["happy pop", "joyful beats", "dance songs"],
    "sad": ["sad ballads", "cry songs", "melancholy music"],
    "angry": ["rage rock", "hard trap", "angry rap"],
    "calm": ["chill lofi", "relaxing music", "ambient jazz"],
    "neutral": ["top 50 hits", "indie mix", "random playlist"],
    "anxious": ["dark ambient", "eerie instrumental", "mystic soundtrack"]
}

# --- Session Başlat ---
if "spotify_token" not in st.session_state:
    st.session_state.spotify_token = None

# --- Spotify Secrets ---
CLIENT_ID = st.secrets["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = st.secrets["SPOTIFY_CLIENT_SECRET"]
REDIRECT_URI = st.secrets["SPOTIFY_REDIRECT_URI"]

scope = "playlist-modify-public"
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope=scope)

# --- Local Server for Spotify Auth ---
class AuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        if 'code' in params:
            self.server.auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write("<h1>Spotify authorization successful. You may close this window.</h1>".encode("utf-8"))
        else:
            self.send_error(400, "No code in callback URL")

def start_local_server():
    PORT = 8888
    with socketserver.TCPServer(("localhost", PORT), AuthHandler) as httpd:
        httpd.handle_request()
        return httpd.auth_code

# --- UI ---
st.title("🎧 MoodCast - Kamera ile Duygu Temelli Spotify Playlist")

# Spotify Bağlantı
if st.session_state.spotify_token:
    st.success("Spotify yetkilendirmesi tamamlandı.")
    if st.button("🔌 Bağlantıyı Kapat"):
        st.session_state.spotify_token = None
        st.rerun()
else:
    if st.button("🔐 Spotify'a Bağlan"):
        auth_url = sp_oauth.get_authorize_url()
        webbrowser.open(auth_url)
        auth_code = start_local_server()
        token_info = sp_oauth.get_access_token(auth_code)
        st.session_state.spotify_token = token_info["access_token"]
        st.rerun()

# Mood Girişi
mood_source = st.radio("Mood belirleme yöntemi:", ["Kamera ile tespit et", "Elle seç"])
moods = ["neutral"]

if mood_source == "Kamera ile tespit et":
    if st.button("📷 Kameradan Mood Tespit Et"):
        detected = get_camera_mood()
        moods = [detected]
        st.success(f"Algılanan mood: {detected}")
else:
    moods = st.multiselect("Mood seçin:", list(MOOD_TERMS.keys()), default=["neutral"])

# Playlist Adı ve Karışık Seçenek
playlist_name = st.text_input("🎵 Playlist adı:", value="MoodCast Playlist")
shuffle_tracks = st.checkbox("🎲 Karışık sırayla çal")

# Playlist Oluşturma
if st.session_state.spotify_token and st.button("🎧 Playlist Oluştur"):
    sp = spotipy.Spotify(auth=st.session_state.spotify_token)
    user_id = sp.current_user()["id"]

    search_terms = []
    for mood in moods:
        search_terms.extend(random.sample(MOOD_TERMS.get(mood, MOOD_TERMS["neutral"]), 3))
    random.shuffle(search_terms)

    track_uris = []
    for term in search_terms:
        results = sp.search(q=term, type="track", limit=2)
        items = results["tracks"]["items"]
        for item in items:
            if len(track_uris) < 10:
                track_uris.append(item["uri"])
        if len(track_uris) >= 10:
            break

    if shuffle_tracks:
        random.shuffle(track_uris)

    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
    sp.playlist_add_items(playlist_id=playlist["id"], items=track_uris)

    st.subheader("🎶 MoodCast Playlist")
    st.markdown(f"[🎧 Spotify'da Aç]({playlist['external_urls']['spotify']})")
    st.components.v1.iframe(f"https://open.spotify.com/embed/playlist/{playlist['id']}", height=400)
