
# 🎵 Smart Mood-Responsive Music Generator

## 🧠 Overview

The **Smart Mood-Responsive Music Generator** is a Python-based desktop application that plays mood-adaptive music by detecting the user's emotional state through facial expressions, voice input, or written text. It integrates advanced technologies such as:

- Facial Emotion Recognition
- Natural Language Processing (NLP)
- Speech Recognition
- YouTube playlist streaming

This application offers a personalized listening experience and can be used for wellness, focus enhancement, or emotional reflection.

---

## 🌟 Key Features

- 🎭 **Facial Mood Detection** via webcam using deep learning.
- ✍️ **Text Input Analysis** with sentiment and keyword detection.
- 🎤 **Voice Mood Detection** via real-time speech-to-text conversion.
- 📝 **Spelling Correction & Mood Classification** using NLP.
- 🎶 **YouTube Playlist Streaming** based on mood classification.
- 🎛️ **Interactive GUI** with playback controls and real-time progress bar.

---

## 💻 System Requirements

- Operating System: Windows / macOS / Linux
- Python: 3.10 recommended
- Internet connection (for streaming)
- Webcam and microphone access
- VLC Media Player (installed on system)

---

## 📦 Installation Guide

### 1. Clone the SMRG_Music.py

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

**Example `requirements.txt`** (with tested versions):

```
opencv-python==4.9.0.80
fer==22.4.0
textblob==0.17.1
yt-dlp==2024.4.9
python-vlc==3.0.18122
SpeechRecognition==3.10.1
pyaudio==0.2.13
```
> ⚠️ Note: `pyaudio` may require system-level build tools (e.g., `portaudio` on Linux/macOS).

### 3. Install VLC Media Player

The application relies on VLC for streaming audio. Download and install the desktop version:

- 📥 [VLC Download Page](https://www.videolan.org/vlc/)

Make sure VLC is added to your system PATH or installed in the default location.

---

## ▶️ How to Run

```bash
python main.py
```

Upon launch, a GUI will open allowing interaction through text, voice, facial detection, or manual mood selection.

---

## 🧠 Mood Detection Techniques

### 🎭 Facial Recognition

- Utilizes OpenCV and FER to capture and analyze webcam frames.
- Detects primary emotion (e.g., "happy", "sad", etc.).

### ✍️ Text Analysis

- Accepts user-written input.
- Applies spell correction (via TextBlob).
- Uses sentiment polarity and keyword matching for mood classification.

### 🎤 Voice Detection

- Records audio from mic.
- Transcribes speech using Google Speech Recognition API.
- Extracts mood via keyword and sentiment analysis.

---

## 🎼 Supported Moods

- Happy
- Sad
- Angry
- Calm
- Anxious
- Tired
- Neutral

Moods are mapped to specific YouTube playlists in the code (`playlist_links` dictionary).

---

## 🖱️ Interface Controls

| Control                   | Description                                        |
|---------------------------|----------------------------------------------------|
| `Start Facial Detection`  | Begin facial emotion recognition via webcam       |
| `Start Voice Detection`   | Start/stop voice mood detection                   |
| `Analyze`                 | Analyze text input and detect mood                |
| `Next`                    | Skip to next song                                 |
| `Pause` / `Resume`        | Playback control                                  |
| Playlist Box              | Select song manually                              |
| Progress Slider           | Seek within the current track                     |

---

## 🧪 Troubleshooting

- **Audio doesn't play?** Make sure VLC is installed and accessible.
- **Microphone not working?** Check OS privacy settings.
- **FER not detecting face?** Ensure good lighting and webcam is accessible.
- **Errors in `pyaudio` install?** Use wheel file or build tools for your OS.

---

## 🔍 Example Use Cases

- Student types "I'm burned out" → Mood: `Tired` → Relaxing playlist.
- User says "I'm excited today!" → Mood: `Happy` → Energetic songs play.
- Camera detects sad expression → Mood: `Sad` → Comforting music starts.

---

## 🙏 Acknowledgements

- [FER Library](https://github.com/justinshenk/fer)
- [yt-dlp Project](https://github.com/yt-dlp/yt-dlp)
- [TextBlob NLP](https://textblob.readthedocs.io/)
- [VLC Python Bindings](https://wiki.videolan.org/PythonBindings/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
