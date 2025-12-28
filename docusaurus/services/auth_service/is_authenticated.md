---
id: "is_authenticated"
sidebar_position: 11
title: "is_authenticated"
---

# ⚙️ is_authenticated

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 384
:::

Check if currently authenticated with valid credentials.

Automatically refreshes expired tokens if refresh token available.

## Returns

**Type**: `bool`


## Example

```python
if auth.is_authenticated():
    service = auth.get_service()
    else:
    auth.login_desktop()
```

## See Also

- `get_service()`: Get authenticated Drive service
- `login_desktop()`: Authenticate user

## Notes

- May make network request to refresh token
- Safe to call frequently
- Saves refreshed credentials automatically
