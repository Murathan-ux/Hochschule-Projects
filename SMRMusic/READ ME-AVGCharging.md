Speech to Sentiment Analysis

This project converts a speech audio file to text using Google Cloud Speech-to-Text API, then analyzes the sentiment of the transcribed text using Google Cloud Natural Language API.

Contents

About the Project
Prerequisites
Google Cloud API Setup
Installation
Usage
Example Output
Important Notes
Contributing
About the Project

This project detects the sentiment (happy, sad, neutral) of spoken words in an audio file. It can be used in apps that respond to user emotions detected from voice, like mood-based music players.

Prerequisites

Python 3.7 or higher
A Google Cloud account
Google Cloud SDK (optional but recommended)
Required Python packages: google-cloud-speech, google-cloud-language
Google Cloud API Setup

Go to Google Cloud Console.
Create a new project or select an existing one.
Enable the following APIs:
Speech-to-Text API
Natural Language API
Navigate to APIs & Services > Credentials.
Create a Service Account with Editor role (or least privilege needed).
Generate and download a JSON key file for this service account.
Set the environment variable to point to your JSON key file:
On macOS/Linux terminal:

export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
On Windows command prompt:

setx GOOGLE_APPLICATION_CREDENTIALS "C:\path\to\your\service-account-file.json"
Important:
Do NOT share your JSON key file publicly or commit it to any public repository. Each user should create and use their own key for security reasons.
Installation

Clone this repository or download the ZIP.
Install required Python packages:
pip install google-cloud-speech google-cloud-language
Usage

Run the Python script:

python speech_to_sentiment_finalll.py
You will be prompted to enter the path to your audio file.

The program will:

Convert speech from the audio file to text.
Analyze the sentiment of the transcribed text.
Print the transcription and sentiment results (score, magnitude, label).
Example Output

Enter the path to your audio file (e.g. test.wav): test.wav
Transcribed text: I feel so sad
Sentiment score: -0.9, magnitude: 0.9, sentiment: sad
Important Notes

You must create your own Google Cloud project and service account key.
The JSON key file contains sensitive credentials. Keep it secret and secure.
Make sure to install the required Python packages before running the script.
The audio file should be in a supported format (e.g., WAV with LINEAR16 encoding).
Sample rate in the script is set to 44100 Hz; modify if your audio file uses a different rate
