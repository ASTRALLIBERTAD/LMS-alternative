---
id: "_handle_mobile_login"
sidebar_position: 14
title: "_handle_mobile_login"
---

# ⚙️ _handle_mobile_login

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`login.py`](./login.py) | **Line:** 1152
:::

Execute mobile OAuth flow with external browser redirect.

Performs OAuth 2.0 authentication on mobile platforms by launching
the system browser with OAuth URL. Uses authorization code flow with
external redirect URL that must be handled by a callback server or
deep link handler.

## Returns

**Type**: `None`


## Algorithm

- **Phase 1: Import URL Encoding Module**:
  - 1. Import urllib.parse for URL parameter encoding
  - 2. Used to safely encode OAuth parameters

- **Phase 2: Update UI for Processing**:
  - 1. Call update_status() with progress message
  - 2. Message: "Opening browser..."
  - 3. Color: default (blue)
  - 4. disable_button: True (prevents double-click)

- **Phase 3: Try Browser Launch**:
  - 1. Enter try block for error handling

- **Phase 4: Build OAuth URL**:
  - 1. Set auth_url to Google OAuth endpoint:
    - "https://accounts.google.com/o/oauth2/v2/auth"
  - 2. Create params dictionary with OAuth parameters:
    - a. client_id: self.provider.client_id
    - (application identifier from Google Console)
    - b. redirect_uri: self.provider.redirect_url
    - (where Google sends user after auth)
    - c. response_type: 'code'
    - (authorization code flow, not implicit)
    - d. scope: ' '.join(self.provider.scopes)
    - (space-separated list of requested permissions)
    - e. access_type: 'offline'
    - (request refresh token for long-term access)
    - f. prompt: 'consent'
    - (force consent screen for consistent UX)
  - 3. URL-encode parameters: urllib.parse.urlencode(params)
  - 4. Build complete URL: f"&#123;auth_url&#125;?&#123;encoded_params&#125;"
  - 5. Store in oauth_url variable

- **Phase 5: Launch External Browser**:
  - 1. Call self.page.launch_url(oauth_url)
  - 2. Opens system browser to OAuth URL
  - 3. Non-blocking operation (returns immediately)
  - 4. User sees Google sign-in page in browser

- **Phase 6: Update UI with Instructions**:
  - 1. Call update_status() with instruction message
  - 2. Message: "Complete sign-in in browser, then return to app"
  - 3. Color: BLUE_600 (informational)
  - 4. disable_button: False (re-enable button)
  - 5. User can retry if browser doesn't open

- **Phase 7: Show Snackbar Notification**:
  - 1. Create SnackBar with content text
  - 2. Content: "Browser opening... Complete sign-in, then return here."
  - 3. Add action button: "OK"
  - 4. Assign to self.page.snack_bar
  - 5. Set snack_bar.open = True
  - 6. Call self.page.update() to display snackbar
  - 7. Provides additional visual feedback

- **Phase 8: Handle Exceptions**:
  - 1. Catch any Exception during browser launch
  - 2. Examples: URLError, OSError
  - 3. Call self.handle_error(ex, "Browser launch")
  - 4. Shows error message and re-enables button

## Interactions

- **urllib.parse.urlencode()**: Encodes OAuth parameters
- **update_status()**: Shows progress and instructions
- **ft.Page.launch_url()**: Opens external browser
- **ft.SnackBar**: Shows notification about browser
- **handle_error()**: Handles launch failures

## Example

```python
# Successful mobile login initiation
login._handle_mobile_login()
# Status: "Opening browser..." (blue, button disabled)
# Browser opens: accounts.google.com OAuth page
# Status: "Complete sign-in in browser..." (blue, button enabled)
# Snackbar: "Browser opening..."
# User completes OAuth in browser
# Browser redirects to external callback URL
# External handler processes token
# User manually returns to app

# Browser launch failure
login._handle_mobile_login()
# Status: "Opening browser..."
# Exception raised (no browser available)
# Status: "Browser launch failed: ..." (red, button enabled)
# User can retry
```

## See Also

- `handle_login()`: Routes to this for mobile platforms
- `FirebaseMobileLogin`:
- Alternative with polling
- `handle_error()`: Called on exceptions
- `urllib.parse`: URL encoding utilities

## Notes

- Uses authorization code flow (not implicit grant)
- Requires external callback URL handling
- Browser opens asynchronously (non-blocking)
- User must return to app manually after auth
- Redirect URL must be configured in Google Console
- Token exchange handled externally (not in app)
- No automatic token retrieval (unlike desktop flow)
- access_type='offline' requests refresh token
- prompt='consent' shows consent screen every time
- Snackbar provides additional user guidance
- Button re-enabled to allow retry if needed
