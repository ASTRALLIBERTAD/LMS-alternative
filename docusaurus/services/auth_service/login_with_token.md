---
id: "login_with_token"
sidebar_position: 8
title: "login_with_token"
---

# ⚙️ login_with_token

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 455
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

- 1. **Validate Input**:
    - a. Print status: "Bridging OAuth token to Google credentials"
    - b. Print token_data type for debugging
    - c. Check if token_data is dictionary type
    - d. If not dict, print error and return False

  - 2. **Extract Access Token** (required):
    - a. Get access_token from token_data
    - b. If not present, print error and return False
    - c. Access token is required minimum

  - 3. **Extract Optional Fields**:
    - a. Get refresh_token (may be None)
    - b. Get client_id (use from token_data or self.client_id)
    - c. Get client_secret (use from token_data or self.client_secret)
    - d. Get scope (from token_data or default to SCOPES)

  - 4. **Process Scope**:
    - a. If scope is string:
    - i. Split by whitespace to create list
    - ii. If empty, use default SCOPES
    - b. If scope is already list, use as-is

  - 5. **Log Token Status**:
    - a. Call _log_token_status() with extracted values
    - b. Prints presence of each component for debugging

  - 6. **Create Credentials Object**:
    - a. Instantiate google.oauth2.credentials.Credentials with:
    - i. token=access_token
    - ii. refresh_token=refresh_token (may be None)
    - iii. token_uri="https://oauth2.googleapis.com/token"
    - iv. client_id=client_id
    - v. client_secret=client_secret
    - vi. scopes=scope (as list)
    - b. Store in self.creds

  - 7. **Validate and Refresh**:
    - a. Call _validate_and_refresh_credentials()
    - b. Checks if credentials valid
    - c. Attempts refresh if expired and refresh_token present
    - d. If validation fails, return False

  - 8. **Save Credentials**:
    - a. Call _save_credentials()
    - b. Persists to token.pickle
    - c. Return True (success)

  - 9. **Handle Errors**:
    - a. Catch any Exception
    - b. Import traceback for detailed error info
    - c. Print error message and full traceback
    - d. Return False (failure)

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
