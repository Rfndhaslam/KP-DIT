import face_recognition #Library untuk melakukan proses pengenalan dan identifikasi wajah dan menghasilkan encoding wajah
import cv2 # Library untuk mengakses kamera dan proses video stream
import numpy as np # Library untuk menangani array
import csv
from datetime import datetime, timedelta
import os
import tkinter as tk # untuk menghasilkan dan menampilkan GUI untuk interaksi dengan system
from tkinter import simpledialog, Label
from PIL import Image, ImageTk # untuk konversi gambar dari format opencv ke format yang dapat ditampilkan oleh tkinter
import firebase_admin # library untuk menghubungkan ke firebase dan mengakses realtime database
from firebase_admin import credentials, db
import dlib # library untuk memproses deteksi wajah dan mendapatkan training model 68 titik landmarks strukutr wajah berupa indeks

#Inisialisasi Detektor dan Prediktor training model untuk mendapatkan 68 Titik Landmarks struktur wajah
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("C:/Users/lenovo/AppData/Roaming/Python/Python310/site-packages/face_recognition_models/models/shape_predictor_68_face_landmarks.dat") 

#Inisialisasi koneksi ke Firebase menggunakan kredensial yang disimpan dalam file JSON dan menetapkan URL basis data Firebase.
base_dir = os.path.dirname(os.path.abspath(__file__))

#Mengakses Dir tempat menyimpan kredensial firebase dan inisialisasi aplikasi firebase untuk menghubungkan firebase dan dapat mengakses nya menggunakan kredensial dan database-url nya
cred_path = os.path.join(base_dir, "D:/vscode/KAPE2/sistempresensidit-firebase-adminsdk-okqli-e67a29dc70.json")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sistempresensidit-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# fungsi untuk mencatat presensi
def insert_attendance_to_firebase(nip, nama, time, day, date, year, status):
    ref = db.reference('data_presensi')
    date_ref = ref.child(date)
    time_ref = date_ref.child(time)
    time_ref.set({
        'nip': nip,
        'nama': nama,
        'day': day,
        'year': year,
        'status': status
    })

# fungsi menambahkan data wajah baru
def insert_to_firebase(nip, nama, encoding):
    ref = db.reference('data_wajah')
    ref.child(nip).set({
        'nip': nip,
        'nama': nama,
        'encoding_foto': encoding.tolist()
    })

# fungsi mengambil data wajah dari Firebase
def load_data_wajah():
    ref = db.reference('data_wajah')
    data = ref.get()
    data_wajah = {}
    if data:
        for nip, value in data.items():
            if 'encoding_foto' in value and 'nama' in value: 
                value['encoding_foto'] = np.array(value['encoding_foto'])
                data_wajah[nip] = value
    return data_wajah

# fungsi Menyimpan encoding wajah baru ke dalam info_data_wajah dan Firebase serta menampilkan pesan konfirmasi di terminal
def register_wajah_baru(nama, nip, encoding_wajah):
    info_data_wajah[nip] = {
        'nip': nip,
        'nama': nama,
        'encoding_foto': encoding_wajah
    }
    insert_to_firebase(nip, nama, encoding_wajah)
    print(f"Wajah baru yang teregistrasi: {nama} - {nip}")
    return nip, nama

# Membuka kamera menggunakan OpenCV dan mengatur resolusi video
info_data_wajah = load_data_wajah()
encodings_data_wajah = [info['encoding_foto'] for info in info_data_wajah.values()]

video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)  

# Membuat file CSV baru untuk menyimpan data kehadiran dengan nama file yang mencakup tanggal dan waktu saat ini.
datetime_terkini = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_file_path = os.path.join(os.path.dirname(__file__), f'Daftar_Presensi_{datetime_terkini}.csv')

csv_file = open(csv_file_path, 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["NIP", "Nama", "Waktu", "Hari", "Tanggal", "Tahun", "Status Kehadiran"])

deadline_presensi = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
hari_berakhir = deadline_presensi + timedelta(days=1)

register_wajah = False

# fungsi untuk Membuka jendela dialog untuk meminta input nama dan NIP dari pengguna ketika meregistrasi wajah baru.
def prompt_user_input():
    root = tk.Tk()
    root.withdraw()  

    nama = simpledialog.askstring("Input", "Masukkan Nama:")
    nip = simpledialog.askstring("Input", "Masukkan NIP:")

    root.destroy()

    return nama, nip

