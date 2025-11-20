import cv2
import numpy as np
import dlib
from imutils import face_utils
import threading
import pygame
import time

# Initialize the camera
cap = cv2.VideoCapture(0)

# Initialize pygame for sound
pygame.mixer.init()

# Load the buzzer sound
try:
    pygame.mixer.music.load("alarm.wav")
except Exception as e:
    print(f"Error loading alarm sound: {e}")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Load the face detector and landmark predictor
try:
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
except Exception as e:
    print(f"Error loading dlib models: {e}")
    print("Ensure 'shape_predictor_68_face_landmarks.dat' is in the same directory.")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Variables for tracking states
sleep = 0
drowsy = 0
active = 0
status = ""
color = (0, 0, 0)
buzzer_playing = False
eyes_closed_start = None  # Timestamp when eyes were first detected as closed
yawning_detected = False  # Variable to track yawning status

# Function to calculate the Euclidean distance
def compute(ptA, ptB):
    return np.linalg.norm(ptA - ptB)

# Function to determine if the eye is blinked
def blinked(a, b, c, d, e, f):
    up = compute(b, d) + compute(c, e)
    down = compute(a, f)
    return up / (2.0 * down)  # Return EAR directly

# Function to compute Mouth Aspect Ratio (MAR) for yawning detection
def mouth_aspect_ratio(mouth):
    A = compute(mouth[2], mouth[10])
    B = compute(mouth[4], mouth[8])
    C = compute(mouth[0], mouth[6])
    return (A + B) / (2.0 * C)

# Function to play the buzzer sound
def play_buzzer():
    global buzzer_playing
    if not pygame.mixer.music.get_busy():  # Play sound only if it's not already playing
        pygame.mixer.music.play()
        buzzer_playing = True

# Function to stop the buzzer sound
def stop_buzzer():
    global buzzer_playing
    if pygame.mixer.music.get_busy():  # Stop sound if it's playing
        pygame.mixer.music.stop()
        buzzer_playing = False

# Main loop for capturing frames
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame. Exiting...")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    # Initialize face_frame as a copy of the original frame
    face_frame = frame.copy()

    # Loop through detected faces
    for face in faces:
        x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
        cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Detect landmarks
        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)

        # Compute Eye Aspect Ratio (EAR)
        left_EAR = blinked(landmarks[36], landmarks[37], landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_EAR = blinked(landmarks[42], landmarks[43], landmarks[44], landmarks[47], landmarks[46], landmarks[45])

        # Compute Mouth Aspect Ratio (MAR) for yawning detection
        mouth = landmarks[48:68]
        mar = mouth_aspect_ratio(mouth)

        # Determine the eye state based on EAR
        if left_EAR < 0.19 or right_EAR < 0.19:  # Eyes closed
            if eyes_closed_start is None:
                eyes_closed_start = time.time()
            sleep += 1
            drowsy = 0
            active = 0

            if time.time() - eyes_closed_start > 3:
                status = "SLEEPING !!!"
                color = (255, 0, 0)
                threading.Thread(target=play_buzzer).start()

        elif 0.19 <= left_EAR < 0.23 or 0.19 <= right_EAR < 0.23:  # Drowsy
            sleep = 0
            active = 0
            drowsy += 1
            eyes_closed_start = None
            status = "Drowsy !"
            color = (0, 0, 255)
            stop_buzzer()

        else:  # Eyes open
            sleep = 0
            drowsy = 0
            active += 1
            eyes_closed_start = None
            status = "Active :)"
            color = (0, 255, 0)
            stop_buzzer()

        # Check for yawning
        if mar > 0.7:
            yawning_detected = True
            status = "Yawning"
            color = (0, 255, 255)  # Yellow for yawning
        else:
            yawning_detected = False

        # Display status and EAR values
        cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
        cv2.putText(face_frame, f"Left EAR: {left_EAR:.2f}", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)
        cv2.putText(face_frame, f"Right EAR: {right_EAR:.2f}", (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)

        # Draw facial landmarks
        for (x, y) in landmarks:
            cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)

    # Resize for better visualization
    frame_resized = cv2.resize(frame, (640, 360))
    face_frame_resized = cv2.resize(face_frame, (640, 360))

    # Show frames
    cv2.imshow("Frame", frame_resized)
    cv2.imshow("Result of detector", face_frame_resized)

    # Exit on pressing the ESC key
    if cv2.waitKey(1) == 27:
        break

# Release resources and close windows
cap.release()
pygame.mixer.music.stop()
pygame.quit()
cv2.destroyAllWindows()
