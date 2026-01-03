---
id: "logout"
sidebar_position: 12
title: "logout"
---

# ⚙️ logout

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 901
:::

Log out user and clear all stored authentication data.

Clears the credentials object and deletes the token pickle file,
ending the current session. User must re-authenticate after logout.

## Returns

**Type**: `None`


## Algorithm

- **Phase 1: Log Action**
  - 1. Print "Logging out..." to console

- **Phase 2: Clear Credentials**
  - 1. Set self.creds = None
  - 2. Removes credentials from memory

- **Phase 3: Delete Token File**
  - 1. Check if self.token_file exists
  - 2. If exists:
  - 3. Enter try block for error handling
    - a. Call os.remove(self.token_file)
    - b. Print "Token file removed"
  - 4. If exception:
  - 5. Print error message with details
    - a. File may be locked or permission denied

## Interactions

- **os.path.exists()**: Checks file existence
- **os.remove()**: Deletes token file

## Example

```python
# User authenticated
auth = GoogleAuth()
auth.login_desktop()
print(auth.is_authenticated())
# True

# Logout
auth.logout()
# Logging out...
# Token file removed

# No longer authenticated
print(auth.is_authenticated())
# False

# token.pickle deleted
import os
print(os.path.exists('token.pickle'))
# False
```

## See Also

- `login_desktop()`: Re-authenticate after logout
- `login_with_token()`: Alternative re-authentication
- `is_authenticated()`: Returns False after logout

## Notes

- Clears credentials from memory immediately
- Deletes token.pickle file if exists
- Silent failure if file deletion fails
- User must re-authenticate after logout
- Does not revoke tokens with Google (tokens still valid)
- For full security, revoke tokens in Google Account settings
