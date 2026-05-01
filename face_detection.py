import cv2
import os
from datetime import datetime
from twilio.rest import Client

# ─── Twilio Configuration ───────────────────────────────────────────────────
TWILIO_SID    = "YOUR_ACCOUNT_SID"       # Replace with your Twilio Account SID
TWILIO_TOKEN  = "YOUR_AUTH_TOKEN"        # Replace with your Twilio Auth Token
TWILIO_FROM   = "+1XXXXXXXXXX"           # Your Twilio phone number
TWILIO_TO     = "+91XXXXXXXXXX"          # Your phone number (receiver)

# ─── Known Faces Directory ───────────────────────────────────────────────────
KNOWN_FACES_DIR = "known_faces"          # Folder with images named Person.jpg
LOCATION        = "Lab - Chennai Institute of Technology"

# ─── Load Face Detector ─────────────────────────────────────────────────────
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# ─── Load Known Faces ────────────────────────────────────────────────────────
def load_known_faces():
    known = {}
    if not os.path.exists(KNOWN_FACES_DIR):
        os.makedirs(KNOWN_FACES_DIR)
        print(f"[INFO] Created '{KNOWN_FACES_DIR}' folder. Add face images named 'PersonName.jpg'.")
        return known
    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            name = os.path.splitext(filename)[0]
            img  = cv2.imread(os.path.join(KNOWN_FACES_DIR, filename), cv2.IMREAD_GRAYSCALE)
            if img is not None:
                known[name] = img
    print(f"[INFO] Loaded {len(known)} known face(s): {list(known.keys())}")
    return known

# ─── Send SMS Alert via Twilio ───────────────────────────────────────────────
def send_sms_alert(name, location, timestamp):
    try:
        client  = Client(TWILIO_SID, TWILIO_TOKEN)
        message = client.messages.create(
            body=(
                f"FACE DETECTION ALERT\n"
                f"Person   : {name}\n"
                f"Location : {location}\n"
                f"Time     : {timestamp}\n"
                f"Status   : Detected via surveillance camera"
            ),
            from_=TWILIO_FROM,
            to=TWILIO_TO
        )
        print(f"[SMS] Alert sent! SID: {message.sid}")
    except Exception as e:
        print(f"[ERROR] SMS failed: {e}")

# ─── Main Detection Loop ─────────────────────────────────────────────────────
def main():
    known_faces   = load_known_faces()
    cap           = cv2.VideoCapture(0)   # 0 = default webcam
    alerted_names = set()                 # Avoid duplicate alerts per session

    print("[INFO] Starting camera. Press 'Q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Cannot read from camera.")
            break

        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))

        for (x, y, w, h) in faces:
            face_roi  = gray[y:y+h, x:x+w]
            label     = "Unknown"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Simple template matching against known faces
            best_score = 0
            for name, known_img in known_faces.items():
                resized_known = cv2.resize(known_img, (w, h))
                result        = cv2.matchTemplate(face_roi, resized_known, cv2.TM_CCOEFF_NORMED)
                score         = result.max()
                if score > best_score and score > 0.35:
                    best_score = score
                    label      = name

            # Draw bounding box
            color = (0, 255, 0) if label != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, f"{label}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            cv2.putText(frame, timestamp, (x, y + h + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)

            # Send SMS only once per person per session
            if label != "Unknown" and label not in alerted_names:
                alerted_names.add(label)
                print(f"[ALERT] Detected: {label} at {timestamp}")
                send_sms_alert(label, LOCATION, timestamp)

        cv2.imshow("Face Detection - Press Q to Quit", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Camera released. Exiting.")

if __name__ == "__main__":
    main()
