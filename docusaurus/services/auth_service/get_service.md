---
id: "get_service"
sidebar_position: 13
title: "get_service"
---

# ⚙️ get_service

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 459
:::

Get authenticated Google Drive API service.

Creates Drive v3 API service object for making Drive API calls.
Automatically verifies authentication and refreshes tokens.

## Returns

**Type**: `googleapiclient.discovery.Resource or None`

                service, or None if not authenticated.

## Example

```python
service = auth.get_service()
if service:
    results = service.files().list(pageSize=10).execute()
    for file in results.get('files', []):
    print(file['name'])
```

## See Also

- `is_authenticated()`: Check auth before calling
- `get_user_info()`: Get authenticated user details
- `DriveService`: Wrapper for Drive operations

## Notes

- Returns None if not authenticated
- Credentials auto-refresh if needed
- Uses Drive API v3
