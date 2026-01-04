---
id: "load_credentials"
sidebar_position: 4
title: "load_credentials"
---

# ⚙️ load_credentials

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`main.py`](./main.py) | **Line:** 240
:::

Load OAuth 2.0 credentials from JSON configuration file.

Searches multiple locations for the OAuth credentials file (web.json),
parses its contents, and extracts client ID, secret, and redirect URIs
needed for Google OAuth authentication. Supports both 'web' and 'installed'
application configurations.

## Purpose

- Locate OAuth credentials file in multiple locations
        - Parse JSON configuration safely
        - Extract OAuth client credentials
        - Support both web and installed app configs
        - Enable Google authentication initialization

## Parameters

- **`app_path`** (str): Application source directory path. Typically the src directory where main.py is located. Used to search for credentials in services subdirectory.
- **`cwd`** (str): Current working directory. Where user launched application. Used to search for credentials in local services subdirectory.

## Returns

**Type**: `dict or None`

            - path (str): Absolute path to credentials file
            - client_id (str): OAuth 2.0 client ID from Google Console
            - client_secret (str): OAuth 2.0 client secret
            - redirect_uris (list): List of authorized redirect URIs
            Returns None if no valid credentials file found in any location.

## Algorithm

- **Phase 1: Define Search Paths**:
  - 1. Create possible_paths list with 4 locations:
    - a. app_path/services/web.json (deployed location)
    - b. cwd/services/web.json (local development)
    - c. app_path/web.json (root fallback)
    - d. cwd/web.json (local root fallback)
  - 2. Paths checked in order (first match wins)

- **Phase 2: Search Each Path**:
  - 1. For each creds_path in possible_paths:
    - a. Check if file exists using os.path.exists()
    - b. If file doesn't exist, continue to next path

- **Phase 3: Try Loading File**:
  - 1. If file exists, enter try block
  - 2. Open file in read mode
  - 3. Parse JSON with json.load()
  - 4. Store in data variable

- **Phase 4: Extract Configuration**:
  - 1. Try to get 'web' section: data.get('web')
  - 2. If 'web' is None, try 'installed': data.get('installed')
  - 3. Store in config variable
  - 4. If config is None (neither section found), continue to next path

- **Phase 5: Build Credentials Dict**:
  - 1. If config found, create dictionary with:
    - a. 'path': creds_path (file location)
    - b. 'client_id': config.get('client_id')
    - c. 'client_secret': config.get('client_secret')
    - d. 'redirect_uris': config.get('redirect_uris', [])
  - 2. Return credentials dictionary immediately

- **Phase 6: Handle Errors**:
  - 1. Catch any Exception during file read/parse
  - 2. Continue to next path (file may be malformed)

- **Phase 7: Return None** (if no valid file found):
  - 1. If all paths checked without success
  - 2. Return None to indicate failure

## Interactions

- **os.path.exists()**: Checks file existence
- **os.path.join()**: Constructs file paths
- **json.load()**: Parses JSON content
- **File I/O**: Opens and reads credential file

## Example

```python
app_path = "/home/user/lms/src"
cwd = "/home/user/lms"
creds = load_credentials(app_path, cwd)
if creds:
    print(f"Client ID: {creds['client_id']}")
    print(f"Redirects: {creds['redirect_uris']}")
    else:
    print("Credentials not found!")
# Client ID: 123456-abc.apps.googleusercontent.com
# Redirects: ['http://localhost:8550/oauth_callback']

# File not found scenario
creds = load_credentials("/invalid", "/paths")
print(creds)
# None
```

## See Also

- `main()`: Uses credentials for OAuth initialization
- `GoogleAuth`: Consumes credentials
- `GoogleOAuthProvider`: Uses client ID/secret

## Notes

- Searches 4 locations in priority order
- Supports both 'web' and 'installed' app types
- First valid file found is used (no merging)
- Returns None if no valid file found (caller must handle)
- Malformed JSON files skipped silently
- redirect_uris defaults to empty list if missing
- File must be named exactly "web.json"
- OAuth credentials from Google Cloud Console
