# 🎵 Smart Mood-Responsive Music Generator

## 🧠 Project Overview

**Smart Mood-Responsive Music Generator** is an intelligent desktop music player that dynamically selects and plays curated playlists based on the user's current mood. The application detects emotions through **facial expression analysis** (via webcam) and **natural language input**, enabling a personalized and emotionally adaptive music experience.

It integrates **computer vision**, **natural language processing**, and **YouTube music streaming** to enhance emotional well-being, relaxation, and productivity through mood-matched playlists.

---

## 🌟 Key Features

- 🧍‍♂️ **Facial Mood Detection**: Detects the user's mood using real-time webcam feed and facial emotion recognition (FER).
- ✍️ **Text Mood Analysis**: Classifies emotional sentiment from written text using keyword matching and sentiment analysis.
- 🎯 **Keyword Correction**: Auto-corrects user input and matches it to mood categories (e.g., "glad" → happy).
- 🎼 **Automated Playlist Matching**: Selects and loads a YouTube playlist that fits the detected mood.
- ▶️ **Music Player UI**: Includes playback controls, progress tracking, playlist display, and mood selection.
- 🔄 **Seamless Integration**: Supports manual mood selection, facial detection, or text-based detection—all linked to curated playlists.

---

## 🧰 Technologies Used

- **Python**
- **Tkinter** – for GUI
- **OpenCV** – for webcam and image processing
- **FER (Facial Expression Recognition)** – for detecting emotional states
- **TextBlob** – for NLP-based sentiment analysis and spell correction
- **yt_dlp** – to fetch YouTube playlist and stream audio
- **python-vlc** – for media playback

---

## 📦 Installation

> **Requirements:**  
> Python 3.7+ and pip

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/smart-mood-music-generator.git
   cd smart-mood-music-generator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

---

## 🖥️ How It Works

### 🎭 Facial Mood Detection
- Uses your webcam via OpenCV
- FER detects dominant emotion (happy, sad, angry, etc.)
- Automatically maps the emotion to a matching playlist

### ✍️ Text-Based Mood Input
- User writes how they feel
- TextBlob corrects spelling and extracts sentiment
- Matches input to predefined mood keywords or polarity score

### 🎧 Playlist Selection
- Each mood is mapped to a specific YouTube playlist
- `yt_dlp` is used to extract song titles and stream URLs
- VLC media player module streams the audio directly

---

## 💬 Supported Moods

- Happy
- Sad
- Angry
- Calm
- Anxious
- Tired
- Neutral

Each mood maps to a curated YouTube playlist via URL.

---

## 🎮 Controls

| Button            | Function                              |
|-------------------|---------------------------------------|
| `Start Facial Detection` | Starts real-time emotion scanning via webcam |
| `Analyze`         | Analyzes typed mood text input        |
| `Next`            | Plays the next song in the playlist   |
| `Pause` / `Resume`| Controls playback state               |
| Playlist Box      | Lets user click to play a specific song |
| Slider Bar        | Shows and controls playback progress  |

---

## 🧪 Example Use Cases

- A student wants upbeat music to stay focused—types "I feel energetic" → playlist selected: **Happy**
- A user looks tired on webcam → detected mood: **Tired** → plays relaxing songs
- Typing "I'm feeling low" → detected: **Sad** → triggers a comforting playlist

---

## 📌 Notes

- Internet connection is required to stream songs from YouTube.
- Make sure your webcam is accessible and not used by other applications.
- Some YouTube links may change over time; update `playlist_links` in the code if needed.

---
