# 🎶 Smart Mood-Responsive Music Generator 

## 🧠 Overview

The **Smart Mood-Responsive Music Generator** is a Python-based application that streams dynamically curated music from YouTube based on real-time emotional input. It offers a multi-modal mood detection system utilizing:

- **Facial Emotion Recognition** via webcam (deep learning-based),
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

## 📦 User Guideline

### 1. Install Python 3.10.11

- [Download Python 3.10.11](https://www.python.org/downloads/release/python-31011/)

Ensure `python3.10.11` is added to your system PATH as an interpreter in PhCharm.

### 2. Create a Python file and a Virtual Environment in PhCharm

```bash
python3.10 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Required PyCharm Modules

Each dependency and its version for Python 3.10.11:

Type the prompts above to the PhCharm terminal

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

---

## 4. ▶️ Run the Code

Clone the code in the Python file and run it 

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

- * User types "I'm chill"* → Detected mood: **Tired** → Tired music list begins.
- * User says "I'm feeling very happy!"* → Detected mood: **Happy** → Hapy music list begins.
- Webcam detects sad expression → Detected mood: **Sad** → Sad music list begins.

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
