---
id: "login_desktop"
sidebar_position: 7
title: "login_desktop"
---

# ⚙️ login_desktop

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 350
:::

Perform desktop OAuth 2.0 authentication flow with browser.

Launches a local HTTP server on port 8550 and opens the system browser
to Google's OAuth consent screen. After user authorization, receives
the authorization code via callback and exchanges it for access and
refresh tokens. Saves credentials to pickle file for session persistence.

## Returns

**Type**: `None`

                - Opens system browser to OAuth consent screen
                - Starts local server on port 8550
                - Creates/updates token.pickle file

## Exceptions

FileNotFoundError: If credentials_file doesn't exist at specified path.
                Must have valid web.json with OAuth client configuration.

## Algorithm

- 1. **Verify Credentials File**:
    - a. Check if self.credentials_file exists
    - b. If not, raise FileNotFoundError with path

  - 2. **Import OAuth Flow**:
    - a. Import InstalledAppFlow from google_auth_oauthlib.flow
    - b. Lazy import (only when needed)

  - 3. **Start OAuth Flow**:
    - a. Print status message: "Starting desktop OAuth flow..."
    - b. Create flow: InstalledAppFlow.from_client_secrets_file()
    - i. Pass self.credentials_file (web.json path)
    - ii. Pass SCOPES (Drive API scope)
    - c. Flow configured with client credentials

  - 4. **Run Local Server**:
    - a. Call flow.run_local_server(port=8550)
    - b. Starts HTTP server on localhost:8550
    - c. Opens default browser to OAuth consent URL
    - d. User sees Google sign-in and consent screen
    - e. User authorizes application
    - f. Browser redirects to localhost:8550/oauth_callback
    - g. Server receives authorization code
    - h. Flow exchanges code for tokens
    - i. Returns Credentials object with tokens

  - 5. **Store Credentials**:
    - a. Assign returned credentials to self.creds
    - b. Contains access_token and refresh_token

  - 6. **Save to Pickle**:
    - a. Call self._save_credentials()
    - b. Persists session to token.pickle

  - 7. **Log Success**:
    - a. Print success message: "✓ Desktop login successful"

## Interactions

- **os.path.exists()**: Verifies credentials file
- **InstalledAppFlow.from_client_secrets_file()**: Creates OAuth flow
- **InstalledAppFlow.run_local_server()**: Runs auth server
- **_save_credentials()**: Persists credentials

## Example

```python
auth = GoogleAuth('path/to/web.json')
auth.login_desktop()
# Starting desktop OAuth flow...
# # Browser opens to Google OAuth consent screen
# # User signs in and authorizes
# # Browser shows success message
# ✓ Desktop login successful

# Check authentication
if auth.is_authenticated():
    print("Login successful!")
# Login successful!

# Get Drive service
service = auth.get_service()
```

## See Also

- `login_with_token()`: Alternative token-based authentication
- `is_authenticated()`: Validates authentication status
- `_save_credentials()`: Persists credentials
- `InstalledAppFlow <[https://google-auth-oauthlib.readthedocs.io/>`_](https://google-auth-oauthlib.readthedocs.io/>`_)

## Notes

- Port 8550 must be in authorized redirect URIs (Google Console)
- Browser must be available on system
- User must complete OAuth consent in browser
- Automatically saves credentials on success
- Refresh token provided for long-term access
- Local server stops after receiving callback
- May fail if port 8550 already in use
