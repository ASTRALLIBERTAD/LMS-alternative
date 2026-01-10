# Security Policy

## 🔒 Overview

LMS Alternative handles sensitive credentials and user data. This document outlines security best practices and policies for maintaining the security of the application and protecting user information.

---

## 🚨 Reporting Security Vulnerabilities

If you discover a security vulnerability, please report it responsibly:

1. **DO NOT** open a public GitHub issue
2. Email the maintainers directly at: [INSERT YOUR EMAIL]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

**Response Time**: We aim to respond to security reports within 48 hours.

---

## 🔐 Credential Security

### Critical Files to Protect

The following files contain sensitive credentials and **MUST NEVER** be committed to version control:

#### Google OAuth Credentials
- `src/services/credentials.json` - OAuth 2.0 client credentials
- `src/services/token.pickle` - User authentication tokens

#### Firebase Credentials
- `src/services/firebase-admin-credentials.json` - Firebase Admin SDK private key
- `src/services/firebase_config.json` - Firebase project configuration
- `src/services/web.json` - Firebase web push VAPID key

#### User Data
- `storage/accounts.json` - Multi-account user data
- `lms_data/` - All LMS data (assignments, students, submissions)
- `saved_links.json` - Saved Google Drive links
- `favorites.json` - User favorites
- `lms_config.json` - LMS configuration including Drive folder IDs

### .gitignore Configuration

Ensure your `.gitignore` file includes:

```gitignore
# Google OAuth
services/credentials.json
services/token.pickle
services/web.json

# Firebase
services/firebase_config.json
services/firebase-admin-credentials.json

# User Data
storage/
lms_data/
saved_links.json
favorites.json
lms_config.json
*.pickle

# Environment Variables
.env
.env.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/
```

---

## 🛡️ Security Best Practices

### 1. Google Cloud Platform Security

#### OAuth 2.0 Configuration

**OAuth Consent Screen:**
- Start with "External" for testing
- Limit test users to trusted individuals
- Move to "Internal" for production (organization only)
- Never publish to production with broad scopes unless necessary

**Client Secret Protection:**
```bash
# Verify credentials.json is in .gitignore
git check-ignore services/credentials.json
# Should output: services/credentials.json

# Check if accidentally staged
git status
# Credentials files should NOT appear here
```

**Scope Limitation:**
- Only request necessary scopes
- Current scope: `https://www.googleapis.com/auth/drive`
- Review and minimize scopes periodically

#### API Key Restrictions

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services** → **Credentials**
3. For each API key:
   - Set **Application restrictions** (HTTP referrers, IP addresses, or Apps)
   - Set **API restrictions** to only required APIs
   - Enable quotas and monitoring

### 2. Firebase Security

#### Admin SDK Protection

The `firebase-admin-credentials.json` file contains a private key that grants **full administrative access** to your Firebase project.

**Critical Rules:**
- ✅ Never commit to version control
- ✅ Never share in screenshots or logs
- ✅ Regenerate immediately if exposed
- ✅ Store securely with restricted permissions
- ✅ Use environment variables in production

**File Permissions:**
```bash
# Restrict file permissions (Linux/macOS)
chmod 600 src/services/firebase-admin-credentials.json
chmod 600 src/services/firebase_config.json
```

#### Firebase Security Rules

**Firestore/Realtime Database:**
```javascript
// Example secure rules for Firestore
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Require authentication
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
    
    // Student-specific data
    match /students/{studentId} {
      allow read: if request.auth.uid == studentId;
      allow write: if request.auth.uid == studentId && 
                     request.resource.data.keys().hasOnly(['name', 'submissions']);
    }
  }
}
```

**Cloud Storage:**
```javascript
// Example secure rules for Storage
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /submissions/{userId}/{fileName} {
      // Users can only upload their own submissions
      allow write: if request.auth != null && request.auth.uid == userId;
      // Teachers and students can read
      allow read: if request.auth != null;
    }
  }
}
```

#### FCM Token Security

- Store FCM tokens securely server-side
- Implement token refresh mechanism
- Never expose tokens in client logs
- Validate token ownership before sending notifications

### 3. Data Protection

#### Local Data Encryption

For sensitive local data storage:

```python
# Example using cryptography library
from cryptography.fernet import Fernet

# Generate key (store securely, never in code)
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt
encrypted_data = cipher.encrypt(b"sensitive data")

# Decrypt
decrypted_data = cipher.decrypt(encrypted_data)
```

#### Drive Storage Security

**Folder Permissions:**
- Set appropriate sharing permissions on LMS root folder
- Use "Specific people" access, not "Anyone with the link"
- Regularly audit folder access
- Remove access for former students/teachers

**File Validation:**
```python
ALLOWED_EXTENSIONS = {'.txt', '.jpg', '.png', 'base64 encoded files'}

def is_allowed_file(filename):
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS
```

### 4. Authentication Security

#### Token Management