# Menginisialisasi jendela GUI menggunakan Tkinter untuk menampilkan informasi waktu, tanggal, dan status deteksi wajah.
root = tk.Tk()
root.title("Sistem Presensi Face Recognition DIT")

judul_label = Label(root, text="Sistem Presensi Berbasis Face Recognition", font=("Helvetica", 16))
judul_label.grid(row=0, column=0, columnspan=2)

tanggal_label = Label(root, text="", font=("Helvetica", 12))
tanggal_label.grid(row=1, column=0, columnspan=2)

waktu_label = Label(root, text="", font=("Helvetica", 12))
waktu_label.grid(row=2, column=0, columnspan=2)

kamera_label = Label(root)
kamera_label.grid(row=3, column=0, padx=10, pady=10, sticky="nw")

info_frame = tk.Frame(root, bd=2, relief=tk.SOLID, height=150, width=300)  
info_frame.grid(row=3, column=1, padx=10, pady=10, sticky="nw")
info_frame.grid_propagate(False)  

nama_label = Label(info_frame, text="Nama: ", font=("Helvetica", 12), bg="lightgrey", anchor="w", width=29)
nama_label.grid(row=0, column=0, sticky="w", padx=10, pady=5, ipadx=5, ipady=5)

nip_label = Label(info_frame, text="NIP: ", font=("Helvetica", 12), bg="lightgrey", anchor="w", width=29)
nip_label.grid(row=1, column=0, sticky="w", padx=10, pady=5, ipadx=5, ipady=5)

status_label = Label(info_frame, text="Status: ", font=("Helvetica", 12), bg="lightgrey", anchor="w", width=29)
status_label.grid(row=2, column=0, sticky="w", padx=10, pady=5, ipadx=5, ipady=5)

# fungsi untuk Memperbarui label GUI dengan informasi tentang nama, NIP, dan status deteksi wajah serta mengubah warna latar belakang berdasarkan status.
def info_update_wajah(nip, nama, status, data_wajah2 = True):
    nama_label.config(text=f"Nama: {nama}")
    nip_label.config(text=f"NIP: {nip}")
    status_label.config(text=f"Status: {status}")

    if data_wajah2:
        nama_label.config(bg="lightgreen")
        nip_label.config(bg="lightgreen")
        status_label.config(bg="lightgreen")
    elif nama == "Tak Dikenal":
        nama_label.config(bg="red")
        nip_label.config(bg="red")
        status_label.config(bg="red")
    else:
        nama_label.config(bg="lightgrey")
        nip_label.config(bg="lightgrey")
        status_label.config(bg="lightgrey")

# fungsi untuk Mengatur waktu dan tanggal saat ini pada GUI dan memperbaruinya setiap detik.
def update_date_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%A, %Y-%m-%d")
    waktu_label.config(text=f"Waktu: {current_time}")
    tanggal_label.config(text=f"Hari, Tanggal: {current_date}")
    root.after(1000, update_date_time)

# Fungsi detect_head_shake mendeteksi apakah pengguna menggelengkan kepala berdasarkan posisi relatif antara mata, hidung, dan rahang. Jika perbedaan posisi cukup besar, dianggap sebagai gerakan kepala.
recorded_wajah = set()

def detect_head_shake(landmarks):
    left_eye = landmarks[36:42]
    right_eye = landmarks[42:48]
    nose = landmarks[27:36]

    nose_x = [point[0] for point in nose]
    left_eye_x = [point[0] for point in left_eye]
    right_eye_x = [point[0] for point in right_eye]

    eye_center_x = (sum(left_eye_x) + sum(right_eye_x)) / 12
    nose_mean_x = sum(nose_x) / len(nose_x)

    head_shake_detected = abs(nose_mean_x - eye_center_x) > 5

    return head_shake_detected

