# Contributing to LMS Alternative

Thank you for your interest in contributing to LMS Alternative! We welcome contributions from the community and appreciate your efforts to improve this project.

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8+**
- **Git**
- **Google Cloud Platform account** (for Google Drive API)
- **Firebase account** (for notifications)

---

## 📋 Contribution Workflow

### 1. Fork the Repository
Click the **Fork** button at the top-right of this repository to create your own copy.

### 2. Clone Your Fork Locally

```bash
git clone https://github.com/<your-username>/LMS-alternative.git 
cd LMS-alternative
```

### 3. Set Up the Development Environment

#### 3.1 Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### 3.2 Install Dependencies

```bash
pip install flet google-auth google-auth-oauthlib google-api-python-client plyer firebase-admin
```

---

## 🔐 Setting Up Google Cloud Credentials

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Create Project** or select an existing project
3. Give your project a name (e.g., "LMS-Alternative-Dev")

### Step 2: Enable Google Drive API

1. In the left sidebar, navigate to **APIs & Services** → **Library**
2. Search for **Google Drive API**
3. Click on **Google Drive API** → **Enable**

### Step 3: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth 2.0 Client ID**
3. If prompted, configure the OAuth consent screen:
   - User Type: Select **External** for testing or **Internal** for organization-only use
   - Fill in:
     - **App Name**: LMS-alternative
     - **User Support Email**: Your email
     - **Developer Email**: Your email
   - Click **Save and Continue**
   - You can skip the **Scopes** section for basic setup
   - Click **Save and Continue**

4. Return to **Create OAuth 2.0 Client ID**:
   - Application Type: Select **Desktop App**
   - Name: e.g., "LMS-alternative-dev"
   - Click **Create**

5. After creation, click **Download JSON**
6. **Save the file as `credentials.json`** in the `services/` folder:
   ```
   src/services/credentials.json
   ```

### Step 4: Add Test Users

1. Go to **APIs & Services** → **OAuth consent screen**
2. Scroll to the **Test users** section
3. Click **Add users**
4. Enter the Gmail accounts that will test your OAuth app:
   - Add your own Gmail
   - Add additional test accounts if needed
5. Click **Save**

---

## 🔔 Setting Up Firebase for Notifications

The LMS Alternative uses Firebase Cloud Messaging (FCM) for push notifications. Follow these steps to set up Firebase:

### Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **Add Project**
3. Enter a project name (e.g., "LMS-Alternative-Notifications")
4. Follow the setup wizard:
   - (Optional) Enable Google Analytics if desired
   - Click **Create Project**

### Step 2: Register Your App

1. In the Firebase Console, click the **Settings** gear icon → **Project Settings**
2. Under **Your Apps**, click the platform icon you're developing for:
   - For desktop/cross-platform: Choose **Web** or **Android** (depending on your deployment target)
3. Register your app and download the configuration file

### Step 3: Generate Firebase Admin SDK Credentials

1. In the Firebase Console, go to **Project Settings** → **Service Accounts**
2. Click **Generate New Private Key**
3. Click **Generate Key** to download the JSON file
4. **Save the file as `firebase-admin-credentials.json`** in the `services/` folder:
   ```
   src/services/firebase-admin-credentials.json
   ```

### Step 4: Get Firebase Configuration

1. In **Project Settings** → **General**, scroll to **Your Apps**
2. Find your app and click on the **Config** option
3. Copy the Firebase configuration object
4. **Create `firebase_config.json`** in the `services/` folder with the following structure:

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

### Step 5: Create Web Credentials (for Web Push)

1. Go to **Project Settings** → **Cloud Messaging**
2. Scroll to **Web configuration** → **Web Push certificates**
3. Click **Generate key pair**
4. Copy the **Key pair** value
5. **Create `web.json`** in the `services/` folder:

```json
{
  "vapidKey": "YOUR_VAPID_KEY_HERE"
}
```

### Services Folder Structure

After completing the setup, your `services/` folder should contain:

```
src/services/
├── auth_service.py
├── credentials.json                    # Google OAuth credentials (YOU CREATE)
├── drive_service.py
├── fcm_integration.py
├── fcm_service.py
├── file_preview_service.py
├── firebase_config.json                # Firebase config (YOU CREATE)
├── firebase-admin-credentials.json     # Firebase Admin SDK (YOU CREATE)
├── notification_service.py
├── token.pickle                        # Auto-generated after first login
└── web.json                            # Firebase web push key (YOU CREATE)
```

