# Enterprise File Upload Center

A lightweight, Flask-based web application for managing corporate file uploads with a desktop-like interface. This project provides a simple, secure way for users to upload, download, and manage files within isolated user directories.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Security Considerations](#security-considerations)
- [Project Structure](#project-structure)

## 📖 Overview
The **Enterprise File Upload Center** is designed for internal use cases where a simple, self-hosted file sharing solution is required. It isolates user data by creating a unique folder for each username upon login. Users have full control (upload, rename, delete) over their own folders, while other users can only view and download files.

## ✨ Features
- **User Isolation:** Automatic creation of user-specific directories.
- **Desktop-Like UI:** A familiar interface with icons and windows for easy navigation.
- **Access Control:**
  - Users can only modify files in their own directory.
  - Download links are public (accessible to anyone with the URL).
- **File Operations:**
  - Upload files.
  - Download files.
  - Rename files (owner only).
  - Delete files (owner only).
- **Session Persistence:** Uses `localStorage` to remember the logged-in user.

## 🏗️ Architecture
The application follows a simple Client-Server architecture:
- **Backend (Flask):** Handles API requests, file system operations, and access control logic.
- **Frontend (HTML/JS):** Renders the desktop-like UI and communicates with the backend via RESTful API calls.
- **Storage:** Uses the local file system (`uploads/` directory) to store user data.

## 🛠️ Prerequisites
- Python 3.6+
- `pip` (Python package manager)

## 📥 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Install dependencies:**
   ```bash
   pip install flask
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the application:**
   Open your browser and navigate to `http://localhost:5151`.

## 🚀 Usage

1. **Login:**
   - Enter your desired username in the login box.
   - Click "Login/Create Folder". A folder will be created for you if it doesn't exist.

2. **Desktop View:**
   - You will see a list of all user folders.
   - Double-click a folder to open it.

3. **File Management:**
   - **Upload:** If you are the owner of the folder (username matches folder name), you can upload files using the toolbar.
   - **Download:** Double-click any file to download it.
   - **Rename/Delete:** These options are only visible for files in your own folder.

## 📡 API Documentation

The backend exposes the following RESTful endpoints:

| Method | Endpoint | Description | Headers Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/login` | Authenticates user and creates directory | `Content-Type: application/json` |
| `GET` | `/api/folders` | Lists all user directories | - |
| `GET` | `/api/files/<folder>` | Lists files in a specific folder | - |
| `POST` | `/api/upload/<folder>` | Uploads a file to a folder | `X-Username`, `multipart/form-data` |
| `DELETE` | `/api/delete/<folder>/<filename>` | Deletes a file | `X-Username` |
| `PUT` | `/api/rename/<folder>` | Renames a file | `X-Username`, `Content-Type: application/json` |
| `GET` | `/download/<folder>/<filename>` | Downloads a file | - |

### Example: Upload File
```bash
curl -X POST http://localhost:5151/api/upload/Ali \
  -H "X-Username: Ali" \
  -F "file=@/path/to/document.pdf"
```

## 🔒 Security Considerations
- **Path Traversal Protection:** The backend sanitizes filenames by removing `/` and `\` characters to prevent directory traversal attacks.
- **Access Control:** The `X-Username` header is checked on write operations (upload, delete, rename) to ensure users can only modify their own files.
- **Note:** This application is designed for **internal networks**. It is not hardened for public internet exposure. For production use, consider adding HTTPS, rate limiting, and more robust authentication.

## 📂 Project Structure
```
.
├── app.py          # Flask backend application
├── index.html      # Frontend UI and client-side logic
├── uploads/        # Directory for storing user files (created automatically)
└── README.md       # This file
```

## 🧪 Development
To run the application in debug mode (enabled by default in `app.py`):
```bash
python app.py
```
The server will start on `0.0.0.0:5151`, making it accessible from other devices on the local network.

## 📄 License
This project is provided as-is for educational and internal use purposes.
