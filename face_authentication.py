import cv2
import numpy as np
import torch
import sqlite3
import threading
from facenet_pytorch import MTCNN, InceptionResnetV1
from scipy.spatial.distance import cosine
import tkinter as tk
from tkinter import Label, Button, messagebox
import time

# Load Models
mtcnn = MTCNN(keep_all=False)  # No 'landmarks' argument
resnet = InceptionResnetV1(pretrained='vggface2').eval()

def extract_face_embedding(image):
    """Extract high-accuracy aligned face embeddings."""
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Get aligned face from MTCNN
    face = mtcnn(image_rgb)
    if face is None:
        return None

    face = face.unsqueeze(0)  # Add batch dimension
    with torch.no_grad():
        embedding = resnet(face)

    return embedding.numpy().flatten()


def fetch_registered_faces():
    """Fetch stored face embeddings from the database."""
    conn = sqlite3.connect("face_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, embedding FROM users")
    data = cursor.fetchall()
    conn.close()
    
    registered_faces = []
    for name, embedding in data:
        try:
            registered_faces.append((name, np.frombuffer(embedding, dtype=np.float32)))
        except Exception as e:
            print(f"Error loading embedding for {name}: {e}")
    
    return registered_faces

def recognize_face():
    """Capture an image with a scanning effect and compare it with registered faces."""
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # Set width
    cap.set(4, 480)  # Set height

    if not cap.isOpened():
        messagebox.showerror("Error", "Camera not accessible!")
        return

    scanning = True
    start_time = time.time()  # Start scanning timer
    scan_direction = 1  # 1 for moving down, -1 for moving up
    scan_pos = 0  # Initial position of scanning line

    while scanning:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture image!")
            cap.release()
            return

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes, probs, landmarks = mtcnn.detect(image_rgb, landmarks=True)

        if boxes is not None:
            for i, box in enumerate(boxes):
                x1, y1, x2, y2 = map(int, box)

                # Draw futuristic scanning frame
                frame_color = (0, 255, 0)  # Green color
                thickness = 3

                # Draw four corners for a futuristic effect
                cv2.line(frame, (x1, y1), (x1 + 30, y1), frame_color, thickness)
                cv2.line(frame, (x1, y1), (x1, y1 + 30), frame_color, thickness)

                cv2.line(frame, (x2, y1), (x2 - 30, y1), frame_color, thickness)
                cv2.line(frame, (x2, y1), (x2, y1 + 30), frame_color, thickness)

                cv2.line(frame, (x1, y2), (x1 + 30, y2), frame_color, thickness)
                cv2.line(frame, (x1, y2), (x1, y2 - 30), frame_color, thickness)

                cv2.line(frame, (x2, y2), (x2 - 30, y2), frame_color, thickness)
                cv2.line(frame, (x2, y2), (x2, y2 - 30), frame_color, thickness)

                # Moving scanning line inside the face box
                scan_pos += scan_direction * 5  # Move line up or down
                if scan_pos >= (y2 - y1) or scan_pos <= 0:
                    scan_direction *= -1  # Reverse direction

                scan_y = y1 + scan_pos  # Calculate the new Y position

                # Draw moving scanning line
                cv2.line(frame, (x1, scan_y), (x2, scan_y), (0, 255, 255), 2)  # Yellow scanning line

                # Display "Scanning..." text above the box
                cv2.putText(frame, "Scanning...", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Face Recognition", frame)

        if time.time() - start_time > 5:  # Auto-recognize after 5 seconds
            scanning = False
            break

        if cv2.waitKey(1) & 0xFF == ord("q"):
            scanning = False
            break

    cap.release()
    cv2.destroyAllWindows()

    # Proceed with face recognition
    embedding = extract_face_embedding(frame)
    if embedding is None:
        messagebox.showerror("Error", "No face detected!")
        return

    registered_faces = fetch_registered_faces()
    
    best_match = None
    best_score = 1.0  # Cosine similarity range is [0,2], lower is better
    
    for name, stored_embedding in registered_faces:
        similarity = cosine(embedding, stored_embedding)
        if similarity < best_score:
            best_match = name
            best_score = similarity

    if best_match and best_score < 0.35:  # Threshold for face match
        messagebox.showinfo("Access Granted", f"✅ Welcome, {best_match}!")
    else:
        messagebox.showerror("Access Denied", "❌ Face Not Recognized!")

def exit_app():
    """Closes the application."""
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("Face Recognition System")
root.geometry("400x350")
root.configure(bg="#1E1E1E")  # Dark theme background
root.resizable(False, False)

# App Title
title_label = Label(
    root, text="Face Recognition System", font=("Helvetica", 16, "bold"), fg="white", bg="#1E1E1E"
)
title_label.pack(pady=20)

# Recognize Button
def on_enter_rec(e):
    recognize_btn.config(bg="#FF9800", fg="black")  # Hover Effect

def on_leave_rec(e):
    recognize_btn.config(bg="#FFA726", fg="white")  # Original Color

recognize_btn = Button(
    root,
    text="Recognize Face",
    command=lambda: threading.Thread(target=recognize_face).start(),
    font=("Helvetica", 12, "bold"),
    bg="#FFA726",
    fg="white",
    relief="flat",
    activebackground="#FF9800",
    activeforeground="black",
    padx=20,
    pady=10
)
recognize_btn.pack(pady=10)
recognize_btn.bind("<Enter>", on_enter_rec)
recognize_btn.bind("<Leave>", on_leave_rec)

# Exit Button
exit_btn = Button(
    root,
    text="Exit",
    command=exit_app,
    font=("Helvetica", 12, "bold"),
    bg="#E53935",
    fg="white",
    relief="flat",
    activebackground="#D32F2F",
    activeforeground="black",
    padx=20,
    pady=10
)
exit_btn.pack(pady=10)

footer_label = Label(root, text="© 2025 FaceAuth Inc.", font=("Helvetica", 10), fg="gray", bg="#1E1E1E")
footer_label.pack(side="bottom", pady=10)

root.mainloop()
