---
id: "module"
sidebar_position: 1
title: "Module"
---

# 📁 Module

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Completeness](https://img.shields.io/badge/Docs-20%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 1
:::

Google Authentication Service Module.

Provides OAuth 2.0 authentication for Google Drive API with credential
management, token refresh, and session persistence.

## Example

```python
from services.auth_service import GoogleAuth
auth = GoogleAuth('web.json')
auth.login_desktop()
service = auth.get_service()
```

## See Also

- `DriveService`: Uses GoogleAuth for authenticated API access
- `ui.login`: Desktop authentication interface
