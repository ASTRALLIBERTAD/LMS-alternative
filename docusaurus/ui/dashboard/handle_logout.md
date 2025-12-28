---
id: "handle_logout"
sidebar_position: 10
title: "handle_logout"
---

# ⚙️ handle_logout

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`dashboard.py`](./dashboard.py) | **Line:** 882
:::

Handle user logout process.

Terminates the user's authenticated session and triggers the
logout callback to return to the login screen. Cleans up
authentication state and invalidates access tokens.

## Parameters

- **`e`** (ft.ControlEvent): Flet control event from button click. Typically from "ACCOUNT" or logout button. Not used in logic but required by Flet event handler signature.

## Returns

**Type**: `None`

                navigating to login screen or clearing session.

## Algorithm

- 1. **Clear Authentication**:
    - a. Call self.auth.logout()
    - b. Auth service clears stored credentials
    - c. Invalidates OAuth2 access and refresh tokens
    - d. Removes cached user information

  - 2. **Trigger Logout Callback**:
    - a. Call self.on_logout() (callback from __init__)
    - b. Callback typically performs:
    - i. Clear page contents (page.clean())
    - ii. Reset application state
    - iii. Navigate to login screen
    - iv. Display logout confirmation message

  - 3. **Session Termination**:
    - a. User returned to unauthenticated state
    - b. Dashboard instance effectively terminated
    - c. New login required to access Drive features

## Interactions

- **GoogleAuth**: Calls logout() to clear credentials
- **on_logout callback**: Executes provided logout handler
- **ft.Page**: Callback typically clears and rebuilds page

## Example

```python
# Define logout handler
def return_to_login():
    page.clean()
    page.add(LoginScreen(page))
    page.update()

dashboard = Dashboard(page, auth, return_to_login)

# User clicks logout button
dashboard.handle_logout(click_event)
# auth.logout() called -> credentials cleared
# return_to_login() called -> page reset to login screen
```

## See Also

- `GoogleAuth`: Handles logout process
- `__init__()`: Receives on_logout callback parameter

## Notes

- Logout callback provided during dashboard initialization
- Auth service handles credential cleanup
- Event parameter required but unused
- Callback should handle page navigation/cleanup
- User must re-authenticate to access dashboard again
- No confirmation dialog (implement in callback if needed)
