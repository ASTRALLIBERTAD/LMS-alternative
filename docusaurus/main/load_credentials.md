---
id: "load_credentials"
sidebar_position: 4
title: "load_credentials"
---

# ⚙️ load_credentials

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`main.py`](./main.py) | **Line:** 233
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

- 1. **Define Search Paths**:
- a. Create possible_paths list with 4 locations:
  - i. app_path/services/web.json (deployed location)
  - ii. cwd/services/web.json (local development)
  - iii. app_path/web.json (root fallback)
  - iv. cwd/web.json (local root fallback)
- b. Paths checked in order (first match wins)

- 2. **Search Each Path**:
- a. For each creds_path in possible_paths:
  - i. Check if file exists using os.path.exists()
  - ii. If file doesn't exist, continue to next path

- 3. **Try Loading File**:
- a. If file exists, enter try block
- b. Open file in read mode
- c. Parse JSON with json.load()
- d. Store in data variable

- 4. **Extract Configuration**:
- a. Try to get 'web' section: data.get('web')
- b. If 'web' is None, try 'installed': data.get('installed')
- c. Store in config variable
- d. If config is None (neither section found), continue to next path

- 5. **Build Credentials Dict**:
- a. If config found, create dictionary with:
  - i. 'path': creds_path (file location)
  - ii. 'client_id': config.get('client_id')
  - iii. 'client_secret': config.get('client_secret')
  - iv. 'redirect_uris': config.get('redirect_uris', [])
- b. Return credentials dictionary immediately

- 6. **Handle Errors**:
- a. Catch any Exception during file read/parse
- b. Continue to next path (file may be malformed)

- 7. **Return None** (if no valid file found):
- a. If all paths checked without success
- b. Return None to indicate failure

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
