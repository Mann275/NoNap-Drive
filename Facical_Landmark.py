import cv2
import dlib
from imutils import face_utils

# Initialize the camera
cap = cv2.VideoCapture(0)

# Load the face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame. Exiting...")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    # Copy the frame to draw landmarks
    face_frame = frame.copy()

    for face in faces:
        x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
        cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Detect facial landmarks
        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)

        # Draw landmarks with numbers
        for i, (x, y) in enumerate(landmarks, start=1):
            cv2.circle(face_frame, (x, y), 2, (255, 255, 255), -1)  # Draw landmark
            cv2.putText(face_frame, str(i), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.4, (0, 255, 255), 1)  # Display landmark number

    # Show the frame with landmarks
    cv2.imshow("Facial Landmarks", face_frame)

    # Exit on pressing the ESC key
    if cv2.waitKey(1) == 27:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
