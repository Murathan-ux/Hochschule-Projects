import speech_recognition as sr
import os

# Initialize the recognizer
recognizer = sr.Recognizer()


# Function to transcribe audio from a file
def transcribe_audio_from_file(audio_file):
    try:
        # Load the audio file
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)

        # Recognize the speech using Google's speech recognition API
        text = recognizer.recognize_google(audio, language="de-DE")  # 'de-DE' for German
        print("Transcription: " + text)
    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from the speech recognition service; {e}")


# Function to listen and transcribe from the microphone
def listen_and_transcribe_from_microphone():
    with sr.Microphone() as source:
        print("Please speak something...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    try:
        # Recognize the speech using Google's speech recognition API
        text = recognizer.recognize_google(audio, language="de-DE")  # 'de-DE' for German
        print("Transcription: " + text)
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
    except sr.RequestError as e:
        print(f"Error with the recognition service: {e}")


# Main function to choose the mode (audio file or microphone)
def main():
    print("Choose the mode:")
    print("1. Transcribe from an audio file")
    print("2. Transcribe from the microphone")

    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        audio_file = input("Enter the path to your audio file (e.g., audio.wav): ")
        if os.path.exists(audio_file):
            transcribe_audio_from_file(audio_file)
        else:
            print("File not found. Please check the path.")
    elif choice == '2':
        listen_and_transcribe_from_microphone()
    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
