---
id: "_load_credentials"
sidebar_position: 5
title: "_load_credentials"
---

# ⚙️ _load_credentials

![Completeness](https://img.shields.io/badge/Docs-0%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 160
:::

Load saved credentials from token.pickle.

Restores previous authentication session by unpickling credentials.
Enables session persistence across application restarts.

## Notes

- Returns silently if token file doesn't exist
- Sets creds to None on error
