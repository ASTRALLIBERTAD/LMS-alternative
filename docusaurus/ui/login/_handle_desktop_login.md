---
id: "_handle_desktop_login"
sidebar_position: 13
title: "_handle_desktop_login"
---

# ⚙️ _handle_desktop_login

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`login.py`](./login.py) | **Line:** 1041
:::

Execute desktop OAuth flow with local callback server.

Performs OAuth 2.0 authentication on desktop platforms using a
temporary local HTTP server to handle the OAuth callback. Opens
the system browser for user authentication and waits for the
callback with authorization code.

## Returns

**Type**: `None`


## Algorithm

- **Phase 1: Update UI for Processing**:
  - 1. Call update_status() with message
  - 2. Message: "Opening browser for authentication..."
  - 3. Color: default (blue)
  - 4. disable_button: True (prevents double-click)

- **Phase 2: Try Desktop Authentication**:
  - 1. Enter try block for error handling
  - 2. Call self.auth.login_desktop()
  - 3. Auth service performs:
    - a. Start local HTTP server on available port
    - b. Build OAuth URL with redirect to localhost
    - c. Open system browser to OAuth URL
    - d. Wait for user to authenticate
    - e. Receive callback with authorization code
    - f. Exchange code for access token
    - g. Store credentials in auth service
  - 4. login_desktop() method blocks until complete or timeout

- **Phase 3: Check Authentication Result**:
  - 1. Call self.auth.is_authenticated()
  - 2. Returns True if credentials valid and stored
  - 3. If True (authenticated):
    - a. Call self.handle_success()
    - b. Shows success message (green)
    - c. Invokes on_success callback
    - d. Typically navigates to dashboard
  - 4. If False (not authenticated):
    - a. Call update_status() with error message
    - b. Message: "Login completed but authentication failed"
    - c. Color: RED_600 (error indication)
    - d. disable_button: False (re-enable for retry)

- **Phase 4: Handle Exceptions**:
  - 1. Catch any Exception during authentication
  - 2. Examples: NetworkError, TimeoutError, ValueError
  - 3. Call self.handle_error(ex, "Desktop login")
  - 4. handle_error displays user message and logs details

## Interactions

- **update_status()**: Shows progress and results
- **GoogleAuth.login_desktop()**: Executes OAuth flow
- **GoogleAuth.is_authenticated()**: Validates credentials
- **handle_success()**: Handles successful authentication
- **handle_error()**: Handles authentication failures

## Example

```python
# Successful desktop login
login._handle_desktop_login()
# Status: "Opening browser for authentication..." (blue)
# Button: disabled
# Browser opens: accounts.google.com OAuth page
# User signs in with Google account
# Browser redirects: http://localhost:8080/callback?code=...
# Local server captures code
# Token exchanged and stored
# Status: "Login successful!" (green)
# on_success() called -> navigate to dashboard

# Failed desktop login (user cancels)
login._handle_desktop_login()
# Status: "Opening browser for authentication..."
# Browser opens
# User cancels OAuth consent
# login_desktop() returns without storing credentials
# is_authenticated() returns False
# Status: "Login completed but authentication failed" (red)
# Button: enabled for retry
```

## See Also

- `handle_login()`: Routes to this for desktop platforms
- `GoogleAuth`: Provides login_desktop()
- `handle_success()`: Called on successful authentication
- `handle_error()`: Called on exceptions

## Notes

- Blocks during authentication (synchronous flow)
- Local server starts on random available port
- Server automatically stops after callback received
- Browser opens automatically via auth service
- User must complete OAuth in browser
- Timeout typically 5 minutes for user to authenticate
- Network errors handled gracefully
- Button re-enabled on failure for retry
- Success callback handles navigation
