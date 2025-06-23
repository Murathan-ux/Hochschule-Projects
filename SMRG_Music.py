import customtkinter as ctk
import threading
import time
import difflib
from textblob import TextBlob
import yt_dlp
import vlc
import cv2
from fer import FER
import speech_recognition as sr

mood_keywords = {
    "happy": ["joy", "glad", "cheerful", "excited", "delighted", "grateful", "content", "ecstatic", "elated", "happy"],
    "sad": ["down", "depressed", "unhappy", "blue", "melancholy", "heartbroken", "gloomy", "miserable", "crying", "sad"],
    "angry": ["mad", "furious", "irritated", "annoyed", "frustrated", "enraged", "agitated", "angry"],
    "calm": ["relaxed", "peaceful", "chill", "easygoing", "serene", "laid-back", "calm"],
    "anxious": ["nervous", "worried", "uneasy", "panicked", "scared", "stressed", "anxious"],
    "tired": ["exhausted", "fatigued", "sleepy", "drained", "burned out", "tired"],
    "neutral": ["fine", "okay", "meh", "average", "normal", "neutral", "just there"]
}

all_keywords = {word: mood for mood, words in mood_keywords.items() for word in words}
keyword_list = list(all_keywords.keys())

playlist_links = {
    "happy": "https://www.youtube.com/playlist?list=PLW9z2i0xwq0F3-8LieqflLLWLWZQgvhEX",
    "sad": "https://www.youtube.com/playlist?list=PL3-sRm8xAzY-w9GS19pLXMyFRTuJcuUjy",
    "tired": "https://www.youtube.com/playlist?list=PL7v1FHGMOadDghZ1m-jEIUnVUsGMT9jbH",
    "neutral": "https://www.youtube.com/playlist?list=PLwswtbNuwYECk10d_0mpJ2P0NKmrcFZE6",
    "angry": "https://www.youtube.com/playlist?list=PLQuudIe95KFPrcus-r9WaUp4-7Ep0YYo7",
    "calm": "https://www.youtube.com/playlist?list=PLC1sg9JBPAb1qtb_JDXX73nWJN8_-c8vb",
    "anxious": "https://www.youtube.com/playlist?list=PLo3pNg0eiPc9hsnjWTTM4PVTKrmGaXOQ1"
}

class FacialMoodDetector(threading.Thread):
    def __init__(self, callback):
        super().__init__(daemon=True)
        self.callback = callback

    def run(self):
        emotion_map = {
            "happy": "happy",
            "sad": "sad",
            "angry": "angry",
            "fear": "anxious",
            "surprise": "calm",
            "neutral": "neutral",
        }
        detector = FER(mtcnn=True)
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            emotions = detector.detect_emotions(frame)
            if emotions:
                top_emotion = detector.top_emotion(frame)
                if top_emotion:
                    emotion, score = top_emotion
                    mood = emotion_map.get(emotion)
                    if mood in playlist_links:
                        cap.release()
                        cv2.destroyAllWindows()
                        self.callback(mood)
                        return
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

def correct_and_classify(text):
    blob = TextBlob(text)
    corrected_text = str(blob.correct())
    words = corrected_text.lower().split()
    for word in words:
        if word in all_keywords:
            return all_keywords[word]
        closest = difflib.get_close_matches(word, keyword_list, n=1, cutoff=0.75)
        if closest:
            return all_keywords[closest[0]]
    return None

def classify_by_sentiment(text):
    blob = TextBlob(text)
    score = blob.sentiment.polarity
    if score > 0.2:
        return "happy"
    elif score < -0.2:
        return "sad"
    else:
        return "neutral"