# fungsi Membaca frame dari kamera, mendeteksi wajah, membandingkan encoding wajah yang terdeteksi dengan encoding yang sudah terdaftar, dan memperbarui informasi GUI.
def show_frame():
    global register_wajah

    ret, frame = video_capture.read()
    if not ret:
        return      

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detected_faces = detector(gray_frame)

    face_names = []
    face_statuses = []

    if register_wajah:
        for face in detected_faces:
            shape = predictor(gray_frame, face)
            landmarks = [(shape.part(i).x, shape.part(i).y) for i in range(68)]

            top, right, bottom, left = face.top(), face.right(), face.bottom(), face.left()
            encoding_wajah = face_recognition.face_encodings(frame, [(top, right, bottom, left)])[0]

            new_face_name, new_face_nim = prompt_user_input()
            if new_face_name and new_face_nim:
                nip, nama = register_wajah_baru(new_face_name, new_face_nim, encoding_wajah)
                print(f"Registration successful for {new_face_name} - {new_face_nim}")
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                current_day = now.strftime("%A")
                current_date = now.strftime("%Y-%m-%d")
                current_year = now.strftime("%Y")
                status = "Teregistrasi"
                csv_writer.writerow([new_face_nim, new_face_name, current_time, current_day, current_date, current_year, status])
        register_wajah = False
    else:
        for face in detected_faces:
            shape = predictor(gray_frame, face)
            landmarks = [(shape.part(i).x, shape.part(i).y) for i in range(68)]

            full_name = "Tak Dikenal"
            face_status = "Unrecognized"
            found = False

            top, right, bottom, left = face.top(), face.right(), face.bottom(), face.left()
            encoding_wajah = face_recognition.face_encodings(frame, [(top, right, bottom, left)])[0]

            for nip, face_info in info_data_wajah.items():
                stored_encoding = np.array(face_info['encoding_foto'])
                face_distances = face_recognition.face_distance([stored_encoding], encoding_wajah)
                if face_distances[0] < 0.4:
                    full_name = face_info['nama']
                    found = True
                    break

            if found and detect_head_shake(landmarks):  # Hanya catat jika sudah bergeleng
                face_status = "Recognized and Nodded"  
                if full_name not in recorded_wajah:
                    recorded_wajah.add(full_name)
                    now = datetime.now()
                    if now <= deadline_presensi:
                        status = "Hadir"
                    else:
                        status = "Telat"
                    info_update_wajah(nip, full_name, status)

                    current_time = now.strftime("%H:%M:%S")
                    current_day = now.strftime("%A")
                    current_date = now.strftime("%Y-%m-%d")
                    current_year = now.strftime("%Y")
                    csv_writer.writerow([nip, full_name, current_time, current_day, current_date, current_year, status])
                    insert_attendance_to_firebase(nip, full_name, current_time, current_day, current_date, current_year, status)
            elif found:
                face_status = "Recognized"  

            face_names.append(full_name)
            face_statuses.append(face_status)

    for face, nama, face_status in zip(detected_faces, face_names, face_statuses):
        left = face.left()
        top = face.top()
        right = face.right()
        bottom = face.bottom()

        if face_status == "Unrecognized":
            color = (0, 0, 255)  # Red for unrecognized
        elif face_status == "Recognized":
            color = (0, 255, 255)  # Yellow for recognized but not nodded
        elif face_status == "Recognized and Nodded":
            color = (0, 255, 0)  # Green for recognized and nodded

        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)

        font_thickness = max((right - left) // 300, 1)
        font = cv2.FONT_HERSHEY_DUPLEX
        text_size = cv2.getTextSize(nama, font, 0.3, font_thickness)[0]

        text_x = left + 6
        text_y = bottom - 6

        if text_x + text_size[0] > frame.shape[1]:
            text_x = frame.shape[1] - text_size[0] - 5
        if text_y - text_size[1] < 0:
            text_y = text_size[1] + 5

        cv2.putText(frame, nama, (left + 6, bottom - 6), font, 0.3, (255, 255, 255), font_thickness)

    outline_color = (0, 0, 128)
    frame_height, frame_width = frame.shape[:2]
    outline_thickness = 5
    cv2.rectangle(frame, (0, 0), (frame_width, frame_height), outline_color, outline_thickness)

    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)
    kamera_label.imgtk = imgtk
    kamera_label.config(image=imgtk)
    kamera_label.after(10, show_frame)

def on_key_press(event):
    global register_wajah
    if event.char == 'r':
        register_wajah = True

root.bind('<KeyPress>', on_key_press) 

# Memulai loop utama Tkinter untuk menjalankan antarmuka dan mengelola pembaruan waktu serta frame kamera.
update_date_time()
show_frame()
root.mainloop()

csv_file.close()
