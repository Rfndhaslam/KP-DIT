import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime, timedelta
import os
import tkinter as tk
from tkinter import simpledialog
from google.cloud import datastore

# Set environment variable for Service Account JSON key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:/vscode/KAPE/attedancesystemkp-8a32cc1e47e9.json"

# Initialize Datastore client
client = datastore.Client()

def get_known_faces():
    known_face_encodings = []
    known_faces_info = {}

    query = client.query(kind='faces')
    results = list(query.fetch())

    for entity in results:
        encoding = np.array(entity['encoding'])
        known_face_encodings.append(encoding)
        known_faces_info[entity.key.id_or_name] = {
            'nim': entity['nim'],
            'name': entity['name'],
            'encoding': entity['encoding']
        }
    
    return known_face_encodings, known_faces_info

def register_new_face(name, nim, face_encoding):
    # Add new face to Datastore
    key = client.key('faces')
    entity = datastore.Entity(key=key)
    entity.update({
        'name': name,
        'nim': nim,
        'encoding': face_encoding.tolist()
    })
    client.put(entity)
    print(f"Registered new face: {name} - {nim}")
    # Update known faces data
    known_face_encodings.append(face_encoding)
    known_faces_info[entity.key.id_or_name] = {
        'nim': nim,
        'name': name,
        'encoding': face_encoding
    }

# Get known faces from Datastore
known_face_encodings, known_faces_info = get_known_faces()

# Video capture setup
video_capture = cv2.VideoCapture(0)

# Generate CSV file path based on current time
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_file_path = os.path.join(os.path.dirname(__file__), f'{current_datetime}.csv')

# Open CSV file for writing attendance
csv_file = open(csv_file_path, 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["NIM", "Name", "Time", "Day", "Date", "Year", "Status"])  # Remove "Camera ID" from header

# Attendance deadline
attendance_deadline = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
end_of_day = attendance_deadline + timedelta(days=1)

# Variables for new face registration
register_face = False

def prompt_user_input():
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window

    name = simpledialog.askstring("Input", "Enter name:")
    nim = simpledialog.askstring("Input", "Enter NIM:")

    root.destroy()

    return name, nim

students = list(known_faces_info.keys())
recorded_faces = set()

while True:
    ret, frame = video_capture.read()
    if not ret:
        continue

    # Resize frame of video for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Histogram equalization for better face recognition
    for i in range(3):
        rgb_small_frame[:, :, i] = cv2.equalizeHist(rgb_small_frame[:, :, i])

    # Face recognition
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    face_names = []

    key = cv2.waitKey(1) & 0xFF
    if key == ord('r'):
        register_face = True

    if register_face:
        for face_encoding in face_encodings:
            new_face_name, new_face_nim = prompt_user_input()
            if new_face_name and new_face_nim:
                register_new_face(new_face_name, new_face_nim, face_encoding)
                print(f"Registration successful for {new_face_name} - {new_face_nim}")
                csv_writer.writerow([new_face_nim, new_face_name, "-", "-", "-", "-", "Registered"])
        register_face = False
    else:
        detected_faces = {}
        for face_encoding in face_encodings:
            # Face recognition using known encodings
            found = False
            for key_id, face_info in known_faces_info.items():
                stored_encoding = np.array(face_info['encoding'])
                face_distances = face_recognition.face_distance([stored_encoding], face_encoding)
                if face_distances[0] < 0.5:  # Adjust distance threshold as needed
                    nim = face_info['nim']
                    full_name = face_info['name']
                    if full_name not in detected_faces:
                        detected_faces[full_name] = nim
                    found = True
                    break
            
            if not found:
                face_names.append("Unknown")
            else:
                face_names.append(full_name)
    
    # Display the NIM and name on the screen for recognized faces only
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top = int(top / 0.75)
        right = int(right / 0.75)
        bottom = int(bottom / 0.75)
        left = int(left / 0.75)

        if name != "Unknown":
            nim = detected_faces[name]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 70), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, nim, (left + 6, bottom - 45), font, 1.0, (255, 255, 255), 1)
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        else:
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Record detected faces to CSV
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_day = now.strftime("%A")
    current_date = now.strftime("%Y-%m-%d")
    current_year = now.strftime("%Y")

    for full_name, nim in detected_faces.items():
        if full_name not in recorded_faces:
            recorded_faces.add(full_name)
            if now <= attendance_deadline:
                status = "Hadir"
            else:
                status = "Telat"
            csv_writer.writerow([nim, full_name, current_time, current_day, current_date, current_year, status])

    # Display the resulting image
    cv2.imshow('Attendance System', frame)

    # Exit condition
    if key == ord('q'):
        break

# Mark absent students
now = datetime.now()
if now >= end_of_day:
    for student in students:
        nim = known_faces_info[student]["nim"]
        full_name = known_faces_info[student]["name"]
        csv_writer.writerow([nim, full_name, "-", now.strftime("%A"), now.strftime("%Y-%m-%d"), now.strftime("%Y"), "Absen"])

# Clean up
csv_file.close()
video_capture.release()
cv2.destroyAllWindows()
