---
id: "login_desktop"
sidebar_position: 7
title: "login_desktop"
---

# ⚙️ login_desktop

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Completeness](https://img.shields.io/badge/Docs-20%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 198
:::

Perform browser-based OAuth 2.0 authentication.

Launches local web server and opens browser for user to grant permissions.
Authorization code is exchanged for access and refresh tokens.

## Exceptions

FileNotFoundError: If credentials file doesn't exist.
            ImportError: If google-auth-oauthlib not installed.
            OSError: If port 8550 unavailable.

## Example

```python
auth = GoogleAuth('credentials.json')
auth.login_desktop()
# Starting desktop OAuth flow...
# ✓ Desktop login successful
```

## See Also

- `login_with_token()`: Alternative token-based auth
- `is_authenticated()`: Check auth status

## Notes

- Requires google-auth-oauthlib package
- Opens default browser
- Port 8550 must be available
- Not suitable for server environments

## Security Considerations

:::note
- Uses localhost redirect (secure)
            - Requires user interaction
:::
