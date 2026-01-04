---
id: "load_client_info"
sidebar_position: 4
title: "load_client_info"
---

# ⚙️ load_client_info

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 136
:::

Load OAuth client credentials from configuration file.

Reads the OAuth client secrets JSON file, extracts the client_id and
client_secret, and stores them as instance attributes. Supports both
'web' and 'installed' application type configurations.

## Returns

**Type**: `None`

                Both None if file doesn't exist or parsing fails.

## Algorithm

- **Phase 1: Check File Existence**
  - 1. Check if self.credentials_file exists
  - 2. If not, return early (no error, silent failure)

- **Phase 2: Try Loading File**
  - 1. Enter try block for error handling
  - 2. Open credentials_file in read mode
  - 3. Parse JSON content with json.load()
  - 4. Store in data variable

- **Phase 3: Extract Configuration Section**
  - 1. Try to get 'web' section: data.get('web')
  - 2. If 'web' is None, try 'installed': data.get('installed')
  - 3. Store result in config variable
  - 4. Supports both application types

- **Phase 4: Extract Client Credentials**
  - 1. If config found (not None):
    - a. Extract client_id: config.get('client_id')
    - b. Store in self.client_id
    - c. Extract client_secret: config.get('client_secret')
    - d. Store in self.client_secret
    - e. Print success message with filename

- **Phase 5: Handle Errors**
  - 1. Catch any Exception during file read/parse
  - 2. Print error message to console
  - 3. Client_id and client_secret remain None

## Interactions

- **os.path.exists()**: Checks file existence
- **json.load()**: Parses JSON configuration
- **os.path.basename()**: Gets filename for logging

## Example

```python
auth = GoogleAuth()
# After initialization:
print(auth.client_id)
# 123456-abc.apps.googleusercontent.com
print(auth.client_secret)
# GOCSPX-abc123...

# If file doesn't exist:
auth = GoogleAuth('/nonexistent/path.json')
print(auth.client_id)
# None
```

## See Also

- `__init__()`: Calls this during initialization
- `login_with_token()`: Uses client_id and client_secret

## Notes

- Supports both 'web' and 'installed' OAuth app types
- Silent failure if file doesn't exist (no exception)
- Prints success message on successful load
- Client credentials required for token operations
- File format matches Google Cloud Console export
