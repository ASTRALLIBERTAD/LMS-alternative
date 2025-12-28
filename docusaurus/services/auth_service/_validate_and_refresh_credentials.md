---
id: "_validate_and_refresh_credentials"
sidebar_position: 10
title: "_validate_and_refresh_credentials"
---

# ⚙️ _validate_and_refresh_credentials

![Completeness](https://img.shields.io/badge/Docs-20%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 357
:::

Validate credentials and refresh if expired.

## Returns

**Type**: `bool`


## Notes

- Requires refresh token for expired credentials
- Network errors result in False return
