import cv2
import numpy as np
import torch
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image, ImageTk
import os

# Initialize models
mtcnn = MTCNN(keep_all=False)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

def extract_face_embedding(image):
    """Extract high-accuracy aligned face embeddings."""
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # MTCNN returns aligned 160×160 face
    face = mtcnn(image_rgb)
    if face is None:
        return None

    face = face.unsqueeze(0)  # Add batch dimension
    with torch.no_grad():
        embedding = resnet(face)

    return embedding.numpy().tobytes()


def save_to_database(user_id, name, embedding):
    """Saves the extracted embedding into the database."""
    conn = sqlite3.connect("face_database.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO users (user_id, name, embedding) VALUES (?, ?, ?)", 
                   (user_id, name, embedding))
    
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", f"✅ User {name} registered successfully!")

def upload_image():
    """Allows the user to select an image and process it for face registration."""
    user_id = user_id_entry.get()
    name = name_entry.get()
    
    if not user_id or not name:
        messagebox.showerror("Error", "Please enter User ID and Name.")
        return

    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")]
    )
    
    if not file_path:
        messagebox.showerror("Error", "No file selected.")
        return
    
    # Read the selected image
    image = cv2.imread(file_path)

    # ---- NEW FEATURE: SAVE IMAGE IN FOLDER ----
    folder_name = f"{user_id}-{name}".replace(" ", "_")  # avoid spaces
    save_dir = os.path.join("images", folder_name)
    os.makedirs(save_dir, exist_ok=True)

    save_path = os.path.join(save_dir, "original.jpg")
    cv2.imwrite(save_path, image)

    # ------------------------------------------

    embedding = extract_face_embedding(image)
    
    if embedding is None:
        messagebox.showerror("Error", "No face detected in the selected image.")
    else:
        save_to_database(user_id, name, embedding)
        messagebox.showinfo("Saved", f"Image saved at: {save_path}")


def exit_app():
    """Closes the application."""
    root.destroy()

# UI Setup
root = tk.Tk()
root.title("Face Registration")
root.geometry("500x400")
root.configure(bg="#2C2F33")

frame = tk.Frame(root, bg="#23272A")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

title_label = tk.Label(frame, text="Register Face", font=("Arial", 18, "bold"), fg="white", bg="#23272A")
title_label.pack(pady=10)

user_id_entry = tk.Entry(frame, font=("Arial", 14), width=20)
user_id_entry.pack(pady=5)
user_id_entry.insert(0, "Enter User ID")

name_entry = tk.Entry(frame, font=("Arial", 14), width=20)
name_entry.pack(pady=5)
name_entry.insert(0, "Enter Name")

upload_btn = tk.Button(frame, text="Upload Image", font=("Arial", 14, "bold"), bg="#7289DA", fg="white", command=upload_image)
upload_btn.pack(pady=10)

exit_btn = tk.Button(frame, text="Exit", font=("Arial", 14, "bold"), bg="#D9534F", fg="white", command=exit_app)
exit_btn.pack(pady=10)

root.mainloop()