**Best Practices:**
- Tokens stored in `token.pickle` are encrypted by Google's library
- Implement token refresh mechanism (already in code)
- Clear tokens on logout
- Never log token values

**Session Security:**
```python
# Validate token expiry
if self.creds.expired and self.creds.refresh_token:
    self.creds.refresh(Request())
    self._save_credentials()
```

#### Multi-Account Security

The multi-account manager stores credentials locally:

**Security measures:**
- Credentials encrypted by OS keyring (when available)
- Separate storage per account
- Token refresh on account switch
- Account removal clears all data

### 5. Input Validation

**Prevent Injection Attacks:**

```python
# Sanitize user input
import re

def sanitize_email(email: str) -> str:
    # Email validation pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValueError("Invalid email format")
    return email.lower().strip()

def sanitize_filename(filename: str) -> str:
    # Remove path traversal attempts
    return Path(filename).name

def validate_drive_id(drive_id: str) -> bool:
    # Drive IDs are alphanumeric with hyphens/underscores
    pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(pattern, drive_id))
```

### 6. Error Handling

**Secure Error Messages:**

```python
# DON'T: Expose sensitive information
try:
    service.authenticate(credentials)
except Exception as e:
    print(f"Auth failed: {credentials.client_secret}")  # ❌ BAD

# DO: Log safely
try:
    service.authenticate(credentials)
except Exception as e:
    logger.error(f"Authentication failed for user: {user_id}")  # ✅ GOOD
    # Send generic error to user
    show_snackbar(page, "Authentication failed. Please try again.", Colors.RED)
```

---

## 🔍 Security Auditing

### Regular Security Checks

**Monthly:**
- Review Firebase users and remove inactive accounts
- Check Google Cloud Platform quotas and usage
- Review Drive folder permissions
- Update dependencies: `pip list --outdated`

**Quarterly:**
- Rotate Firebase Admin SDK credentials
- Review and update OAuth scopes
- Audit application logs for suspicious activity
- Update Python and all dependencies

**Annually:**
- Security code review
- Penetration testing (if applicable)
- Update security documentation

### Dependency Security

**Check for vulnerabilities:**

```bash
# Install safety
pip install safety

# Check for known vulnerabilities
safety check

# Update dependencies
pip install --upgrade pip
pip install --upgrade -r requirements.txt
```

**Recommended `requirements.txt`:**

```txt
flet>=0.23.0
google-auth>=2.34.0
google-auth-oauthlib>=1.2.0
google-api-python-client>=2.147.0
firebase-admin>=6.5.0
plyer>=2.1.0
cryptography>=42.0.0  # For encryption
python-dotenv>=1.0.0  # For environment variables
```

---

## 🚀 Production Deployment Security

### Environment Variables

**Never hardcode credentials in production:**

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Access credentials from environment
FIREBASE_CREDENTIALS_PATH = os.getenv('FIREBASE_CREDENTIALS_PATH')
GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH')
```

**Example `.env` file (never commit):**

```env
# .env (add to .gitignore)
FIREBASE_CREDENTIALS_PATH=/secure/path/firebase-admin-credentials.json
GOOGLE_CREDENTIALS_PATH=/secure/path/credentials.json
FCM_SENDER_ID=your_sender_id
DATABASE_URL=https://your-project.firebaseio.com
```

### Server Deployment

**If deploying to a server:**

1. Use HTTPS only
2. Implement rate limiting
3. Set up logging and monitoring
4. Use firewall rules
5. Regular security patches
6. Backup encryption keys securely

### Mobile Deployment

**For Android/iOS builds:**

1. Enable ProGuard/R8 (Android)
2. Use code obfuscation
3. Implement certificate pinning
4. Store secrets in Android Keystore 
5. Use App Check for Firebase

---

## 📋 Security Checklist

Before deploying or sharing:

- [ ] All sensitive files in `.gitignore`
- [ ] No credentials in source code
- [ ] Firebase security rules configured
- [ ] Google Cloud API restrictions set
- [ ] OAuth consent screen configured
- [ ] Test users limited (if in testing mode)
- [ ] Dependencies up to date
- [ ] Error messages don't expose sensitive data
- [ ] Input validation implemented
- [ ] File upload restrictions in place
- [ ] Logging configured (no sensitive data logged)
- [ ] Backup strategy for credentials
- [ ] Incident response plan documented

---

## 📞 Contact

For security concerns or questions:

- **Email**: [INSERT YOUR EMAIL]
- **GitHub Issues**: For non-security bugs only
- **Response Time**: 48 hours for security issues

---

## 📚 Additional Resources

- [Google OAuth 2.0 Best Practices](https://developers.google.com/identity/protocols/oauth2/best-practices)
- [Firebase Security Documentation](https://firebase.google.com/docs/security)
- [OWASP Top Ten](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security.html)

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-10 | Initial security policy |

---

**Last Updated**: January 10, 2026

**⚠️ Remember**: Security is an ongoing process, not a one-time setup. Stay vigilant and keep your application and dependencies updated.