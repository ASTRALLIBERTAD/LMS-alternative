---
id: "is_authenticated"
sidebar_position: 11
title: "is_authenticated"
---

# ⚙️ is_authenticated

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 767
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

- 1. **Check Credentials Exist**:
    - a. If self.creds is None:
    - i. No authentication performed yet
    - ii. Return False immediately

  - 2. **Check Not Expired**:
    - a. If not self.creds.expired:
    - i. Credentials still valid (not expired)
    - ii. Return self.creds.valid (should be True)

  - 3. **Check Refresh Token**:
    - a. If not self.creds.refresh_token:
    - i. Credentials expired but no refresh token
    - ii. Print message: "Credentials expired and no refresh token available"
    - iii. Return False (cannot refresh)

  - 4. **Attempt Refresh**:
    - a. Enter try block for error handling
    - b. Print "→ Refreshing expired credentials..."
    - c. Call self.creds.refresh(Request())
    - i. Exchanges refresh_token for new access_token
    - ii. Updates self.creds with new tokens
    - d. Call self._save_credentials()
    - i. Persists refreshed tokens to pickle
    - e. Print "✓ Credentials refreshed"
    - f. Return True (refresh successful)

  - 5. **Handle Refresh Errors**:
    - a. Catch any Exception during refresh
    - b. Print error message with exception details
    - c. Return False (refresh failed)

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
