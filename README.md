-------------------Face Recognition System--------------------

A complete Face Recognition System built using Python, OpenCV, FaceNet, SQLite, and Tkinter. 

It consists of:

Database Management (intialise_db.py) – Handles the user database. 

Face Registration (register_face.py) – Allows users to register their face in the database. 

Face Recognition (face_authentication.py) – Identifies registered users using a webcam. 

🚀 Features
✅ Face Registration – Users can register their faces by uploading an image.
✅ Face Recognition – Identifies registered users in real-time using a webcam.
✅ SQLite Database – Stores user details along with their facial embeddings.
✅ Tkinter GUI – Provides an easy-to-use interface for registering and recognizing faces.
✅ Futuristic Scanning Effect – A cool scanning animation during face recognition.


------------📂 Project Structure----------------------------
📂 Face-Recognition-System  
 ├── initialize_db.py         # Manages user database (SQLite)  
 ├── registerface.py     # GUI for face registration  
 ├── face_authentication.py    # GUI for real-time face recognition  
 ├── face_database.db    # SQLite database (auto-created)  
 ├── requirements.txt    # Required dependencies  
 ├── README.md           # Project documentation  


🔧 Installation
1️⃣ Clone the Repository
git clone https://github.com/your-repo/face-recognition-system.git
cd face-recognition-system


2️⃣ Create a Virtual Environment (Optional but Recommended)
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows


3️⃣ Install Dependencies
pip install -r requirements.txt


4️⃣ Run the Program
▶ Create the Database

---------------Run the script----------------------
Run the database setup script to create the users table:

python database.py
Select "Create Table" (Option 1) from the menu.

▶ Register a Face
Run the registration script to add a new user:

python registerface.py
Enter User ID & Name
Upload a clear image of the face
The system extracts the Face Embedding and stores it in the database
▶ Recognize a Face


Run the recognition script to identify a face using the webcam:

python face_authenction.py

The system captures an image from the webcam
It compares it against registered faces
If a match is found, access is granted ✅
If no match is found, access is denied ❌



----------------🛠 Technologies Used-------------
Python 3.x
OpenCV – Image processing
FaceNet (facenet-pytorch) – Face embedding extraction
MTCNN – Face detection
SQLite3 – Database
Tkinter – GUI


❗ Notes
Make sure you have a working webcam for real-time face recognition.
Ensure clear images for better recognition accuracy.
The FaceNet model is pre-trained on the VGGFace2 dataset.

🏆 Future Improvements
🚀 Multiple Face Recognition – Recognize multiple faces at once.
🚀 Mobile Integration – Extend support for mobile devices.
🚀 Cloud Database – Store face embeddings on the cloud for remote authentication.

📩 Contact
For any issues or suggestions, feel free to reach out!

👤 Prateek sharma

📧 prateeksharma9114@gmail.com


⭐ If you like this project, give it a star! 🚀✨





