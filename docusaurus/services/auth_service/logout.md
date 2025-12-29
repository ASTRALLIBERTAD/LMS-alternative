---
id: "logout"
sidebar_position: 12
title: "logout"
---

# ⚙️ logout

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 877
:::

Log out user and clear all stored authentication data.

Clears the credentials object and deletes the token pickle file,
ending the current session. User must re-authenticate after logout.

## Returns

**Type**: `None`


## Algorithm

- 1. **Log Action**:
    - a. Print "Logging out..." to console

  - 2. **Clear Credentials**:
    - a. Set self.creds = None
    - b. Removes credentials from memory

  - 3. **Delete Token File**:
    - a. Check if self.token_file exists
    - b. If exists:
    - i. Enter try block for error handling
    - ii. Call os.remove(self.token_file)
    - iii. Print "Token file removed"
    - c. If exception:
    - i. Print error message with details
    - ii. File may be locked or permission denied

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
