---
id: "delete_file"
sidebar_position: 22
title: "delete_file"
---

# ⚙️ delete_file

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`drive_service.py`](./drive_service.py) | **Line:** 1930
:::

Permanently delete file or folder from Drive.

Deletes file and invalidates all related caches. Cannot be undone.

## Parameters

- **`file_id`** (str): ID of file or folder to delete.

## Returns

**Type**: `bool`


## Algorithm

- 1. **Get File Info First**:
    - a. Call get_file_info(file_id, use_cache=False)
    - b. Need parent info for cache invalidation
    - c. Store in file_info

  - 2. **Define Request Function**:
    - a. Create make_request() closure
    - b. Call service.files().delete(fileId=file_id)
    - c. Execute request (returns None on success)
    - d. Return True to indicate success

  - 3. **Execute with Retry**:
    - a. Call _retry_request(make_request, operation_name)
    - b. Returns True or None
    - c. Store in success variable

  - 4. **Invalidate Caches** (if successful):
    - a. If success is True:
    - i. If file_info exists and has 'parents':
    - - For each parent in file_info['parents']:
    - - Call _invalidate_cache(parent)
    - ii. Call _invalidate_cache(file_id)
    - iii. Return True

  - 5. **Return Failure**:
    - a. If success is None or False:
    - i. Return False

## Interactions

- **get_file_info()**: Get parent info
- **service.files().delete()**: Drive delete API
- **_retry_request()**: Retry wrapper
- **_invalidate_cache()**: Cache management

## Example

```python
# Delete file
success = drive.delete_file('file_id')
if success:
    print("Deleted successfully")
    else:
    print("Deletion failed")

# Delete folder (recursive)
success = drive.delete_file('folder_id')
# Deletes folder and all contents

# Confirm before delete
file = drive.get_file_info('file_id')
confirm = input(f"Delete {file['name']}? (y/n): ")
if confirm.lower() == 'y':
    drive.delete_file('file_id')
```

## See Also

- `get_file_info()`: Get file info before delete
- `list_files()`: Verify deletion

## Notes

- Permanent deletion (not trash)
- Folder deletion is recursive
- Invalidates parent caches
- Returns bool (not dict)
- File info fetched for cache invalidation
- Cannot be undone
- Deletes all folder contents if folder
