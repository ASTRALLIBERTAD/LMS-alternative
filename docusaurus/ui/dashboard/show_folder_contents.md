---
id: "show_folder_contents"
sidebar_position: 6
title: "show_folder_contents"
---

# ⚙️ show_folder_contents

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`dashboard.py`](./dashboard.py) | **Line:** 555
:::

Display contents of a specific Google Drive folder.

Navigates to a folder and displays its contents in the main view area.
Delegates actual loading and display logic to the folder_navigator
module while maintaining a simple interface for external callers.

## Parameters

- **`folder_id`** (str): Google Drive ID of the folder to display. Must be a valid Drive folder ID accessible by authenticated user. Example: '1abc...xyz' (33-character alphanumeric string).
- **`folder_name`** (str, optional): Display name for the folder, shown in breadcrumb navigation and title. If None, name is fetched from Drive API. Defaults to None.
- **`is_shared_drive`** (bool, optional): Whether this folder is in a shared (team) drive rather than user's personal My Drive. Affects permission handling and API parameters. Defaults to False.
- **`push_to_stack`** (bool, optional): Whether to add current folder to navigation history stack for back button functionality. Set to False when going backward to prevent stack duplication. Defaults to True.

## Returns

**Type**: `None`

                Does not return folder data directly.

## Algorithm

- **Phase 1: Delegate to FolderNavigator**:
  - 1. Access self.folder_navigator instance
  - 2. Call show_folder_contents() method on navigator
  - 3. Pass all four parameters through unchanged:
    - a. folder_id: target folder identifier
    - b. folder_name: optional display name
    - c. is_shared_drive: team drive flag
    - d. push_to_stack: history tracking flag

- **Phase 2: FolderNavigator Processing** (handled internally):
  - 1. Update current_folder_id and current_folder_name
  - 2. Push previous folder to folder_stack if push_to_stack=True
  - 3. Query Drive API for folder contents
  - 4. Clear folder_list.controls
  - 5. Build UI cards for files and subfolders
  - 6. Populate folder_list with new content
  - 7. Update breadcrumb navigation trail
  - 8. Call page.update() to render changes

## Interactions

- **FolderNavigator**: Delegates all folder display logic
- **DriveService**: Navigator uses this to query folder contents
- **folder_list**: Navigator populates with folder contents
- **folder_stack**: Navigator manages navigation history

## Example

```python
# Navigate to a subfolder from current folder
dashboard.show_folder_contents(
    'folder_abc123',
    'Documents',
    is_shared_drive=False,
    push_to_stack=True
    )
# folder_list now shows contents of Documents folder
print(dashboard.current_folder_name)
# Documents

# Navigate to team drive folder
dashboard.show_folder_contents(
    'shared_xyz789',
    'Team Projects',
    is_shared_drive=True,
    push_to_stack=True
    )

# Go back without adding to stack
previous_folder_id = dashboard.folder_stack.pop()
dashboard.show_folder_contents(
    previous_folder_id,
    push_to_stack=False
    )
```

## See Also

- `FolderNavigator`: Handles logic
- `refresh_folder_contents()`: Reload current folder
- `show_todo_view()`: Switch to assignment view

## Notes

- This is a convenience wrapper for external callers
- All folder display logic encapsulated in FolderNavigator
- folder_name is optional; fetched from API if not provided
- push_to_stack=False used for back navigation to avoid loops
- Shared drives require different API parameters (handled internally)
- Invalid folder_id will result in error from Drive API
