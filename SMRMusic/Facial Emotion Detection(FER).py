import cv2
import fer

# Custom mood mapping
emotion_map = {
    "happy": "1: happy",
    "sad": "2: sad",
    "angry": "5: angry",
    "disgust": "5: angry",
    "fear": "6: anxious",
    "surprise": "4: calm",
    "neutral": "7: neutral"
}

# Initialize detector
detector = fer.FER(mtcnn=True)

# Start video capture
cap = cv2.VideoCapture(0)
print("Detecting mood... (Press 'q' to quit early)")

detected_mood = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to access webcam.")
        break

    # Show live feed
    cv2.imshow("Mood Detection - Live", frame)

    # Detect emotions
    emotions = detector.detect_emotions(frame)
    if emotions:
        top_emotion = detector.top_emotion(frame)
        if top_emotion:
            emotion, score = top_emotion
            mood = emotion_map.get(emotion, "Unknown")

            # Draw box and label
            for face in emotions:
                (x, y, w, h) = face["box"]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"Mood: {mood}", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # Show final detection frame with annotation
            print(f"Mood Detected: {mood}")
            print(f"Playing music playlist for the mood: {mood}")
            cv2.imshow("Mood Detected", frame)
            cv2.waitKey(3000)  # Show for 3 seconds
            break

    # Quit manually with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exited without detecting mood.")
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
