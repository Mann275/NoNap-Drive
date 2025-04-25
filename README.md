# NoNap Drive: Driver Drowsiness Detection System

This project uses real-time facial landmark detection to monitor a driver's alertness. It leverages Eye Aspect Ratio (EAR) and Mouth Aspect Ratio (MAR) to detect signs of sleepiness or yawning. If drowsiness or sleep is detected, an alarm is triggered—and optionally, an SMS alert is sent to a designated emergency contact.

## 🔧 Features

- Real-time face and eye tracking using `dlib` and `OpenCV`
- EAR and MAR based detection
- Audible buzzer alerts using `pygame`
- SMS alerts via Twilio (in `SMS_NoNap_Drive.py`)
- Modular scripts for development, alerting, and SMS notification

## 🧠 How it works

- **EAR (Eye Aspect Ratio):** Detects blinking and prolonged eye closure.
- **MAR (Mouth Aspect Ratio):** Detects frequent yawning.
- A threshold-based system triggers alerts or actions like:
  - Sounding a buzzer
  - Sending an SMS alert (in the advanced script)

## 📁 File Overview

| File Name             | Description |
|-----------------------|-------------|
| `EAR.py`              | Basic drowsiness detection using EAR and MAR |
| `Facical_Landmark.py` | Detects facial landmarks for tracking eye and mouth movements in real-time |
| `NoNap_Drive.py`      | Improved detection with adjusted thresholds |
| `SMS_NoNap_Drive.py`  | Includes Twilio SMS functionality for alerts |

## 🛠 Requirements

- Python 3.7+
- dlib
- OpenCV
- pygame
- imutils
- numpy
- Twilio (only for `SMS_NoNap_Drive.py`)

You can install all required packages via:
```bash
1 Setup Instrucions.md
