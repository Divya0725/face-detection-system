# Real-Time Face Detection & Notification System

A smart surveillance system that detects faces in real-time using **OpenCV** and sends instant **SMS alerts** via the **Twilio API** with the person's name, location, and timestamp.

---

## System Architecture

![System Diagram](images/system_diagram.png)

---

## Features

- Real-time face detection from webcam feed
- Matches detected faces against a known faces database
- Sends instant SMS alert with name, location & timestamp via Twilio
- Color-coded bounding boxes (Green = Known, Red = Unknown)
- Duplicate alert prevention per session

---

## Tech Stack

| Component | Technology |
|---|---|
| Face Detection | OpenCV (Haar Cascade) |
| SMS Alerts | Twilio API |
| Language | Python 3.x |
| Hardware | Webcam / Raspberry Pi / Jetson Nano |

---

## Project Structure

```
face-detection/
├── face_detection.py     # Main detection script
├── requirements.txt      # Python dependencies
├── known_faces/          # Add face images here (e.g. Divya.jpg)
└── images/               # Screenshots for README
```

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Divya0725/face-detection-notification.git
cd face-detection-notification
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add known faces
- Create a folder called `known_faces/`
- Add photos named after the person: `Divya.jpg`, `John.jpg` etc.

### 4. Configure Twilio
Open `face_detection.py` and replace:
```python
TWILIO_SID   = "YOUR_ACCOUNT_SID"
TWILIO_TOKEN = "YOUR_AUTH_TOKEN"
TWILIO_FROM  = "+1XXXXXXXXXX"
TWILIO_TO    = "+91XXXXXXXXXX"
```

### 5. Run the project
```bash
python face_detection.py
```

Press **Q** to quit the camera window.

---

## SMS Alert Example

```
FACE DETECTION ALERT
Person   : Divya M
Location : Lab - Chennai Institute of Technology
Time     : 2025-05-01 10:45:32
Status   : Detected via surveillance camera
```

---

## Demo

![Detection Screenshot](images/detection_demo.png)

---

## Use Cases

- Campus security monitoring
- Smart home surveillance
- IoT-based attendance systems
- Real-time intruder detection

---

## Author

**Divya M**  
B.E. Electronics & Communication (Advanced Communication Technology)  
Chennai Institute of Technology  
[GitHub](https://github.com/Divya0725) | [LinkedIn](https://linkedin.com/in/divya-m)

---

## Published Internship Project
Developed during internship at **GB Tech** (Nov–Dec 2024)
