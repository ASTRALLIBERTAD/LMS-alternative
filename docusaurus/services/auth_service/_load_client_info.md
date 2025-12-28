---
id: "_load_client_info"
sidebar_position: 4
title: "_load_client_info"
---

# ⚙️ _load_client_info

![Completeness](https://img.shields.io/badge/Docs-0%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 136
:::

Load OAuth client ID and secret from credentials file.

Extracts client_id and client_secret from JSON file. Supports both
'web' and 'installed' application types from Google Cloud Console.

## Notes

- Silently returns if file doesn't exist
- Errors logged but don't stop initialization
