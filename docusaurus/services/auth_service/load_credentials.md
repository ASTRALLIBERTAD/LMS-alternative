---
id: "load_credentials"
sidebar_position: 5
title: "load_credentials"
---

# ⚙️ load_credentials

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 220
:::

Load saved OAuth credentials from pickle file.

Attempts to restore a previous authentication session by unpickling
the credentials object from token.pickle. Enables session persistence
across application restarts.

## Returns

**Type**: `None`

                Remains None if file doesn't exist or unpickling fails.

## Algorithm

- **Phase 1: Check File Existence**
  - 1. Check if self.token_file exists
  - 2. If not, return early (no saved session)

- **Phase 2: Try Loading Credentials**
  - 1. Enter try block for error handling
  - 2. Open token_file in binary read mode ('rb')
  - 3. Use context manager for automatic closing
  - 4. Call pickle.load(token) to deserialize
  - 5. Store result in self.creds
  - 6. Print success message

- **Phase 3: Handle Errors**
  - 1. Catch any Exception during unpickling
  - 2. Print warning message with error details
  - 3. Set self.creds = None (invalid session)

## Interactions

- **os.path.exists()**: Checks file existence
- **pickle.load()**: Deserializes credentials object
- **File I/O**: Opens file in binary mode

## Example

```python
# First run - no token file
auth = GoogleAuth()
print(auth.creds)
# None

# After login and save
auth.login_desktop()
# token.pickle created

# Second run - session restored
auth2 = GoogleAuth()
print(auth2.creds)
# <Credentials object>
print(auth2.is_authenticated())
# True
```

## See Also

- `__init__()`: Calls this during initialization
- `_save_credentials()`: Saves credentials to pickle
- `is_authenticated()`: Validates loaded credentials

## Notes

- Token file may not exist (first run or after logout)
- Credentials may be expired even if loaded successfully
- Pickle format is Python-specific (not portable)
- Silent failure if file corrupt or wrong format
- Prints success message when credentials restored
- Credentials validated later by is_authenticated()
