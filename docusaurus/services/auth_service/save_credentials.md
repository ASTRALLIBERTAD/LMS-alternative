---
id: "save_credentials"
sidebar_position: 6
title: "save_credentials"
---

# ⚙️ save_credentials

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 296
:::

Persist current OAuth credentials to pickle file.

Serializes the credentials object to token.pickle for session
persistence across application restarts. Called after successful
authentication or token refresh.

## Returns

**Type**: `None`


## Algorithm

- **Phase 1: Try Saving Credentials**
  - 1. Enter try block for error handling
  - 2. Open self.token_file in binary write mode ('wb')
  - 3. Use context manager for automatic closing
  - 4. Call pickle.dump(self.creds, token)
  - 5. Serializes credentials object to file
  - 6. Print success message

- **Phase 2: Handle Errors**
  - 1. Catch any Exception during pickling
  - 2. Print error message with exception details
  - 3. File may not be created if error occurs

## Interactions

- **pickle.dump()**: Serializes credentials object
- **File I/O**: Opens file in binary write mode

## Example

```python
auth = GoogleAuth()
auth.login_desktop()  # Sets self.creds
# _save_credentials() called automatically
# token.pickle now exists

# Manual save after token refresh
auth.creds.refresh(Request())
auth._save_credentials()
# Credentials saved to token.pickle
```

## See Also

- `_load_credentials()`: Loads credentials from pickle
- `login_desktop()`: Calls this after authentication
- `login_with_token()`: Calls this after token validation
- `is_authenticated()`: Calls this after refresh

## Notes

- Called automatically after successful authentication
- Called after token refresh to save new tokens
- Overwrites existing token.pickle
- File contains sensitive credentials (use .gitignore)
- Pickle format preserves full Credentials object state
