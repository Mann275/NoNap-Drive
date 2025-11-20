# NoNap-Drive 🚗💤
## Driver Drowsiness Detection System

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-green.svg)](https://opencv.org)

A real-time computer vision system that detects driver drowsiness and fatigue to prevent road accidents. The system monitors facial features and provides immediate alerts through sound and SMS notifications when signs of drowsiness are detected.

---

## 📋 Table of Contents

- [About The Project](#about-the-project)
- [Problem Statement](#problem-statement)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Advantages](#advantages)
- [Limitations](#limitations)
- [Applications](#applications)
- [Contributing](#contributing)

---

## 🎯 About The Project

Driver drowsiness and fatigue significantly contribute to road accidents and fatalities worldwide. This system uses advanced OpenCV algorithms to detect drowsiness through visual cues like eye closure and yawning. By analyzing facial features and gestures in real-time, it aims to enhance transportation safety and reduce accidents caused by driver fatigue.

### Problem Statement

One of the most common causes of road accidents is driver drowsiness and fatigue. Each year, thousands of people lose their lives in such preventable accidents around the world. This system addresses this critical issue by providing real-time monitoring and alert mechanisms.

---

## 🚀 Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/Mann275/NoNap-Drive.git
cd NoNap-Drive
```

### Step 2: Install Required Python Libraries
```bash
pip install numpy opencv-python dlib imutils pygame twilio
```

### Step 3: Download Facial Landmark Predictor
1. Download `shape_predictor_68_face_landmarks.dat` from:
   ```
   https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat
   ```
2. Place the file in the same directory as your Python scripts

### Step 4: Setup Audio File
Ensure `alarm.wav` is present in the project directory for audio alerts.

### Step 5: Configure SMS (Optional)
For SMS functionality, update the Twilio credentials in `SMS_NoNap_Drive.py`:
- Replace `account_sid`, `auth_token`, and phone numbers with your Twilio details

---

## 🎮 Usage

### Running Different Modules

1. **Basic EAR Detection with Buzzer**:
   ```bash
   python EAR.py
   ```

2. **Facial Landmark Detection (Demo)**:
   ```bash
   python Facical_Landmark.py
   ```

3. **Enhanced Drowsiness Detection**:
   ```bash
   python NoNap_Drive.py
   ```

4. **Complete System with SMS Alerts**:
   ```bash
   python SMS_NoNap_Drive.py
   ```

### Controls
- **ESC Key**: Exit the program safely
- **Ensure**: Your webcam is connected and functioning
- **Position**: Sit facing the camera for optimal detection

---

## 📁 Project Structure

```
NoNap-Drive/
├── EAR.py                     # Basic EAR-based detection
├── Facical_Landmark.py        # Facial landmark visualization
├── NoNap_Drive.py            # Enhanced detection logic
├── SMS_NoNap_Drive.py        # Complete system with SMS
├── alarm.wav                 # Audio alert file
├── README.md                 # Project documentation
├── 1 Setup Instructions.md   # Detailed setup guide
├── Code Explaination.txt     # Technical documentation
└── Readme.txt               # Additional notes
```

---

## 🔧 How It Works

1. **Face Detection**: The system uses OpenCV to detect faces in real-time video feed
2. **Landmark Detection**: 68 facial landmarks are identified using dlib's predictor
3. **Eye Aspect Ratio (EAR)**: Calculates the ratio between eye height and width
4. **Mouth Aspect Ratio (MAR)**: Monitors mouth opening for yawn detection
5. **Threshold Analysis**: Compares EAR/MAR values against predefined thresholds
6. **Alert System**: Triggers audio, visual, and SMS alerts when drowsiness is detected
7. **Logging**: Records all detection events for analysis

---

## ⭐ Advantages

- **Fast Detection**: Quickly identifies signs of drowsiness in real-time
- **Accurate Differentiation**: Distinguishes between normal blinks and drowsy behavior
- **Low-light Performance**: Functions effectively in various lighting conditions
- **Spectacle Compatibility**: Works even when the driver is wearing glasses
- **Multi-modal Alerts**: Provides audio, visual, and SMS notifications
- **User-friendly Interface**: Simple and intuitive operation

---

## ⚠️ Limitations

- **Fixed Blink Duration**: Assumes standard blink patterns, though individual variations exist
- **2D Analysis**: EAR calculations use 2D data, limiting out-of-plane head rotation detection
- **Eye-dependent**: Primarily relies on eye monitoring, may miss other drowsiness indicators
- **Lighting Sensitivity**: Performance may vary in extreme lighting conditions
- **Camera Dependency**: Requires functional camera with clear view of the driver's face

---

## 🌟 Applications

- **Transportation Safety**: Reduces accidents caused by driver fatigue
- **Fleet Management**: Monitor commercial vehicle drivers
- **Personal Use**: Individual car safety enhancement
- **Research**: Study patterns in driver behavior and fatigue
- **Emergency Services**: Critical for long-haul emergency vehicle operators

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📞 Support

If you encounter any issues or have questions:
- Create an issue in the GitHub repository
- Check the `1 Setup Instructions.md` for detailed setup guidance
- Review `Code Explaination.txt` for technical details

---

**⚠️ Safety Notice**: This system is designed to assist drivers but should not replace responsible driving practices. Always ensure you are well-rested before driving and take breaks during long journeys.

---

Made with ❤️ for safer roads
