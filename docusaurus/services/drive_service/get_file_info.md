---
id: "get_file_info"
sidebar_position: 12
title: "get_file_info"
---

# ⚙️ get_file_info

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`drive_service.py`](./drive_service.py) | **Line:** 933
:::

Get detailed metadata for a specific file or folder.

Retrieves comprehensive information about a file including name,
type, size, timestamps, owners, and links. Uses LRU cache for
frequently accessed files.

## Parameters

- **`file_id`** (str): Google Drive file or folder ID. Format: 33-character alphanumeric string. Example: "1abc...xyz".
- **`use_cache`** (bool, optional): Whether to use cached info. If True, checks LRU cache and time-based cache before API call. If False, always queries API. Defaults to True.

## Returns

**Type**: `dict or None`

                - id (str): File ID
                - name (str): File/folder name
                - mimeType (str): MIME type (e.g., 'application/pdf')
                - size (str, optional): Size in bytes (not present for folders)
                - createdTime (str): ISO 8601 creation timestamp
                - modifiedTime (str): ISO 8601 modification timestamp
                - owners (list): List of owner objects with displayName, emailAddress
                - parents (list): List of parent folder IDs
                - webViewLink (str): URL to view file in browser
                Returns None if file not found or API error.

## Algorithm

  - 1. **Try LRU Cache** (if use_cache=True):
    - a. Check if _cached_get_file_info exists
    - b. Try calling _cached_get_file_info(file_id)
    - c. If successful, return cached result
    - d. If exception, continue to next step

  - 2. **Generate Cache Key**:
    - a. Format: "fileinfo_&#123;file_id&#125;"
    - b. Example: "fileinfo_1abc...xyz"

  - 3. **Check Time-Based Cache** (if use_cache=True):
    - a. Call self._get_cached(cache_key)
    - b. If cached and not expired, return data

  - 4. **Define Request Function**:
    - a. Create make_request() closure
    - b. Calls service.files().get() with:
    - i. fileId=file_id
    - ii. fields: comprehensive field list
    - c. Returns file metadata dictionary

  - 5. **Execute with Retry**:
    - a. Call _retry_request(make_request, operation_name)
    - b. Returns file dict or None on failure

  - 6. **Update Cache** (if result not None):
    - a. Call _set_cache(cache_key, file)
    - b. Stores with current timestamp

  - 7. **Return Result**:
    - a. Return file dictionary or None

## Interactions

- **_cached_get_file_info**: LRU cached wrapper
- **_get_cached()**: Time-based cache check
- **service.files().get()**: Drive API endpoint
- **_retry_request()**: Retry wrapper
- **_set_cache()**: Stores result

## Example

```python
# Get file info
info = drive.get_file_info('file_abc123')
print(f"Name: {info['name']}")
print(f"Type: {info['mimeType']}")
print(f"Size: {info.get('size', 'N/A')} bytes")
print(f"Modified: {info['modifiedTime']}")
print(f"Owner: {info['owners'][0]['displayName']}")

# Get folder info
folder = drive.get_file_info('folder_xyz')
is_folder = folder['mimeType'] == 'application/vnd.google-apps.folder'

# Bypass cache for fresh data
info = drive.get_file_info('file_id', use_cache=False)

# Handle not found
info = drive.get_file_info('invalid_id')
if info:
    print("File exists")
    else:
    print("File not found")
```

## See Also

- `_setup_lru_caches()`: LRU cache initialization
- `resolve_drive_link()`: Parse URL and get info
- `list_files()`: List folder contents

## Notes

- Uses dual caching (LRU + time-based)
- LRU cache maxsize: 128 entries
- Time cache TTL: cache_ttl seconds
- Size field absent for folders
- Returns None for non-existent files
- webViewLink for browser viewing
- Comprehensive field set for all metadata
