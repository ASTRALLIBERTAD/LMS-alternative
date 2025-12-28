---
id: "get_user_info"
sidebar_position: 14
title: "get_user_info"
---

# ⚙️ get_user_info

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 498
:::

Retrieve authenticated user's account information.

Fetches user profile from Drive API including email and display name.

## Returns

**Type**: `dict`

                - emailAddress (str): User's email
                - displayName (str): User's display name
                - photoLink (str): Profile photo URL
                Returns empty dict {} on error.

## Example

```python
user = auth.get_user_info()
print(f"Logged in as: {user['emailAddress']}")
# ✓ User info retrieved: user@example.com
# Logged in as: user@example.com
```

## See Also

- `get_service()`: Required for API access
- `is_authenticated()`: Check auth first

## Notes

- Requires authenticated service
- Returns {} if not authenticated
- Makes API request to Google
