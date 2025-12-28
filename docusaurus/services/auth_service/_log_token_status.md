---
id: "_log_token_status"
sidebar_position: 9
title: "_log_token_status"
---

# ⚙️ _log_token_status

![Completeness](https://img.shields.io/badge/Docs-20%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 337
:::

Log token component presence for debugging.

## Parameters

- **`access_token`** (str): Access token (checked for presence only).
- **`refresh_token`** (str or None): Refresh token.
- **`client_id`** (str or None): OAuth client ID.
- **`client_secret`** (str or None): OAuth client secret.
- **`scope`** (list or str): OAuth scopes.

## Notes

- Never logs actual token values
- Only indicates presence/absence
