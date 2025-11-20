import cv2
import numpy as np
import dlib
from imutils import face_utils
import threading
import pygame
import time
from twilio.rest import Client  # Import Twilio library

# Twilio credentials (Replace these with your Twilio credentials)
account_sid = 'YOUR_ACCOUNT_SID'
auth_token = 'YOUR_AUTH_TOKEN'
twilio_number = '+18305051963'
emergency_number = '+91XXXXXXXXXX'


# Initialize Twilio client
client = Client(account_sid, auth_token)

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
eyes_closed_start = None
yawn_count = 0  
yawn_threshold = 3  
mouth_open = False  
last_yawn_time = None  

# Function to calculate the Euclidean distance
def compute(ptA, ptB):
    return np.linalg.norm(ptA - ptB)

# Function to determine if the eye is blinked
def blinked(a, b, c, d, e, f):
    up = compute(b, d) + compute(c, e)
    down = compute(a, f)
    ratio = up / (2.0 * down)

    if ratio > 0.23:  
        return 2
    elif 0.19 < ratio <= 0.22:  
        return 1
    else:  
        return 0

# Function to compute Mouth Aspect Ratio (MAR) for yawning detection
def mouth_aspect_ratio(mouth):
    A = compute(mouth[2], mouth[10])
    B = compute(mouth[4], mouth[8])
    C = compute(mouth[0], mouth[6])
    return (A + B) / (2.0 * C)

# Function to send SMS using Twilio
def send_sms(message):
    try:
        client.messages.create(
            to=emergency_number,
            from_=twilio_number,
            body=message
        )
        print(f"SMS sent: {message}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")

# Function to play the buzzer sound
def play_buzzer():
    global buzzer_playing
    if not pygame.mixer.music.get_busy():  
        pygame.mixer.music.play()
        buzzer_playing = True

# Function to stop the buzzer sound
def stop_buzzer():
    global buzzer_playing
    if pygame.mixer.music.get_busy():  
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

    face_frame = frame.copy()

    for face in faces:
        x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
        cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)

        left_blink = blinked(landmarks[36], landmarks[37], landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_blink = blinked(landmarks[42], landmarks[43], landmarks[44], landmarks[47], landmarks[46], landmarks[45])

        mouth = landmarks[48:68]  
        mar = mouth_aspect_ratio(mouth)

        # Track blinking state
        if left_blink == 0 or right_blink == 0:
            if eyes_closed_start is None:
                eyes_closed_start = time.time()
            sleep += 1
            drowsy = 0
            active = 0

            if time.time() - eyes_closed_start > 3:
                status = "SLEEPING !!!"
                color = (255, 0, 0)
                threading.Thread(target=play_buzzer).start()
                send_sms("Driver is sleeping")  

        elif left_blink == 1 or right_blink == 1:
            sleep = 0
            active = 0
            drowsy += 1
            eyes_closed_start = None  
            status = "Drowsy !"
            color = (0, 0, 255)
            stop_buzzer()  

        else:
            sleep = 0
            drowsy = 0
            active += 1
            eyes_closed_start = None  
            status = "Active :)"
            color = (0, 255, 0)
            stop_buzzer()  

        # Check for yawning detection logic
        if mar > 0.8:  
            if not mouth_open:  
                mouth_open = True  
                last_yawn_time = time.time()
                status="yawnnnnnnnn"
        else:   
            if mouth_open:  
                if time.time() - last_yawn_time < 2:  
                    yawn_count += 1  
                    print(f"Yawn Count: {yawn_count}")

                    if yawn_count >= yawn_threshold:  
                        send_sms("Take a tea break")
                        yawn_count = 0  

                mouth_open = False  

        cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

        for n in range(0, 68):
            (x, y) = landmarks[n]
            cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)

    frame_resized = cv2.resize(frame, (640, 360))
    face_frame_resized = cv2.resize(face_frame, (640, 360))
    cv2.imshow("Frame", frame_resized)
    cv2.imshow("Result of detector", face_frame_resized)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
pygame.mixer.music.stop()
pygame.quit()
cv2.destroyAllWindows()
