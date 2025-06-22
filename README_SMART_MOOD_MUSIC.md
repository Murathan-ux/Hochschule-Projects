# 🎶 Smart Mood-Responsive Music Generator (SMRG)

## 🧠 Overview

The **Smart Mood-Responsive Music Generator (SMRG)** is an AI-powered, Python-based desktop application that plays dynamically curated music from YouTube based on real-time emotional input. It offers a multi-modal mood detection system utilizing:

- **Facial Emotion Recognition (FER)** via webcam (deep learning-based),
- **Speech Emotion Recognition** via real-time voice transcription and sentiment analysis,
- **Text-Based Mood Inference** with spelling correction, keyword detection, and sentiment analysis,
- **Manual Mood Selection** for user-driven input.

Once the user's mood is inferred, the app selects and plays music from a pre-defined YouTube playlist corresponding to the detected mood. This application is useful for mood regulation, relaxation, study focus, or emotional awareness.

---

## 💻 System Requirements

- **Operating System:** Windows / macOS / Linux
- **Python Version:** 3.10.11 (recommended)
- **Python IDE:** PyCharm (recommended)
  - [Download PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/)
- **Hardware Requirements:**
  - Webcam (for facial detection)
  - Microphone (for voice detection)
- **Software Requirements:**
  - VLC Media Player (installed and added to system PATH)
    - [Download VLC](https://www.videolan.org/vlc/)
- **Internet Connection:** Required for YouTube streaming and voice recognition

---

## 📦 Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/smrg-music.git
cd smrg-music
```

### 2. Install Python 3.10.11 (if not installed)

- [Download Python 3.10.11](https://www.python.org/downloads/release/python-31011/)

Ensure `python3.10` is added to your system PATH.

### 3. Create Virtual Environment (Optional but recommended)

```bash
python3.10 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Required Python Packages

Each dependency and its tested version for Python 3.10.11:

```bash
pip install opencv-python==4.9.0.80
pip install fer==22.4.0
pip install textblob==0.17.1
pip install yt-dlp==2024.4.9
pip install python-vlc==3.0.18122
pip install SpeechRecognition==3.10.1
pip install pyaudio==0.2.13
pip install customtkinter==5.2.1
pip install moviepy==1.0.3
pip install tensorflow==2.10.0
```

> ⚠️ **Note**: `pyaudio` may require system-level tools:
> - **Linux**: `sudo apt install portaudio19-dev`
> - **macOS**: `brew install portaudio`

### 5. Install VLC Media Player

- Download from [VLC Website](https://www.videolan.org/vlc/)
- Ensure it is added to your system PATH

---

## ▶️ How to Run

```bash
python main.py
```

On execution, the GUI will appear with options for mood-based interaction.

---

## 🎯 Mood Detection Modes

### 🎭 Facial Recognition
- Uses OpenCV and FER to analyze webcam feed and identify emotional expression.
- Maps expressions like "happy", "sad", "angry", etc., to mood-specific playlists.

### ✍️ Text Input
- Accepts user-written text describing mood.
- Applies spelling correction using TextBlob.
- Combines keyword matching and sentiment polarity to classify mood.

### 🎤 Voice Detection
- Records and transcribes speech using Google Speech API.
- Extracts mood using NLP and sentiment analysis.

### 🖱️ Manual Mood Selection
- Dropdown menu allows manual mood selection from supported options.

---

## 🎼 Supported Moods

- Happy
- Sad
- Angry
- Calm
- Anxious
- Tired
- Neutral

Moods are linked to curated YouTube playlists.

---

## 🖱️ Interface Controls

| Control                   | Description                                        |
|---------------------------|----------------------------------------------------|
| `Start Facial Detection`  | Launch real-time facial emotion recognition       |
| `Start Voice Detection`   | Record and analyze spoken emotion                 |
| `Analyze`                 | Analyze typed mood text                           |
| `Next`                    | Play next song in playlist                        |
| `Pause` / `Resume`        | Pause or resume audio playback                    |
| `Mood Dropdown Menu`      | Manually select mood                              |
| `Progress Slider`         | Navigate within the currently playing song        |

---

## 🧪 Troubleshooting

- **No Audio?** Ensure VLC is installed and path is properly set.
- **Microphone issues?** Check OS permissions and input device settings.
- **Facial recognition fails?** Improve lighting and webcam visibility.
- **`pyaudio` install errors?** Use prebuilt wheel files or system build tools.

---

## 🔍 Example Use Cases

- *"I'm burned out"* → Detected mood: **Tired** → Calm music plays.
- *"I'm excited!"* → Detected mood: **Happy** → Upbeat songs begin.
- Webcam shows sad face → Detected mood: **Sad** → Soothing music selected.

---

## 🙏 Acknowledgements

- [FER (Facial Expression Recognition)](https://github.com/justinshenk/fer)
- [OpenCV](https://opencv.org/)
- [TextBlob NLP](https://textblob.readthedocs.io/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [CustomTkinter GUI Toolkit](https://github.com/TomSchimansky/CustomTkinter)
- [VLC Python Bindings](https://wiki.videolan.org/PythonBindings/)
- [MoviePy Video Editing](https://zulko.github.io/moviepy/)
- [TensorFlow (used by FER backend)](https://www.tensorflow.org/)
- [PyCharm IDE](https://www.jetbrains.com/pycharm/)