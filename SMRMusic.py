import tkinter as tk
from tkinter import ttk
import threading
import time
import difflib
from textblob import TextBlob
import yt_dlp
import vlc
import cv2
from fer import FER
import speech_recognition as sr

# === Mood keywords ===
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

# Facial Emotion Detector Thread
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
            "tired": "tired"
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

class YouTubeMoodPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Mood-Responsive Music Generator")
        self.root.geometry("880x720")
        self.root.configure(bg="white")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TLabel", background="white", foreground="#333", font=("Segoe UI", 11))
        self.style.configure("TEntry", fieldbackground="#f0f0f0", foreground="black")
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), background="#007ACC", foreground="white")
        self.style.map("TButton", background=[("active", "#005A9E")])
        self.style.configure("TScale", background="white")

        title = ttk.Label(root, text="🎼 Smart Mood-Responsive Music Generator", font=("Segoe UI", 20, "bold"), foreground="#007ACC")
        title.pack(pady=25)

        self.mood_var = tk.StringVar()
        self.mood_menu = ttk.OptionMenu(root, self.mood_var, "Select Mood", *playlist_links.keys(), command=self.on_mood_selected)
        self.mood_menu.pack(pady=8)

        input_frame = ttk.Frame(root)
        input_frame.pack(pady=10)
        ttk.Label(input_frame, text="Or describe your mood:").pack(side=tk.LEFT, padx=(0, 5))
        self.text_input = ttk.Entry(input_frame, width=40)
        self.text_input.pack(side=tk.LEFT)
        ttk.Button(input_frame, text="Analyze", command=self.analyze_text).pack(side=tk.LEFT, padx=5)

        ttk.Button(root, text="Start Facial Detection", command=self.start_facial_detection).pack(pady=10)

        # --- Voice Detection button below Facial Detection ---
        self.voice_detecting = False
        self.voice_thread = None
        self.voice_button = ttk.Button(root, text="Start Voice Detection", command=self.toggle_voice_detection)
        self.voice_button.pack(pady=5)

        self.status_label = ttk.Label(root, text="Waiting for input...", font=("Segoe UI", 10, "italic"))
        self.status_label.pack(pady=10)

        self.song_label = ttk.Label(root, text="", font=("Segoe UI", 13, "bold"), foreground="#CC5500")
        self.song_label.pack(pady=5)

        self.progress_frame = ttk.Frame(root)
        self.progress_frame.pack(pady=5)
        self.elapsed_label = ttk.Label(self.progress_frame, text="0:00")
        self.elapsed_label.pack(side=tk.LEFT)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Scale(self.progress_frame, from_=0, to=100, variable=self.progress_var, orient=tk.HORIZONTAL, command=self.seek_song, length=450)
        self.progress_bar.pack(side=tk.LEFT, padx=10)
        self.remaining_label = ttk.Label(self.progress_frame, text="0:00")
        self.remaining_label.pack(side=tk.LEFT)

        controls = ttk.Frame(root)
        controls.pack(pady=10)
        self.next_button = ttk.Button(controls, text="⏭️ Next", command=self.next_song, state=tk.DISABLED)
        self.next_button.pack(side=tk.LEFT, padx=5)
        self.pause_button = ttk.Button(controls, text="⏸️ Pause", command=self.pause_music, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        self.resume_button = ttk.Button(controls, text="▶️ Resume", command=self.resume_music, state=tk.DISABLED)
        self.resume_button.pack(side=tk.LEFT, padx=5)

        self.song_listbox = tk.Listbox(root, width=90, height=10, bg="#f9f9f9", fg="#333", font=("Segoe UI", 10))
        self.song_listbox.pack(pady=10)
        self.song_listbox.bind("<<ListboxSelect>>", self.on_song_selected)

        self.player = None
        self.event_manager = None
        self.video_urls = []
        self.video_titles = []
        self.current_index = 0
        self.playing = False
        self.duration = 0
        self.update_thread = threading.Thread(target=self.update_progress, daemon=True)
        self.update_thread.start()

    def start_facial_detection(self):
        self.status_label.config(text="Detecting facial expression...")
        FacialMoodDetector(self.load_playlist).start()

    def on_mood_selected(self, mood):
        if mood != "Select Mood":
            self.text_input.delete(0, tk.END)
            threading.Thread(target=self.load_playlist, args=(mood,), daemon=True).start()

    def analyze_text(self):
        text = self.text_input.get().strip()
        if not text:
            self.status_label.config(text="Please type something.")
            return
        mood = correct_and_classify(text)
        if not mood:
            mood = classify_by_sentiment(text)
        self.mood_var.set(mood)
        threading.Thread(target=self.load_playlist, args=(mood,), daemon=True).start()

    def load_playlist(self, mood):
        self.stop_music()
        self.status_label.config(text=f"Loading playlist for: {mood}")
        try:
            url = playlist_links[mood]
            self.video_urls, self.video_titles = self.fetch_playlist(url)
            self.song_listbox.delete(0, tk.END)
            for title in self.video_titles:
                self.song_listbox.insert(tk.END, title)
            self.status_label.config(text=f"{len(self.video_titles)} songs loaded.")
            self.current_index = 0
            self.next_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.NORMAL)
            self.resume_button.config(state=tk.DISABLED)
            self.play_song(0)
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")

    def fetch_playlist(self, url):
        ydl_opts = {'quiet': True, 'extract_flat': True, 'force_generic_extractor': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            entries = info.get('entries', [])
            urls = [f"https://www.youtube.com/watch?v={entry['id']}" for entry in entries if 'id' in entry]
            titles = [entry.get('title', 'Unknown Title') for entry in entries]
            return urls, titles

    def get_stream_info(self, url):
        ydl_opts = {'quiet': True, 'format': 'bestaudio/best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info['url'], info.get('title', ''), int(info.get('duration', 0))

    def play_song(self, index):
        if index < 0 or index >= len(self.video_urls):
            return
        self.current_index = index
        stream_url, title, self.duration = self.get_stream_info(self.video_urls[index])
        if self.player:
            self.player.stop()
        self.player = vlc.MediaPlayer(stream_url)
        self.event_manager = self.player.event_manager()
        self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.song_finished)
        self.player.play()
        self.song_label.config(text=title)
        self.song_listbox.selection_clear(0, tk.END)
        self.song_listbox.selection_set(index)
        self.song_listbox.activate(index)
        self.progress_var.set(0)
        self.elapsed_label.config(text="0:00")
        self.remaining_label.config(text=self.format_time(self.duration))
        self.playing = True
        # Update buttons states
        self.pause_button.config(state=tk.NORMAL)
        self.resume_button.config(state=tk.DISABLED)

    def pause_music(self):
        if self.player and self.playing:
            self.player.pause()
            self.playing = False
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.NORMAL)

    def resume_music(self):
        if self.player and not self.playing:
            self.player.play()
            self.playing = True
            self.pause_button.config(state=tk.NORMAL)
            self.resume_button.config(state=tk.DISABLED)

    def stop_music(self):
        if self.player:
            self.player.stop()
            self.playing = False
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.DISABLED)
            self.song_label.config(text="")
            self.status_label.config(text="Stopped.")

    def next_song(self):
        next_index = (self.current_index + 1) % len(self.video_urls)
        self.play_song(next_index)

    def song_finished(self, event):
        self.next_song()

    def update_progress(self):
        while True:
            if self.player and self.playing:
                try:
                    pos = self.player.get_time() // 1000
                    if pos >= 0:
                        self.progress_var.set((pos / self.duration) * 100 if self.duration > 0 else 0)
                        self.elapsed_label.config(text=self.format_time(pos))
                        self.remaining_label.config(text=self.format_time(max(0, self.duration - pos)))
                except:
                    pass
            time.sleep(1)

    def seek_song(self, val):
        if self.player and self.duration > 0:
            seek_time = (float(val) / 100) * self.duration
            self.player.set_time(int(seek_time * 1000))

    def format_time(self, seconds):
        m, s = divmod(int(seconds), 60)
        return f"{m}:{s:02d}"

    def on_song_selected(self, event):
        selection = self.song_listbox.curselection()
        if selection:
            self.play_song(selection[0])

    # --- Voice Detection Section ---

    def toggle_voice_detection(self):
        if self.voice_detecting:
            self.voice_detecting = False
            self.voice_button.config(text="Start Voice Detection")
            self.status_label.config(text="Voice detection stopped.")
        else:
            self.voice_detecting = True
            self.voice_button.config(text="Stop Voice Detection")
            self.status_label.config(text="Listening for your mood (say something)...")
            self.voice_thread = threading.Thread(target=self.voice_detection_thread, daemon=True)
            self.voice_thread.start()

    def voice_detection_thread(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
        while self.voice_detecting:
            with mic as source:
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    text = recognizer.recognize_google(audio)
                    self.status_label.config(text=f"You said: {text}")
                    mood = correct_and_classify(text)
                    if not mood:
                        mood = classify_by_sentiment(text)
                    self.mood_var.set(mood)
                    self.load_playlist(mood)
                    self.voice_detecting = False
                    self.voice_button.config(text="Start Voice Detection")
                    break
                except sr.WaitTimeoutError:
                    self.status_label.config(text="Listening timed out, please try again.")
                except sr.UnknownValueError:
                    self.status_label.config(text="Sorry, I didn't catch that. Try again.")
                except sr.RequestError as e:
                    self.status_label.config(text=f"API error: {e}")
            time.sleep(0.1)

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeMoodPlayer(root)
    root.mainloop()