### ⚠️ Security Notice

**IMPORTANT:** Never commit sensitive credentials to version control!

Add these files to your `.gitignore`:

```gitignore
# Google OAuth
services/credentials.json
services/token.pickle

# Firebase
services/firebase_config.json
services/firebase-admin-credentials.json
services/web.json
```

---

## 🌿 Branching Strategy

### Create a Feature Branch

```bash
git checkout -b feature/amazing-feature
```

### Branch Naming Conventions

- **Features**: `feature/description` (e.g., `feature/add-assignment-filter`)
- **Bug Fixes**: `fix/description` (e.g., `fix/notification-timing`)
- **Documentation**: `docs/description` (e.g., `docs/update-readme`)
- **Refactoring**: `refactor/description` (e.g., `refactor/cleanup-ui-code`)

---

## 💻 Making Changes

### Code Style Guidelines

- Follow **PEP 8** style guide for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and modular
- Use type hints where appropriate

### Example:

```python
def calculate_time_remaining(due_date: datetime) -> str:
    """
    Calculate time remaining until assignment due date.
    
    Args:
        due_date (datetime): The assignment due date
        
    Returns:
        str: Formatted time remaining string
    """
    # Implementation here
    pass
```

### Testing Your Changes

1. **Run the application** to ensure it works:
   ```bash
   flet main.py
   ```

2. **Test core functionality**:
   - Login with Google
   - Navigate folders
   - Create/edit assignments
   - Test notifications (if applicable)

3. **Check for errors** in the console output

---

## 📝 Commit Guidelines

### Commit Message Format

```
<type>: <subject>

<body (optional)>
```

### Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples:

```bash
git commit -m "feat: add assignment filter by subject"
git commit -m "fix: resolve notification timing issue"
git commit -m "docs: update Firebase setup instructions"
```

---

## 🚀 Submitting Your Contribution

### 1. Push to Your Branch

```bash
git push origin feature/amazing-feature
```

### 2. Create a Pull Request

1. Go to your fork on GitHub
2. Click **Compare & Pull Request**
3. Fill in the PR template:
   - **Title**: Brief description of changes
   - **Description**: Detailed explanation of what was changed and why
   - **Related Issues**: Link any related issues (e.g., "Closes #123")
   - **Screenshots**: If UI changes, include before/after screenshots

### 3. PR Review Process

- Maintainers will review your PR
- Address any requested changes
- Once approved, your PR will be merged!

---

## 🐛 Reporting Bugs

### Before Submitting a Bug Report

1. **Check existing issues** to avoid duplicates
2. **Update to the latest version** of the project
3. **Verify the bug** is reproducible

### Bug Report Template

```markdown
**Describe the Bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., Windows 11, macOS 13]
- Python Version: [e.g., 3.10]
- Flet Version: [e.g., 0.12.0]

**Additional Context**
Any other relevant information.
```

---

## 💡 Suggesting Enhancements

We love new ideas! To suggest an enhancement:

1. **Open an issue** with the label `enhancement`
2. **Describe the feature** clearly
3. **Explain the use case** and why it would be valuable
4. **Provide examples** if possible

---

## 📚 Resources

- [Flet Documentation](https://flet.dev/docs)
- [Google Drive API Documentation](https://developers.google.com/drive/api/guides/about-sdk)
- [Firebase Documentation](https://firebase.google.com/docs)
- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)

---

## 🤝 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior

- Be respectful and considerate
- Welcome newcomers and help them get started
- Accept constructive criticism gracefully
- Focus on what's best for the project and community

### Unacceptable Behavior

- Harassment or discrimination of any kind
- Trolling or inflammatory comments
- Publishing others' private information
- Other conduct that is inappropriate in a professional setting

---

## ❓ Questions?

If you have questions about contributing:

1. Check the [README.md](README.md) for basic project information
2. Search existing [GitHub Issues](https://github.com/ASTRALLIBERTAD/LMS-alternative/issues)
3. Open a new issue with the `question` label

---

## 🙏 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!

Happy coding! 🎉