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
    dist = np.linalg.norm(ptA - ptB)
    return dist

# Function to determine if the eye is blinked
def blinked(a, b, c, d, e, f):
    up = compute(b, d) + compute(c, e)
    down = compute(a, f)
    ratio = up / (2.0 * down)

    # Adjusted EAR thresholds
    if ratio > 0.23:  # Eyes are open
        return 2
    elif 0.19 < ratio <= 0.22:  # Eyes are partially closed
        return 1
    else:  # Eyes are fully closed
        return 0

# Function to compute Mouth Aspect Ratio (MAR) for yawning detection
def mouth_aspect_ratio(mouth):
    A = compute(mouth[2], mouth[10])
    B = compute(mouth[4], mouth[8])
    C = compute(mouth[0], mouth[6])
    mar = (A + B) / (2.0 * C)
    return mar

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

        # Check eye status
        left_blink = blinked(landmarks[36], landmarks[37],
                             landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_blink = blinked(landmarks[42], landmarks[43],
                              landmarks[44], landmarks[47], landmarks[46], landmarks[45])

        # Check mouth for yawning (MAR)
        mouth = landmarks[48:68]  # Mouth landmarks
        mar = mouth_aspect_ratio(mouth)

        # Update states based on eye blinks
        if left_blink == 0 or right_blink == 0:
            if eyes_closed_start is None:
                eyes_closed_start = time.time()  # Record the time eyes were closed
            sleep += 1
            drowsy = 0
            active = 0

            # Check if eyes have been closed for more than 3 seconds
            if time.time() - eyes_closed_start > 3:
                status = "SLEEPING !!!"
                color = (255, 0, 0)
                threading.Thread(target=play_buzzer).start()  # Start buzzer in a separate thread

        elif left_blink == 1 or right_blink == 1:
            sleep = 0
            active = 0
            drowsy += 1
            eyes_closed_start = None  # Reset the timer as eyes are no longer closed
            status = "Drowsy !"
            color = (0, 0, 255)
            stop_buzzer()  # Stop the buzzer if eyes are open

        else:
            sleep = 0
            drowsy = 0
            active += 1
            eyes_closed_start = None  # Reset the timer as eyes are no longer closed
            status = "Active :)"
            color = (0, 255, 0)
            stop_buzzer()  # Stop the buzzer if eyes are open

        # Check for yawning
        if mar > 0.7:  # If the mouth aspect ratio indicates yawning
            yawning_detected = True
            status = "Yawning"
            color = (0, 255, 255)  # Yellow color for yawning
        else:
            yawning_detected = False

        # Display status on the frame
        cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

        # Display status on the right side of the frame
        # cv2.putText(frame, status, (frame.shape[1] - 250, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)


        # Draw facial landmarks
        for n in range(0, 68):
            (x, y) = landmarks[n]
            cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)

    frame_resized = cv2.resize(frame, (640, 360  ))
    face_frame_resized = cv2.resize(face_frame, (640, 360 ))
    # Show frames
    cv2.imshow("Frame", frame_resized)
    cv2.imshow("Result of detector", face_frame_resized)

    # Exit on pressing the ESC key
    key = cv2.waitKey(1)
    if key == 27:
        break

# Release resources and close windows
cap.release()
pygame.mixer.music.stop()
pygame.quit()
cv2.destroyAllWindows()