---
id: "__init__"
sidebar_position: 3
title: "__init__"
---

# 🔧 __init__

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 113
:::

Initialize authentication manager.

## Parameters

- **`credentials_file`** (str, optional): Path to OAuth client secrets JSON. Defaults to 'web.json' in module directory.

## Example

```python
auth = GoogleAuth()  # Uses default web.json
auth = GoogleAuth('/path/to/credentials.json')
```
