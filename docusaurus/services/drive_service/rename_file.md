---
id: "rename_file"
sidebar_position: 21
title: "rename_file"
---

# ⚙️ rename_file

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`drive_service.py`](./drive_service.py) | **Line:** 1844
:::

Rename file or folder without moving.

Changes file name while keeping in same location.
Invalidates parent folder cache.

## Parameters

- **`file_id`** (str): ID of file or folder to rename.
- **`new_name`** (str): New name for file. Can include extension.

## Returns

**Type**: `dict or None`

                - id (str): File ID (unchanged)
                - name (str): New file name
                - parents (list): Parent folder IDs (unchanged)
                Returns None if rename fails.

## Algorithm

- 1. **Define Request Function**:
    - a. Create make_request() closure
    - b. Build metadata: file_metadata = &#123;'name': new_name&#125;
    - c. Call service.files().update() with:
    - i. fileId: file_id
    - ii. body: file_metadata
    - iii. fields: 'id, name, parents'
    - d. Execute and return

  - 2. **Execute with Retry**:
    - a. Call _retry_request(make_request, operation_name)
    - b. Returns updated_file or None

  - 3. **Invalidate Caches** (if successful):
    - a. If updated_file not None:
    - i. For each parent in updated_file['parents']:
    - - Call _invalidate_cache(parent)
    - ii. Call _invalidate_cache(file_id)

  - 4. **Return Result**:
    - a. Return updated_file (success) or None (failure)

## Interactions

- **service.files().update()**: Drive rename API
- **_retry_request()**: Retry wrapper
- **_invalidate_cache()**: Cache management

## Example

```python
# Rename file
result = drive.rename_file('file_id', 'New Name.pdf')
print(f"Renamed to: {result['name']}")

# Change extension
result = drive.rename_file('file_id', 'document.txt')

# Handle failure
result = drive.rename_file('invalid_id', 'Name')
if not result:
    print("Rename failed")
```

## See Also

- `move_file()`: Move to different folder
- `update_file()`: Update content and optionally rename

## Notes

- Name only, location unchanged
- Invalidates parent and file caches
- Extension change allowed
- Name need not be unique
- Returns None on failure
