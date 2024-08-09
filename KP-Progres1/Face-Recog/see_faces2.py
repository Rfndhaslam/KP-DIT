import json
import os

# File path for storing face encodings and information
face_data_file = "D:/vscode/KAPE2/face_data.json"

# Load known faces from local storage
def load_known_faces():
    if not os.path.exists(face_data_file):
        print(f"File {face_data_file} not found.")
        return {}

    with open(face_data_file, 'r') as file:
        try:
            data = json.load(file)
            for key, value in data.items():
                if 'name' not in value or 'nim' not in value or 'encoding' not in value:
                    print(f"Warning: Entry {key} is missing required keys. Skipping.")
                    continue
            return data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return {}

# Function to print known faces data
def print_known_faces(known_faces):
    print("\nKnown Faces:")
    for name, info in known_faces.items():
        print(f"Name: {info['name']}, NIM: {info['nim']}")

# Load known faces
known_faces_info = load_known_faces()

# Print known faces data
print_known_faces(known_faces_info)
