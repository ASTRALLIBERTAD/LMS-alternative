---
id: "is_authenticated"
sidebar_position: 11
title: "is_authenticated"
---

# ⚙️ is_authenticated

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 785
:::

Check if user currently has valid authentication.

Validates current credentials and attempts to refresh them if expired.
Provides the primary method for checking authentication status before
API operations.

## Returns

**Type**: `bool`

                not authenticated, credentials expired without refresh token,
                or refresh operation failed.

## Algorithm

- **Phase 1: Check Credentials Exist**
  - 1. If self.creds is None:
  - 2. No authentication performed yet
    - a. Return False immediately


- **Phase 2: Check Not Expired**
  - 1. If not self.creds.expired:
  - 2. Credentials still valid (not expired)
    - a. Return self.creds.valid (should be True)


- **Phase 3: Check Refresh Token**
  - 1. If not self.creds.refresh_token:
  - 2. Credentials expired but no refresh token
    - a. Print message: "Credentials expired and no refresh token available"
    - b. Return False (cannot refresh)


- **Phase 4: Attempt Refresh**
  - 1. Enter try block for error handling
  - 2. Print "→ Refreshing expired credentials..."
  - 3. Call self.creds.refresh(Request())
  - 4. Exchanges refresh_token for new access_token
    - a. Updates self.creds with new tokens
  - 5. Call self._save_credentials()
  - 6. Persists refreshed tokens to pickle
  - 7. Print "✓ Credentials refreshed"
  - 8. Return True (refresh successful)


- **Phase 5: Handle Refresh Errors**
  - 1. Catch any Exception during refresh
  - 2. Print error message with exception details
  - 3. Return False (refresh failed)

## Interactions

- **google.auth.transport.requests.Request**: HTTP transport
- **Credentials.refresh()**: Token refresh operation
- **_save_credentials()**: Persists refreshed credentials

## Example

```python
# Not authenticated
auth = GoogleAuth()
print(auth.is_authenticated())
# False

# After login
auth.login_desktop()
print(auth.is_authenticated())
# True

# Token expires, but refreshes automatically
# (time passes, token expires)
print(auth.is_authenticated())
# → Refreshing expired credentials...
# ✓ Credentials refreshed
# True

# Use for API access control
if auth.is_authenticated():
    service = auth.get_service()
    # Make API calls
    else:
    print("Please login first")
```

## See Also

- `login_desktop()`: Desktop authentication
- `login_with_token()`: Token-based authentication
- `get_service()`: Requires authentication
- `_save_credentials()`: Saves refreshed credentials

## Notes

- Primary method for checking auth status
- Automatically refreshes expired tokens
- Saves refreshed tokens to pickle file
- Returns False if refresh fails
- Should be called before API operations
- Token refresh requires refresh_token
- Refresh may fail if token revoked
