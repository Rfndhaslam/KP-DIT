import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime, timedelta
import os
import json
import tkinter as tk
from tkinter import simpledialog, Label
from PIL import Image, ImageTk
import mysql.connector

face_data_file = "D:/vscode/KAPE2/face_data.json"

# Database connection with error handling
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3307,
        ssl_disabled=True,
        database="sistempresensi"
    )
    cursor = db.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

def load_known_faces():
    if os.path.exists(face_data_file):
        with open(face_data_file, 'r') as file:
            data = json.load(file)
            for key, value in data.items():
                if 'name' not in value or 'nim' not in value or 'encoding' not in value:
                    print(f"Warning: Entry {key} is missing required keys. Skipping.")
                    continue
                value['encoding'] = np.array(value['encoding'])
            return data
    return {}

def save_known_faces(known_faces):
    with open(face_data_file, 'w') as file:
        data_to_save = {}
        for key, value in known_faces.items():
            data_to_save[key] = {
                'nim': value['nim'],
                'name': value['name'],
                'encoding': value['encoding'].tolist()
            }
        json.dump(data_to_save, file)

def register_new_face(name, nim, face_encoding):
    # Update known faces data
    known_faces_info[name] = {
        'nim': nim,
        'name': name,
        'encoding': face_encoding
    }
    save_known_faces(known_faces_info)
    print(f"Registered new face: {name} - {nim}")
    return nim, name

known_faces_info = load_known_faces()
known_face_encodings = [info['encoding'] for info in known_faces_info.values()]

video_capture = cv2.VideoCapture(0)

current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_file_path = os.path.join(os.path.dirname(__file__), f'{current_datetime}.csv')

csv_file = open(csv_file_path, 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["NIM", "Name", "Time", "Day", "Date", "Year", "Status"])

attendance_deadline = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
end_of_day = attendance_deadline + timedelta(days=1)

register_face = False

def prompt_user_input():
    root = tk.Tk()
    root.withdraw()

    name = simpledialog.askstring("Input", "Enter name:")
    nim = simpledialog.askstring("Input", "Enter NIM:")

    root.destroy()

    return name, nim

root = tk.Tk()
root.title("Attendance System")

title_label = Label(root, text="Attendance System", font=("Helvetica", 16))
title_label.grid(row=0, column=0, columnspan=2)

date_label = Label(root, text="", font=("Helvetica", 12))
date_label.grid(row=1, column=0, columnspan=2)

time_label = Label(root, text="", font=("Helvetica", 12))
time_label.grid(row=2, column=0, columnspan=2)

camera_label = Label(root)
camera_label.grid(row=3, column=0, padx=10, pady=10, sticky="nw")

info_frame = tk.Frame(root, bd=2, relief=tk.SOLID, height=240, width=320)
info_frame.grid(row=3, column=1, padx=10, pady=10, sticky="nw")
info_frame.grid_propagate(False)

label_width = 20

name_label = Label(info_frame, text="Name: ", font=("Helvetica", 12), bg="lightgrey", anchor='w', width=label_width)
name_label.grid(row=0, column=0, sticky="w", padx=10, pady=5, ipadx=5, ipady=5)

nim_label = Label(info_frame, text="NIM: ", font=("Helvetica", 12), bg="lightgrey", anchor='w', width=label_width)
nim_label.grid(row=1, column=0, sticky="w", padx=10, pady=5, ipadx=5, ipady=5)

status_label = Label(info_frame, text="Status: ", font=("Helvetica", 12), bg="lightgrey", anchor='w', width=label_width)
status_label.grid(row=2, column=0, sticky="w", padx=10, pady=5, ipadx=5, ipady=5)

def update_face_info(nim, name, status, known_face=True):
    name_label.config(text=f"Name: {name}")
    nim_label.config(text=f"NIM: {nim}")
    status_label.config(text=f"Status: {status}")

    if known_face:
        name_label.config(bg="lightgreen")
        nim_label.config(bg="lightgreen")
        status_label.config(bg="lightgreen")
    else:
        name_label.config(bg="lightgrey")
        nim_label.config(bg="lightgrey")
        status_label.config(bg="lightgrey")

