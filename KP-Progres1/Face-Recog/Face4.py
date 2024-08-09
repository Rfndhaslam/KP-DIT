import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime, timedelta
import os

script_dir = os.path.dirname(__file__)
photos_folder = os.path.join(script_dir, 'photos')

tuwi_image = face_recognition.load_image_file(os.path.join(photos_folder, "Tuwi.jpg"))
tuwi_encoding = face_recognition.face_encodings(tuwi_image)[0]

kevin_image = face_recognition.load_image_file(os.path.join(photos_folder, "Kevin.jpg"))
kevin_encoding = face_recognition.face_encodings(kevin_image)[0]

rafi_image = face_recognition.load_image_file(os.path.join(photos_folder, "Rafi.jpg"))
rafi_encoding = face_recognition.face_encodings(rafi_image)[0]

daanish_image = face_recognition.load_image_file(os.path.join(photos_folder, "Daanish.jpg"))
daanish_encoding = face_recognition.face_encodings(daanish_image)[0]

arkan_image = face_recognition.load_image_file(os.path.join(photos_folder, "Arkan.jpg"))
arkan_encoding = face_recognition.face_encodings(arkan_image)[0]

known_face_encodings = [
    tuwi_encoding,
    kevin_encoding,
    rafi_encoding,
    daanish_encoding,
    arkan_encoding
]
known_faces_info = {
    "tuwi": {"nip": "1103213054", "nama": "Triwardana Tegar"},
    "kevin": {"nip": "1103210066", "nama": "Kevin Olind"},
    "rafi": {"nip": "1103213080", "nama": "Rafindha Aslam"},
    "daanish": {"nip": "1103213014", "nama":"Daanish Abdul"},
    "arkan": {"nip": "1103213052", "nama":"Arkan Fayiz"},
}

karyawan = list(known_faces_info.keys())

video_capture = cv2.VideoCapture(0)

current_date = datetime.now().strftime("%Y-%m-%d")
csv_file_path = os.path.join(script_dir, f'{current_date}.csv')
csv_file = open(csv_file_path, 'w+', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["NIP", "Nama", "Pukul", "Hari", "Tanggal", "Tahun", "Status Kehadiran"])  # Header for the CSV file

attendance_deadline = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
end_of_day = attendance_deadline + timedelta(days=1)

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)  # Reduced scaling for better recognition
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    for i in range(3):
        rgb_small_frame[:, :, i] = cv2.equalizeHist(rgb_small_frame[:, :, i])

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    face_names = []

    for face_encoding in face_encodings:
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        nama = "Tidak Dikenali"

        if face_distances[best_match_index] < 0.5:  # Reduced threshold for better accuracy
            nama = list(known_faces_info.keys())[best_match_index]

            if nama in karyawan:
                karyawan.remove(nama)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                current_day = now.strftime("%A")
                current_date = now.strftime("%Y-%m-%d")
                current_year = now.strftime("%Y")
                nip = known_faces_info[nama]["nip"]
                full_nama = known_faces_info[nama]["nama"]

                if now <= attendance_deadline:
                    status = "Hadir"
                else:
                    status = "Telat"

                csv_writer.writerow([nip, full_nama, current_time, current_day, current_date, current_year, status])

        face_names.append(nama)

    for (top, right, bottom, left), nama in zip(face_locations, face_names):
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        if nama != "Tidak Dikenali":
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 70), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            nip = known_faces_info[nama]['nip']
            full_nama = known_faces_info[nama]['nama']
            cv2.putText(frame, nip, (left + 6, bottom - 45), font, 1.0, (255, 255, 255), 1)
            cv2.putText(frame, full_nama, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        else:
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, nama, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Sistem Presensi', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

now = datetime.now()
if now >= end_of_day:
    for kary in karyawan:
        nip = known_faces_info[kary]["nip"]
        full_nama = known_faces_info[kary]["nama"]
        csv_writer.writerow([nip, full_nama, "-", now.strftime("%A"), now.strftime("%Y-%m-%d"), now.strftime("%Y"), "Absen"])

csv_file.close()
video_capture.release()
cv2.destroyAllWindows()
