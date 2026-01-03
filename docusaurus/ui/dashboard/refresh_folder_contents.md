---
id: "refresh_folder_contents"
sidebar_position: 7
title: "refresh_folder_contents"
---

# ⚙️ refresh_folder_contents

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`dashboard.py`](./dashboard.py) | **Line:** 649
:::

Refresh the currently displayed folder contents.

Reloads the current folder to reflect any changes made since it was
last loaded. Useful after file uploads, deletions, renames, or when
syncing with changes made in other clients or by other users.

## Returns

**Type**: `None`


## Algorithm

- **Delegate to FolderNavigator**:
  - 1. Access self.folder_navigator instance
  - 2. Call refresh_folder_contents() method

- **Navigator Refresh Process** (handled internally):
  - 1. Read current_folder_id from dashboard state
  - 2. Query Drive API for latest folder contents
  - 3. Clear existing folder_list.controls
  - 4. Rebuild UI cards for current files and subfolders
  - 5. Preserve current breadcrumb navigation
  - 6. Call page.update() to render changes
  - 7. Maintain scroll position if possible

## Interactions

- **FolderNavigator**: Executes refresh logic
- **DriveService**: Queries API for current folder state
- **folder_list**: Repopulated with refreshed content

## Example

```python
# User uploads a file
dashboard.file_manager.upload_file('document.pdf')

# Refresh to show newly uploaded file
dashboard.refresh_folder_contents()
# folder_list now includes document.pdf

# Another user shares a file to this folder
# Refresh to see the new shared file
dashboard.refresh_folder_contents()
```

## See Also

- `show_folder_contents()`: Navigate to different folder
- `FolderNavigator`: Refresh logic

## Notes

- Does not change current folder or navigation history
- Useful after file operations to show updated state
- Preserves current scroll position in folder_list
- No API optimization (always fetches full folder data)
- Consider calling after uploads, deletes, or renames
