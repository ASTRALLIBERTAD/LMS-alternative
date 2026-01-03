---
id: "login_desktop"
sidebar_position: 7
title: "login_desktop"
---

# ⚙️ login_desktop

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 360
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

- **Phase 1: Verify Credentials File**
  - 1. Check if self.credentials_file exists
  - 2. If not, raise FileNotFoundError with path


- **Phase 2: Import OAuth Flow**
  - 1. Import InstalledAppFlow from google_auth_oauthlib.flow
  - 2. Lazy import (only when needed)


- **Phase 3: Start OAuth Flow**
  - 1. Print status message: "Starting desktop OAuth flow..."
  - 2. Create flow: InstalledAppFlow.from_client_secrets_file()
  - 3. Pass self.credentials_file (web.json path)
    - a. Pass SCOPES (Drive API scope)
  - 4. Flow configured with client credentials


- **Phase 4: Run Local Server**
  - 1. Call flow.run_local_server(port=8550)
  - 2. Starts HTTP server on localhost:8550
  - 3. Opens default browser to OAuth consent URL
  - 4. User sees Google sign-in and consent screen
  - 5. User authorizes application
  - 6. Browser redirects to localhost:8550/oauth_callback
  - 7. Server receives authorization code
  - 8. Flow exchanges code for tokens
  - 9. Returns Credentials object with tokens

- **Phase 5: Store Credentials**
  - 1. Assign returned credentials to self.creds
  - 2. Contains access_token and refresh_token

- **Phase 6: Save to Pickle**
  - 1. Call self._save_credentials()
  - 2. Persists session to token.pickle

- **Phase 7: Log Success**
  - 1. Print success message: "✓ Desktop login successful"

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