class YouTubeMoodPlayer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MoodyTunes")
        self.geometry("880x720")
        self.configure(fg_color="#000000")

        title = ctk.CTkLabel(self, text="MoodyTunes", font=ctk.CTkFont(size=32, weight="bold"), text_color="#D8DEE9", fg_color="#000000")
        title.pack(pady=(30, 0))

        subtitle = ctk.CTkLabel(self, text="The world where your emotions make the music", font=ctk.CTkFont(size=16, weight="normal"), text_color="#D8DEE9", fg_color="#000000")
        subtitle.pack(pady=(0, 20))

        self.mood_var = ctk.StringVar(value="Select Mood")
        self.mood_menu = ctk.CTkOptionMenu(self, values=list(playlist_links.keys()), variable=self.mood_var, command=self.on_mood_selected)
        self.mood_menu.configure(fg_color="#1E1E1E", button_color="#3B4252", text_color="#D8DEE9", dropdown_fg_color="#2E2E2E", dropdown_text_color="#D8DEE9")
        self.mood_menu.pack(pady=12)

        input_frame = ctk.CTkFrame(self, fg_color="#000000")
        input_frame.pack(pady=12)
        ctk.CTkLabel(input_frame, text="Or describe your mood:", font=ctk.CTkFont(size=14), text_color="#D8DEE9", fg_color="#000000").pack(side="left", padx=(0, 8))
        self.text_input = ctk.CTkEntry(input_frame, width=320, fg_color="#1E1E1E", text_color="#D8DEE9", border_color="#4C566A")
        self.text_input.pack(side="left")
        ctk.CTkButton(input_frame, text="Analyze", command=self.analyze_text, fg_color="#5E81AC", hover_color="#81A1C1").pack(side="left", padx=8)

        ctk.CTkButton(self, text="Start Facial Detection", command=self.start_facial_detection, fg_color="#5E81AC", hover_color="#81A1C1").pack(pady=15)

        self.voice_detecting = False
        self.voice_thread = None
        self.voice_button = ctk.CTkButton(self, text="Start Voice Detection", command=self.toggle_voice_detection, fg_color="#5E81AC", hover_color="#81A1C1")
        self.voice_button.pack(pady=8)

        self.status_label = ctk.CTkLabel(self, text="Waiting for input...", font=ctk.CTkFont(size=14), text_color="#D8DEE9", fg_color="#000000")
        self.status_label.pack(pady=14)

        self.song_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=16, weight="bold"), text_color="#D08770", fg_color="#000000")
        self.song_label.pack(pady=7)

        self.progress_frame = ctk.CTkFrame(self, fg_color="#000000")
        self.progress_frame.pack(pady=7, fill="x", padx=20)

        self.elapsed_label = ctk.CTkLabel(self.progress_frame, text="0:00", font=ctk.CTkFont(size=12), text_color="#D8DEE9", fg_color="#000000")
        self.elapsed_label.pack(side="left", padx=(10, 0))

        self.progress_var = ctk.DoubleVar(value=0)
        self.progress_bar = ctk.CTkSlider(self.progress_frame, from_=0, to=100, variable=self.progress_var, command=self.seek_song, width=550, button_color="#5E81AC", progress_color="#81A1C1", fg_color="#1E1E1E")
        self.progress_bar.pack(side="left", padx=10, fill="x", expand=True)

        self.remaining_label = ctk.CTkLabel(self.progress_frame, text="0:00", font=ctk.CTkFont(size=12), text_color="#D8DEE9", fg_color="#000000")
        self.remaining_label.pack(side="left", padx=(0, 10))

        controls = ctk.CTkFrame(self, fg_color="#000000")
        controls.pack(pady=12)
        self.next_button = ctk.CTkButton(controls, text="⏭️ Next", command=self.next_song, state="disabled", fg_color="#5E81AC", hover_color="#81A1C1")
        self.next_button.pack(side="left", padx=8)
        self.pause_button = ctk.CTkButton(controls, text="⏸️ Pause", command=self.pause_music, state="disabled", fg_color="#5E81AC", hover_color="#81A1C1")
        self.pause_button.pack(side="left", padx=8)
        self.resume_button = ctk.CTkButton(controls, text="▶️ Resume", command=self.resume_music, state="disabled", fg_color="#5E81AC", hover_color="#81A1C1")
        self.resume_button.pack(side="left", padx=8)

        self.song_list_frame = ctk.CTkFrame(self, fg_color="#000000")
        self.song_list_frame.pack(pady=12, fill="both", expand=True)
        self.song_canvas = ctk.CTkCanvas(self.song_list_frame, bg="#000000", highlightthickness=0)
        self.song_scrollbar = ctk.CTkScrollbar(self.song_list_frame, orientation="vertical", command=self.song_canvas.yview)
        self.song_scrollbar.pack(side="right", fill="y")
        self.song_canvas.pack(side="left", fill="both", expand=True)
        self.song_canvas.configure(yscrollcommand=self.song_scrollbar.set)

        self.song_listbox = ctk.CTkFrame(self.song_canvas, fg_color="#000000")
        self.song_canvas.create_window((0, 0), window=self.song_listbox, anchor="nw")

        self.song_listbox.bind("<Configure>", lambda e: self.song_canvas.configure(scrollregion=self.song_canvas.bbox("all")))

        self.video_titles = []
        self.video_stream_urls = []
        self.current_index = -1
        self.player = None
        self.event_manager = None
        self.playing = False
        self.song_labels = []
        self.updating_progress = False

    def on_mood_selected(self, choice):
        self.load_playlist(choice)

    def analyze_text(self):
        text = self.text_input.get()
        if not text.strip():
            self.status_label.configure(text="Please enter some text.")
            return
        self.status_label.configure(text="Analyzing text...")
        threading.Thread(target=self._analyze_text_thread, args=(text,), daemon=True).start()

    def _analyze_text_thread(self, text):
        mood = correct_and_classify(text)
        if mood is None:
            mood = classify_by_sentiment(text)
        if mood not in playlist_links:
            mood = "neutral"
        self.status_label.configure(text=f"Detected mood: {mood}")
        self.load_playlist(mood)

    def start_facial_detection(self):
        self.status_label.configure(text="Starting facial detection...")
        detector_thread = FacialMoodDetector(self.load_playlist)
        detector_thread.start()

    def toggle_voice_detection(self):
        if self.voice_detecting:
            self.voice_detecting = False
            self.voice_button.configure(text="Start Voice Detection")
            self.status_label.configure(text="Voice detection stopped.")
        else:
            self.voice_detecting = True
            self.voice_button.configure(text="Stop Voice Detection")
            self.status_label.configure(text="Listening for voice...")
            self.voice_thread = threading.Thread(target=self.voice_detection_thread, daemon=True)
            self.voice_thread.start()

    def voice_detection_thread(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
        while self.voice_detecting:
            try:
                with mic as source:
                    audio = recognizer.listen(source, phrase_time_limit=5)
                text = recognizer.recognize_google(audio)
                self.status_label.configure(text=f"Recognized: {text}")
                mood = correct_and_classify(text)
                if mood is None:
                    mood = classify_by_sentiment(text)
                if mood not in playlist_links:
                    mood = "neutral"
                self.load_playlist(mood)
                self.voice_detecting = False
                self.voice_button.configure(text="Start Voice Detection")
                break
            except Exception:
                continue

    def load_playlist(self, mood):
        self.status_label.configure(text=f"Loading playlist for mood: {mood}...")
        self.current_index = -1
        self.video_titles.clear()
        self.video_stream_urls.clear()
        self.clear_song_list()
        playlist_url = playlist_links.get(mood)
        if not playlist_url:
            self.status_label.configure(text=f"No playlist for mood: {mood}")
            return
        ydl_opts = {"quiet": True, "ignoreerrors": True, "extract_flat": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            entries = info.get("entries", [])
            for entry in entries:
                if entry and "title" in entry and "url" in entry:
                    self.video_titles.append(entry["title"])
                    self.video_stream_urls.append(f"https://www.youtube.com/watch?v={entry['id']}")
        self.populate_song_list()
        if self.video_stream_urls:
            self.play_song(0)

    def clear_song_list(self):
        for lbl in self.song_labels:
            lbl.destroy()
        self.song_labels.clear()

    def populate_song_list(self):
        for lbl in self.song_labels:
            lbl.destroy()
        self.song_labels.clear()

        for i, title in enumerate(self.video_titles):
            lbl = ctk.CTkLabel(
                self.song_listbox,
                text=title,
                fg_color="#2E3440" if i % 2 == 0 else "#3B4252",
                text_color="#D8DEE9",
                width=800,
                corner_radius=6
            )
            lbl.pack(pady=2, padx=5, fill="x")
            lbl.bind("<Button-1>", lambda e, idx=i: self.play_song(idx))
            self.song_labels.append(lbl)

    def play_song(self, index):
        if index < 0 or index >= len(self.video_stream_urls):
            return
        self.current_index = index
        if self.player:
            self.player.stop()
            self.player.release()
            self.player = None

        self.status_label.configure(text=f"Loading: {self.video_titles[index]}")
        self.song_label.configure(text=self.video_titles[index])

        ydl_opts = {
            "quiet": True,
            "format": "bestaudio/best",
            "noplaylist": True,
            "extract_flat": False,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.video_stream_urls[index], download=False)
                stream_url = info_dict["url"]

            self.player = vlc.MediaPlayer(stream_url)
            self.event_manager = self.player.event_manager()
            self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self._song_ended)
            self.player.play()
            self.playing = True

            self.next_button.configure(state="normal")
            self.pause_button.configure(state="normal")
            self.resume_button.configure(state="normal")

            if not self.updating_progress:
                self.updating_progress = True
                threading.Thread(target=self.update_progress_bar, daemon=True).start()

        except Exception as e:
            self.status_label.configure(text=f"Playback error: {str(e)}")

    def _song_ended(self, event):
        self.next_song()

    def next_song(self):
        if self.current_index + 1 < len(self.video_stream_urls):
            self.play_song(self.current_index + 1)
        else:
            # No next song, disable next button and reset progress
            self.next_button.configure(state="disabled")
            self.pause_button.configure(state="disabled")
            self.resume_button.configure(state="disabled")
            self.status_label.configure(text="Playlist ended.")
            self.song_label.configure(text="")
            self.progress_var.set(0)
            self.elapsed_label.configure(text="0:00")
            self.remaining_label.configure(text="0:00")
            if self.player:
                self.player.stop()
                self.player.release()
                self.player = None
            self.playing = False
            self.updating_progress = False

    def pause_music(self):
        if self.player and self.playing:
            self.player.pause()

    def resume_music(self):
        if self.player and self.playing:
            self.player.play()

    def seek_song(self, value):
        if self.player:
            length = self.player.get_length()
            if length > 0:
                self.player.set_time(int(length * (value / 100)))

    def update_progress_bar(self):
        while self.playing and self.player:
            try:
                length = self.player.get_length()
                current_time = self.player.get_time()
                if length > 0 and current_time >= 0:
                    progress = (current_time / length) * 100
                    self.progress_var.set(progress)
                    elapsed_sec = current_time // 1000
                    remaining_sec = (length - current_time) // 1000
                    elapsed_str = f"{elapsed_sec // 60}:{elapsed_sec % 60:02d}"
                    remaining_str = f"{remaining_sec // 60}:{remaining_sec % 60:02d}"
                    self.elapsed_label.configure(text=elapsed_str)
                    self.remaining_label.configure(text=remaining_str)
                else:
                    self.progress_var.set(0)
                    self.elapsed_label.configure(text="0:00")
                    total_sec = length // 1000 if length > 0 else 0
                    total_str = f"{total_sec // 60}:{total_sec % 60:02d}"
                    self.remaining_label.configure(text=total_str)
                time.sleep(0.5)
            except Exception:
                break
        self.updating_progress = False

if __name__ == "__main__":
    app = YouTubeMoodPlayer()
    app.mainloop() 
