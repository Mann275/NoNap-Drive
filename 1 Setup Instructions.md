# Setup Instructions for NoNap-Drive Project

Follow these steps to set up the project on your machine:

## 1. Install Required Python Libraries

Use the following command to install all necessary libraries:

```
pip install numpy opencv-python dlib imutils pygame twilio
```
⚠️ Twilio is only needed for ```SMS_NoNap_Drive.py```. Use Python 3.7 or above.



## 2. Download Facial Landmark Predictor

You need the shape_predictor_68_face_landmarks.dat file to detect facial landmarks.

🔗 Download from here : ``` github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat ``` 

Place the file in the same folder as your .py scripts.

## 3. Important Notes

Make sure your ```webcam``` is connected.

```alarm.wav``` must be in the same directory for sound alerts.

Press ```ESC``` anytime to safely exit the program.

## 4. How to Run the Project
Use the following commands based on which file you want to run:

```python EAR.py```                # Basic EAR/MAR-based drowsiness detection with buzzer

```python Facical_Landmark.py```   # Shows facial landmark detection only (demo/debug)

```python NoNap_Drive.py```        # Improved logic with better EAR thresholding

```python SMS_NoNap_Drive.py```    # Drowsiness + yawning detection with Twilio SMS alerts

⚠️ Before running SMS_NoNap_Drive.py, replace the Twilio credentials (account_sid, auth_token, etc.) in the script with your own Twilio details.

