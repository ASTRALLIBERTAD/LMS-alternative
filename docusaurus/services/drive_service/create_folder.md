---
id: "create_folder"
sidebar_position: 15
title: "create_folder"
---

# ⚙️ create_folder

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`drive_service.py`](./drive_service.py) | **Line:** 1224
:::

Create a new folder in Google Drive.

Creates a folder with specified name in the given parent folder.
Automatically invalidates parent folder cache.

## Parameters

- **`folder_name`** (str): Name for the new folder. Can contain any characters valid in Drive (avoid / and \\ for compatibility).
- **`parent_id`** (str, optional): Parent folder ID where folder will be created. Use 'root' for root folder or specific folder ID. Defaults to 'root'.

## Returns

**Type**: `dict or None`

                - id (str): New folder ID
                - name (str): Folder name
                Returns None if creation fails.

## Algorithm

- 1. **Define Request Function**:
    - a. Create make_request() closure
    - b. Build file_metadata dictionary:
    - i. name: folder_name
    - ii. mimeType: 'application/vnd.google-apps.folder'
    - iii. parents: [parent_id]
    - c. Call service.files().create() with metadata
    - d. Specify fields: 'id, name'
    - e. Execute request
    - f. Returns created folder dict

  - 2. **Execute Mutation**:
    - a. Call _execute_file_mutation() with:
    - i. operation_name: "create_folder(&#123;folder_name&#125;)"
    - ii. request_func: make_request
    - iii. parent_id: parent_id (for cache invalidation)
    - b. Returns result or None

## Interactions

- **service.files().create()**: Drive API create endpoint
- **_execute_file_mutation()**: Mutation wrapper

## Example

```python
# Create in root
folder = drive.create_folder('My Folder')
print(f"Created: {folder['name']} (ID: {folder['id']})")

# Create in specific folder
folder = drive.create_folder('Subfolder', parent_id='parent_id')

# Handle failure
folder = drive.create_folder('New Folder', parent_id='invalid')
if folder:
    print("Success")
    else:
    print("Failed")
```

## See Also

- `list_files()`: List created folder
- `_execute_file_mutation()`: Mutation wrapper

## Notes

- Folder MIME type: application/vnd.google-apps.folder
- Automatically invalidates parent cache
- Returns None on failure
- Folder name need not be unique
- Created folder initially empty
