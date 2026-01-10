# LMS Alternative
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flet](https://img.shields.io/badge/Flet-UI-green.svg)
![Google Drive API](https://img.shields.io/badge/Google%20Drive-API%20v3-yellow.svg)

## 📖 Description

**LMS Alternative** is a robust desktop application designed to streamline the academic workflow for students and educators. Built with [Flet](https://flet.dev/) (Python), it functions as a lightweight **Learning Management System (LMS)** that integrates seamless file management with essential academic tools.

By layering organizational features over **Google Drive**, this application provides a centralized dashboard where users can manage assignments, track deadlines, and organize course materials without the complexity of traditional LMS platforms. Whether you need to submit assignments, manage shared resources, or simply keep your digital workspace tidy, LMS Alternative offers a simple, efficient solution.

## 🎯 Purpose

This application serves as a **lightweight alternative to traditional Learning Management Systems (LMS)**, specifically designed to solve common student challenges:

- **📚 Centralized Assignment Management** – No more hunting through countless Google Drive links for different subjects and assignments
- **✅ To-Do List with Smart Notifications** – Track assignments with due dates and get timely reminders before and after deadlines
- **⏰ Time Tracking** – See remaining time for each assignment at a glance
- **🔗 Quick Link Access** – Organize and access all your course folders and assignment submission links in one place
- **📂 Subject-Based Organization** – Keep everything organized by subject/course for easy navigation

Perfect for students who need a simple, efficient way to manage their academic workload without the complexity of full-featured LMS platforms.

---

## ✨ Features

### 🎓 LMS Features
- **📋 Assignment To-Do List** – Create and manage assignments with due dates
- **🔔 Smart Notifications** – Get reminders before and after assignment due dates
- **⏱️ Time Remaining Tracker** – Visual countdown showing time left to complete tasks
- **📚 Subject Organization** – Organize assignments and folders by course/subject
- **🔗 Assignment Link Management** – Store and quickly access Google Drive submission folders for each assignment

### 📁 Google Drive Management
- **🔐 Google OAuth Authentication** – Secure login using your Google account
- **📁 Browse & Navigate** – Explore your Google Drive folders with an intuitive interface
- **🔍 Search** – Quickly find files and folders across your Drive
- **🔗 Paste Drive Links** – Open folders/files directly by pasting Google Drive links
- **📝 File Operations** – Create folders, upload files, rename, and delete
- **💾 Saved Links** – Keep a list of important Drive links for quick access
- **🔄 Caching** – Smart caching for improved performance and reduced API calls

---

## 📋 Prerequisites

- Python 3.8 or higher
- Google Cloud Platform project with Drive API enabled
- OAuth 2.0 credentials (`credentials.json`)
- Firebase project for notifications

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ASTRALLIBERTAD/LMS-alternative.git
cd LMS-alternative
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install flet google-auth google-auth-oauthlib google-api-python-client plyer firebase-admin
```

### 4. Set Up Google Cloud Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **Google Drive API**:
   - Navigate to **APIs & Services** → **Library**
   - Search for **Google Drive API** → **Enable**
4. Create OAuth 2.0 credentials:
   - Go to **APIs & Services** → **Credentials**
   - Click **Create Credentials** → **OAuth 2.0 Client ID**
   - Configure the OAuth consent screen if prompted
   - Select **Desktop App** as the application type
   - Download the JSON file
5. Save the file as `credentials.json` in the `services/` folder:
   ```
   src/services/credentials.json
   ```
6. Add test users:
   - Go to **APIs & Services** → **OAuth consent screen**
   - Add Gmail accounts that will test the app

### 5. Set Up Firebase for Notifications

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project
3. Generate Firebase Admin SDK credentials:
   - **Project Settings** → **Service Accounts** → **Generate New Private Key**
   - Save as `firebase-admin-credentials.json` in `services/` folder
4. Get Firebase configuration:
   - **Project Settings** → **General** → **Your Apps**
   - Copy the config and create `firebase_config.json` in `services/` folder:
   ```json
   {
     "apiKey": "YOUR_API_KEY",
     "authDomain": "your-project.firebaseapp.com",
     "projectId": "your-project-id",
     "storageBucket": "your-project.appspot.com",
     "messagingSenderId": "123456789",
     "appId": "1:123456789:web:abcdef123456",
     "measurementId": "G-XXXXXXXXXX"
   }
   ```
5. Generate web push key:
   - **Project Settings** → **Cloud Messaging** → **Web Push certificates**
   - Generate key pair and create `web.json` in `services/` folder:
   ```json
   {
     "vapidKey": "YOUR_VAPID_KEY_HERE"
   }
   ```

**Required files in `services/` folder:**
- `credentials.json` (Google OAuth)
- `firebase-admin-credentials.json` (Firebase Admin SDK)
- `firebase_config.json` (Firebase configuration)
- `web.json` (Firebase web push key)

**⚠️ Security:** Add these files to `.gitignore` to prevent committing sensitive credentials!

## 🎮 Usage

Run the application:

```bash
flet main.py
```

### First Launch

1. Click **"Login with Google"**
2. A browser window will open for Google authentication
3. Grant the requested permissions
4. You'll be redirected to the main dashboard

### Main Features

| Feature | Description |
|---------|-------------|
| **Your Folders** | Browse folders in your personal Drive |
| **Shared Drives** | Access shared/team drives |
| **Paste Links** | Open Drive links directly by pasting them |
| **Search** | Find files and folders by name |
| **New** | Create new folders or upload files |
| **Favorites** | Save folders organized by subject/category |

## 📁 Project Structure

```bash
capstone/
├── src/
│   ├── main.py              # Application entry point
│   ├── assets/
│   │   ├── icon_android.png
│   │   ├── icon.png
│   │   └── splash_android.png
│   ├── services/
│   │   ├── auth_service.py     # Google OAuth authentication
│   │   ├── credentials.json    # OAuth credentials (you provide)
│   │   ├── drive_service.py    # Google Drive API operations
│   │   ├── fcm_integration.py
│   │   ├── fcm_service.py
│   │   ├── file_preview_service.py
│   │   ├── firebase_config.json    # Firebase config (you provide)
│   │   ├── firebase-admin-credentials.json  # Firebase Admin SDK (you provide)
│   │   ├── notification_service.py
│   │   ├── token.pickle        # Auth token (auto-generated)
│   │   └── web.json            # Firebase web push key (you provide)
│   ├── ui/
│   │   ├── custom_control/     # Custom UI components
│   │   │   ├── __init__.py
│   │   │   ├── custom_controls.py
│   │   │   ├── gmail_profile_menu.py
│   │   │   └── multi_account_manager.py
│   │   ├── dashboard_modules/ 
│   │   │   ├── __init__.py
│   │   │   ├── file_manager.py
│   │   │   ├── folder_navigator.py
│   │   │   └── paste_links_manager.py
│   │   ├── todo_modules/
│   │   │   ├── __init__.py
│   │   │   ├── assignment_manager.py
│   │   │   ├── data_manager.py
│   │   │   ├── storage_manager.py
│   │   │   ├── student_manager.py
│   │   │   └── submission_manager.py
│   │   ├── __init__.py
│   │   ├── firebase_mobile_login.py
│   │   ├── login.py            # Login screen
│   │   ├── todo_view.py
│   │   └── dashboard.py        # Main dashboard UI
│   ├── utils/
│   │   └── common.py
├── README.md               # Project Overview
├── CONTRIBUTING.md         # Contribution Guidelines
├── saved_links.json        # Saved Drive links (auto-generated)
├── favorites.json          # Saved favorites (auto-generated)
└── venv/                   # Virtual environment
```

## 🔧 Configuration

The application stores configuration in the following files:

| File | Purpose |
|------|---------|
| `services/credentials.json` | Google OAuth credentials (required - you provide) |
| `services/firebase-admin-credentials.json` | Firebase Admin SDK (required - you provide) |
| `services/firebase_config.json` | Firebase configuration (required - you provide) |
| `services/web.json` | Firebase web push key (required - you provide) |
| `services/token.pickle` | Authentication token (auto-generated) |
| `saved_links.json` | Saved Drive links (auto-generated) |
| `favorites.json` | Favorite folders by category (auto-generated) |

## 🛡️ Security

- OAuth tokens are stored locally in `token.pickle`
- Credentials never leave your device
- Add the following to `.gitignore`:
  ```
  # Google OAuth
  services/credentials.json
  services/token.pickle
  
  # Firebase
  services/firebase_config.json
  services/firebase-admin-credentials.json
  services/web.json
  ```

## 📝 Supported Google Drive Link Formats

The app supports pasting links in these formats:

- `https://drive.google.com/drive/folders/FOLDER_ID`
- `https://drive.google.com/file/d/FILE_ID`
- `https://drive.google.com/...?id=ID`

## 🤝 Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:

- Setting up the development environment
- Configuring Google Cloud and Firebase
- Code style guidelines
- Submitting pull requests
- Reporting bugs and suggesting features

**Quick Start for Contributors:**

1. Fork the repository
2. Follow the setup instructions in [CONTRIBUTING.md](CONTRIBUTING.md)
3. Create a feature branch: `git checkout -b feature/amazing-feature`
4. Make your changes and commit: `git commit -m "feat: add amazing feature"`
5. Push to your fork: `git push origin feature/amazing-feature`
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. 
See [`LICENSE`](LICENSE.txt) for more information.

## 🙏 Acknowledgments

- [Flet](https://flet.dev/) – Cross-platform UI framework for Python
- [Google Drive API](https://developers.google.com/drive) – Cloud storage API
- [Firebase](https://firebase.google.com/) – Cloud messaging and notifications

## 📞 Support

- **Documentation**: Check [CONTRIBUTING.md](CONTRIBUTING.md) for detailed setup
- **Issues**: [GitHub Issues](https://github.com/ASTRALLIBERTAD/LMS-alternative/issues)
- **Questions**: Open an issue with the `question` label