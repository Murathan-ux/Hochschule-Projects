# 🎵 Smart Mood-Responsive Music Generator

## 🧠 Project Overview

**Smart Mood-Responsive Music Generator** is an intelligent desktop music player that dynamically selects and plays curated playlists based on the user's current mood. The application detects emotions through:

- **Facial expression analysis** (via webcam),
- **Natural language input**, and
- **Voice-based mood detection**.

This creates a personalized, emotionally adaptive music experience by integrating **computer vision**, **speech recognition**, **natural language processing**, and **YouTube music streaming**.

---

## 🌟 Key Features

- 🧍‍♂️ **Facial Mood Detection** – Real-time webcam-based emotion recognition using FER (Facial Expression Recognition).
- ✍️ **Text Mood Analysis** – Extracts mood via user input using keyword detection and sentiment analysis.
- 🎤 **Voice Mood Detection** – Detects emotion from spoken words using speech-to-text + sentiment classification.
- 📝 **Keyword Correction** – Automatically corrects mood-related typos (e.g., "gladd" → "happy").
- 🎼 **Automated Playlist Matching** – Dynamically maps detected mood to a curated YouTube playlist.
- ▶️ **Music Player UI** – Includes playback controls, progress tracking, and song selection.
- 🧩 **Multi-Input Flexibility** – Use text, voice, facial expression, or manual dropdown to set your mood.

---

## 🧰 Technologies Used

- **Python 3.7+**
- **Tkinter** – GUI framework
- **OpenCV** – Webcam access and frame capture
- **FER** – Facial emotion recognition
- **TextBlob** – NLP (sentiment analysis, spelling correction)
- **SpeechRecognition** – Voice input and transcription
- **yt_dlp** – Extract YouTube playlist/song info
- **python-vlc** – Stream and control audio playback

---

## 📦 Installation

> **Requirements:**  
> Python 3.7+ and internet access

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/smart-mood-music-generator.git
   cd smart-mood-music-generator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Example `requirements.txt`:
   ```
   opencv-python
   fer
   textblob
   yt-dlp
   python-vlc
   SpeechRecognition
   pyaudio
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

---

## 🖥️ How It Works

### 🎭 Facial Mood Detection
- Captures live webcam video
- Detects dominant emotion using FER
- Matches emotion to playlist (e.g., "angry" → intense music)

### ✍️ Text Mood Input
- User types something like: "I'm feeling a bit off today"
- System corrects spelling, analyzes sentiment and keyword match
- Maps to a mood like: "neutral"

### 🎤 Voice Mood Input
- Click `Start Voice Detection` and speak how you feel
- Converts speech to text, analyzes mood, and plays appropriate playlist

### 🎧 Playlist Selection & Playback
- Each mood links to a specific YouTube playlist
- `yt_dlp` fetches video URLs and metadata
- VLC streams audio without needing YouTube login

---

## 💬 Supported Moods

- Happy
- Sad
- Angry
- Calm
- Anxious
- Tired
- Neutral

You can modify or update the `playlist_links` dictionary in the code to assign new playlists.

---

## 🎮 Controls

| Button                | Function                                           |
|------------------------|----------------------------------------------------|
| `Start Facial Detection` | Detect mood from facial expression               |
| `Start Voice Detection`  | Analyze mood from your spoken input              |
| `Analyze`             | Detect mood from written input                     |
| `Next`                | Skip to next song                                  |
| `Pause` / `Resume`    | Playback control                                   |
| Playlist Box          | Select a song manually from loaded playlist        |
| Slider Bar            | Shows & controls current song progress             |

---

## 🧪 Example Use Cases

- A student feeling low types: "I'm burned out" → detected as **Tired** → calming playlist plays.
- A user says "I'm excited today!" via microphone → detected as **Happy** → upbeat songs play.
- The camera detects a sad expression → mood: **Sad** → launches comforting music.

---

## 📌 Notes

- Ensure your webcam and microphone are accessible by the system.
- Requires internet access to stream songs.
- Playlist links can be edited in the `playlist_links` dictionary in the code.
- For best results, avoid running multiple detection modes simultaneously.

---

## 🧑‍💻 Author

Developed by [Your Name]  
Feel free to fork, contribute or suggest improvements via pull requests or issues!

---

## 📜 License

This project is licensed under the MIT License.