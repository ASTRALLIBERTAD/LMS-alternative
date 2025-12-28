---
id: "googleauth"
sidebar_position: 2
title: "GoogleAuth"
---

# 📦 GoogleAuth

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-20%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 34
:::

OAuth 2.0 authentication manager for Google Drive API.

Manages complete authentication lifecycle including credential storage,
automatic token refresh, and session persistence. Supports both desktop
OAuth flow (browser-based) and token bridging from external providers.

## Purpose

- Handle OAuth 2.0 authentication flows
        - Persist credentials across sessions
        - Automatically refresh expired tokens
        - Provide authenticated Drive API service

## Attributes

- **`creds`** (Credentials or None): OAuth credentials with access/refresh tokens. None when not authenticated.
- **`credentials_file`** (str): Path to OAuth client secrets JSON (web.json).
- **`token_file`** (str): Path to pickled credentials (token.pickle).
- **`client_id`** (str or None): OAuth client ID from credentials file.
- **`client_secret`** (str or None): OAuth client secret from credentials file.

## Algorithm

**Initialization Flow**:
    - 1. Set file paths for credentials and token storage
    - 2. Load client_id and client_secret from credentials JSON
    - 3. Restore existing session from token.pickle if available

  - **Desktop Authentication**:
    - 1. Launch local server on port 8550
    - 2. Open browser for user consent
    - 3. Receive authorization code via callback
    - 4. Exchange code for tokens
    - 5. Persist credentials to token.pickle

  - **Token-Based Authentication**:
    - 1. Validate incoming token structure
    - 2. Create Credentials object from token data
    - 3. Refresh if expired
    - 4. Save to token.pickle

## Example

```python
# Desktop authentication
auth = GoogleAuth('web.json')
auth.login_desktop()

# Token-based authentication
token_data = {
    'access_token': 'ya29...',
    'refresh_token': '1//0g...',
    'client_id': 'xxx.apps.googleusercontent.com',
    'client_secret': 'secret'
    }
auth.login_with_token(token_data)

# Use authenticated service
if auth.is_authenticated():
    service = auth.get_service()
    user = auth.get_user_info()
```

## See Also

- `DriveService`: Wraps GoogleAuth for Drive operations
- `ui.login.LoginView`: Desktop OAuth UI
- `login_desktop()`: Browser-based authentication
- `login_with_token()`: External token integration

## Notes

- Credentials stored in token.pickle (binary format)
- Tokens auto-refresh when expired
- Desktop OAuth uses port 8550
- Add token.pickle to .gitignore

## Security Considerations

:::note
- Never commit web.json or token.pickle
        - Credentials file contains client_secret
        - Token file contains user access tokens
        - Use appropriate file permissions (chmod 600)
        - Refresh tokens have long lifetime
:::
