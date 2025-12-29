---
id: "_log_token_status"
sidebar_position: 9
title: "_log_token_status"
---

# ⚙️ _log_token_status

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 619
:::

Log OAuth token components for debugging authentication issues.

Prints the presence/absence of each token component to console for
troubleshooting authentication problems. Does not print actual token
values for security.

## Parameters

- **`access_token`** (str): OAuth access token (only presence checked).
- **`refresh_token`** (str or None): Refresh token (may be None).
- **`client_id`** (str or None): OAuth client ID.
- **`client_secret`** (str or None): OAuth client secret.
- **`scope`** (list or str): Granted OAuth scopes.

## Returns

**Type**: `None`


## Algorithm

- 1. **Log Token Components**:
    - a. Print "Access token: present" (don't print actual value)
    - b. Print refresh_token status: "present" or "missing"
    - c. Print client_id status: "present" or "missing"
    - d. Print client_secret status: "present" or "missing"
    - e. Print scopes: join list or print string directly

## Interactions

- **Console output**: Prints to stdout

## Example

```python
# Called from login_with_token
auth._log_token_status(
    'token123',
    '1//refresh',
    'client_id',
    'secret',
    ['drive', 'email']
    )
# Access token: present
# Refresh token: present
# Client ID: present
# Client secret: present
# Scopes: drive, email
```

## See Also

- `login_with_token()`: Calls this for debugging

## Notes

- Never prints actual token values (security)
- Only indicates presence/absence of components
- Helps diagnose missing credentials
- Scope handling for both list and string formats
