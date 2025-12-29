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

- 1. **Delegate to FolderNavigator**:
    - a. Access self.folder_navigator instance
    - b. Call refresh_folder_contents() method

  - 2. **Navigator Refresh Process** (handled internally):
    - a. Read current_folder_id from dashboard state
    - b. Query Drive API for latest folder contents
    - c. Clear existing folder_list.controls
    - d. Rebuild UI cards for current files and subfolders
    - e. Preserve current breadcrumb navigation
    - f. Call page.update() to render changes
    - g. Maintain scroll position if possible

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
