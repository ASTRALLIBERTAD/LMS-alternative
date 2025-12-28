---
id: "_save_credentials"
sidebar_position: 6
title: "_save_credentials"
---

# ⚙️ _save_credentials

![Completeness](https://img.shields.io/badge/Docs-0%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 181
:::

Persist credentials to token.pickle.

Serializes current credentials for session persistence across restarts.

## Security Considerations

:::note
- Token file contains sensitive access tokens
            - Should not be committed to version control
            - Use appropriate file permissions (chmod 600)
:::
