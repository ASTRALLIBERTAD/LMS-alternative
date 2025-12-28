---
id: "logout"
sidebar_position: 12
title: "logout"
---

# ⚙️ logout

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Completeness](https://img.shields.io/badge/Docs-20%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 427
:::

Clear authentication and remove stored credentials.

Deletes token.pickle and clears in-memory credentials. User must
re-authenticate on next use.

## Example

```python
auth.logout()
# Logging out...
# Token file removed
```

## See Also

- `login_desktop()`: Re-authenticate after logout

## Notes

- Does not revoke tokens server-side
- Only removes local credential storage
- Safe to call when not authenticated

## Security Considerations

:::note
- Tokens remain valid until expiry
            - For full revocation, use Google Account settings
:::
