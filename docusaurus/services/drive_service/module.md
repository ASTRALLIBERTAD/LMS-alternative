---
id: "module"
sidebar_position: 1
title: "Module"
---

# 📁 Module

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Completeness](https://img.shields.io/badge/Docs-20%25-red)

:::info Source
**File:** [`drive_service.py`](./drive_service.py) | **Line:** 1
:::

Google Drive Service Module.

This module provides a high-level interface for Google Drive API operations
with built-in caching, retry logic, and error handling.

## Example

```python
from services.auth_service import GoogleAuth
auth = GoogleAuth()
drive = DriveService(auth.get_service())
files = drive.list_files('root')
```

## See Also

- `GoogleAuth`: Provides the API service.