def update_date_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%A, %Y-%m-%d")
    time_label.config(text=f"Time: {current_time}")
    date_label.config(text=f"Date: {current_date}")
    root.after(1000, update_date_time)

recorded_faces = set()

def insert_to_db(nim, name, time, day, date, year, status):
    try:
        query = "INSERT INTO presensi (nim, name, time, day, date, year, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (nim, name, time, day, date, year, status)
        cursor.execute(query, values)
        db.commit()
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")

def show_frame():
    global register_face

    ret, frame = video_capture.read()
    if not ret:
        return

    frame = cv2.resize(frame, (320, 240))

    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    face_names = []

    if register_face:
        for face_encoding in face_encodings:
            new_face_name, new_face_nim = prompt_user_input()
            if new_face_name and new_face_nim:
                if new_face_nim in known_faces_info:
                    print(f"NIM {new_face_nim} already exists. Skipping registration.")
                    continue
                nim, name = register_new_face(new_face_name, new_face_nim, face_encoding)
                print(f"Registration successful for {new_face_name} - {new_face_nim}")
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                current_day = now.strftime("%A")
                current_date = now.strftime("%Y-%m-%d")
                current_year = now.strftime("%Y")
                status = "Teregistrasi"
                recorded_faces.add(nim)
                csv_writer.writerow([nim, name, current_time, current_day, current_date, current_year, status])
                insert_to_db(nim, name, current_time, current_day, current_date, current_year, status)
            else:
                print("Registration canceled or invalid input.")
        register_face = False

    for face_encoding in face_encodings:
        if len(known_face_encodings) == 0:
            continue

        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        nim = "Unknown"
        status = ""

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                matched_face_info = list(known_faces_info.values())[best_match_index]
                name = matched_face_info['name']
                nim = matched_face_info['nim']
                status = "Dikenal"
                face_names.append(name)

                if nim not in recorded_faces:
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    current_day = now.strftime("%A")
                    current_date = now.strftime("%Y-%m-%d")
                    current_year = now.strftime("%Y")
                    recorded_faces.add(nim)
                    csv_writer.writerow([nim, name, current_time, current_day, current_date, current_year, status])
                    insert_to_db(nim, name, current_time, current_day, current_date, current_year, status)
            else:
                face_names.append("Unknown")
        else:
            face_names.append("Unknown")

        update_face_info(nim, name, status, known_face=name != "Unknown")

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top = int(top / 0.5)
        right = int(right / 0.5)
        bottom = int(bottom / 0.5)
        left = int(left / 0.5)

        color = (0, 0, 255)

        if name != "Unknown":
            if name in recorded_faces:
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)

        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)

        font_scale = max((right - left) // 160, 1)
        font_thickness = max((right - left) // 300, 1)
        font = cv2.FONT_HERSHEY_DUPLEX
        text_size = cv2.getTextSize(name, font, font_scale, font_thickness)[0]

        text_x = left + 6
        text_y = bottom - 6

        if text_x + text_size[0] > frame.shape[1]:
            text_x = frame.shape[1] - text_size[0] - 5
        if text_y - text_size[1] < 0:
            text_y = text_size[1] + 5

        cv2.putText(frame, name, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)

    outline_color = (0, 0, 128)
    frame_height, frame_width = frame.shape[:2]
    outline_thickness = 5
    cv2.rectangle(frame, (0, 0), (frame_width, frame_height), outline_color, outline_thickness)

    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)
    camera_label.imgtk = imgtk
    camera_label.config(image=imgtk)
    camera_label.after(10, show_frame)

def on_key_press(event):
    global register_face
    if event.char == 'r':
        register_face = True

root.bind("<Key>", on_key_press)

update_date_time()

show_frame()

root.mainloop()

video_capture.release()
csv_file.close()
db.close()
