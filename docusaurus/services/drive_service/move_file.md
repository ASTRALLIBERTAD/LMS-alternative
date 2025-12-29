---
id: "move_file"
sidebar_position: 20
title: "move_file"
---

# ⚙️ move_file

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`drive_service.py`](./drive_service.py) | **Line:** 1742
:::

Move file or folder to different parent folder.

Removes file from current parent(s) and adds to new parent.
Invalidates cache for both old and new parent folders.

## Parameters

- **`file_id`** (str): ID of file or folder to move.
- **`new_parent_id`** (str): Destination folder ID.

## Returns

**Type**: `dict or None`

                - id (str): File ID (unchanged)
                - parents (list): New parent IDs (only new_parent_id)
                Returns None if move fails.

## Algorithm

- 1. **Define Request Function**:
    - a. Create make_request() closure
    - b. Get current parents:
    - i. Call service.files().get(fileId, fields='parents')
    - ii. Extract parents list
    - iii. Join with commas: ",".join(parents)
    - c. Update file:
    - i. Call service.files().update()
    - ii. addParents: new_parent_id
    - iii. removeParents: previous_parents (comma-separated)
    - iv. fields: 'id, parents'
    - d. Execute and return

  - 2. **Execute with Retry**:
    - a. Call _retry_request(make_request, operation_name)
    - b. Returns updated_file or None

  - 3. **Invalidate Caches** (if successful):
    - a. If updated_file not None:
    - i. Get fresh parent list
    - ii. Invalidate old parents:
    - - Get file info to find old parents
    - - Invalidate each old parent cache
    - iii. Invalidate new parent: _invalidate_cache(new_parent_id)

  - 4. **Return Result**:
    - a. Return updated_file (success) or None (failure)

## Interactions

- **service.files().get()**: Get current parents
- **service.files().update()**: Move operation
- **_retry_request()**: Retry wrapper
- **_invalidate_cache()**: Cache management

## Example

```python
# Move file to new folder
result = drive.move_file('file_id', 'new_folder_id')
if result:
    print(f"Moved to: {result['parents']}")

# Move to root
result = drive.move_file('file_id', 'root')

# Handle failure
result = drive.move_file('invalid_id', 'folder_id')
if not result:
    print("Move failed")
```

## See Also

- `rename_file()`: Rename without moving
- `create_folder()`: Create destination folder

## Notes

- Removes from all current parents
- Adds to single new parent
- File can have multiple parents (uncommon)
- Invalidates both old and new parent caches
- Returns None on failure
- Parent change tracked in parents field
