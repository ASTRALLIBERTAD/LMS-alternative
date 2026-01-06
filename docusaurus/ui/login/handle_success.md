---
id: "handle_success"
sidebar_position: 7
title: "handle_success"
---

# ⚙️ handle_success

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`login.py`](./login.py) | **Line:** 560
:::

Handle successful authentication completion.

Updates the UI to display success message and invokes the success
callback to navigate to the main application view. Called by subclass
implementations after successful OAuth token retrieval and validation.

## Returns

**Type**: `None`


## Algorithm

- **Phase 1: Update Status Display**:
  - 1. Call update_status() with success message
  - 2. Set message to "Login successful!"
  - 3. Set color to ft.Colors.GREEN_600 (success color)
  - 4. Leave button state unchanged (remains in current state)

- **Phase 2: Invoke Success Callback**:
  - 1. Check if self.on_success is not None
  - 2. If callback exists:
    - a. Call self.on_success()
    - b. Typically navigates to dashboard
    - c. May perform additional setup (e.g., load user data)
  - 3. If callback is None:
    - a. Take no action
    - b. UI displays success message only

## Interactions

- **update_status()**: Shows success message to user
- **on_success callback**: Invoked for post-login navigation

## Example

```python
# Define success callback
def on_login_success():
    page.go('/dashboard')
    load_user_data()
    print('Login complete')

login = LoginView(page, provider, auth, on_login_success)

# After successful authentication
login.handle_success()
# Status: "Login successful!" (green)
# on_login_success() called
# User navigated to dashboard
```

## See Also

- `update_status()`: Updates status message
- `handle_error()`: Handles authentication failures
- `handle_login()`: Initiates authentication flow

## Notes

- Called by subclass after successful OAuth token validation
- Success callback is optional (None check performed)
- Callback should handle navigation and post-login setup
- UI update provides visual confirmation before navigation
- Button state not explicitly changed (typically already disabled)
- Callback may trigger page navigation (removes login view)
