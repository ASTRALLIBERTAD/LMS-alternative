---
id: "login_with_token"
sidebar_position: 8
title: "login_with_token"
---

# ⚙️ login_with_token

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 469
:::

Authenticate using OAuth tokens from external provider.

Creates Google credentials from token data received from Flet's OAuth
provider or mobile authentication. Validates and refreshes tokens if
needed, then saves credentials for session persistence.

## Parameters

- **`token_data`** (dict): OAuth token dictionary containing: - access_token (str, required): OAuth access token for API calls - refresh_token (str, optional): Token for refreshing access - client_id (str, optional): OAuth client ID (falls back to instance attr) - client_secret (str, optional): Client secret (falls back to instance attr) - scope (str or list, optional): Granted scopes (defaults to SCOPES)

## Returns

**Type**: `bool`

                False if token invalid, missing required fields, or validation failed.

## Algorithm

- **Phase 1: Validate Input**
  - 1. Print status: "Bridging OAuth token to Google credentials"
  - 2. Print token_data type for debugging
  - 3. Check if token_data is dictionary type
  - 4. If not dict, print error and return False

- **Phase 2: Extract Access Token(required)**
  - 1. Get access_token from token_data
  - 2. If not present, print error and return False
  - 3. Access token is required minimum

- **Phase 3: Extract Optional Fields**
  - 1. Get refresh_token (may be None)
  - 2. Get client_id (use from token_data or self.client_id)
  - 3. Get client_secret (use from token_data or self.client_secret)
  - 4. Get scope (from token_data or default to SCOPES)

- **Phase 4: Process Scope**
  - 1. If scope is string:
  - 2. Split by whitespace to create list
    - a. If empty, use default SCOPES
  - 3. If scope is already list, use as-is

- **Phase 5: Log Token Status**
  - 1. Call _log_token_status() with extracted values
  - 2. Prints presence of each component for debugging

- **Phase 6: Create Credentials Object**
  - 1. Instantiate google.oauth2.credentials.Credentials with:
  - 2. token=access_token
    - a. refresh_token=refresh_token (may be None)
    - b. token_uri="https://oauth2.googleapis.com/token"
    - c. client_id=client_id
  - 3. client_secret=client_secret
    - a. scopes=scope (as list)
  - 4. Store in self.creds

- **Phase 7: Validate and Refresh**
  - 1. Call _validate_and_refresh_credentials()
  - 2. Checks if credentials valid
  - 3. Attempts refresh if expired and refresh_token present
  - 4. If validation fails, return False

- **Phase 8: Save Credentials**
  - 1. Call _save_credentials()
  - 2. Persists to token.pickle
  - 3. Return True (success)

- **Phase 9: Handle Errors**
  - 1. Catch any Exception
  - 2. Import traceback for detailed error info
  - 3. Print error message and full traceback
  - 4. Return False (failure)

## Interactions

- **google.oauth2.credentials.Credentials**: Creates credentials object
- **_log_token_status()**: Logs token components
- **_validate_and_refresh_credentials()**: Validates tokens
- **_save_credentials()**: Persists credentials

## Example

```python
# From Flet OAuth provider
token_data = {
    'access_token': 'ya29.a0AfH6SMBx...',
    'refresh_token': '1//0gTVgG...',
    'client_id': '123-abc.apps.googleusercontent.com',
    'client_secret': 'GOCSPX-...',
    'scope': 'openid email profile https://www.googleapis.com/auth/drive'
    }
auth = GoogleAuth()
success = auth.login_with_token(token_data)
# Bridging OAuth token to Google credentials
# Token data type: <class 'dict'>
# Access token: present
# Refresh token: present

print(success)
# True

# Invalid token data
success = auth.login_with_token({'invalid': 'data'})
print(success)
# False
```

## See Also

- `login_desktop()`: Alternative desktop authentication
- `_validate_and_refresh_credentials()`: Validates tokens
- `_log_token_status()`: Debugging helper
- `FirebaseMobileLogin`: Mobile OAuth

## Notes

- Supports tokens from external OAuth providers (Flet, Firebase)
- access_token is required minimum
- refresh_token optional but recommended for long sessions
- Client credentials fall back to instance attributes
- Scope can be space-separated string or list
- Validates and refreshes tokens immediately
- Saves credentials on success for persistence
- Returns bool for error handling by caller
