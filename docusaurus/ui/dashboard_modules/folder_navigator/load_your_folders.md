---
id: "load_your_folders"
sidebar_position: 4
title: "load_your_folders"
---

# ⚙️ load_your_folders

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`folder_navigator.py`](./folder_navigator.py) | **Line:** 228
:::

Load and display user's My Drive root folder view.

Resets navigation to My Drive root, fetches root-level folders,
counts subfolders for each, and displays as list items. Clears
any previous view and history.

## Returns

**Type**: `None`


## Algorithm

  - 1. **Set View Context**:
    - a. Set dash.current_view = "your_folders"
    - b. Set dash.current_folder_id = "root"
    - c. Set dash.current_folder_name = "My Drive"
    - d. Establishes root context

  - 2. **Clear UI**:
    - a. Call dash.folder_list.controls.clear()
    - b. Removes all previous list items

  - 3. **Try Folder Loading**:
    - a. Enter try block for error handling
    - b. Call dash.drive.list_files("root", page_size=100)
    - c. Returns &#123;'files': [...], 'nextPageToken': ...&#125; or None

  - 4. **Handle API Result**:
    - a. If result is None:
    - i. API call failed (network error)
    - ii. Append error text: "Failed to load folders."
    - b. If result is dict:
    - i. Extract files list: result.get("files", [])
    - ii. Filter folders only:
    - - List comprehension
    - - mimeType == "application/vnd.google-apps.folder"
    - iii. Store in folders list

  - 5. **Process Folders**:
    - a. If folders list empty:
    - i. Append message: "No folders found"
    - b. Else for each folder:
    - i. Fetch subfolder count:
    - - Call drive.list_files(folder["id"], page_size=100)
    - - Get sub_result
    - - If None: sub_count = 0
    - - Else: Filter for folders, count length
    - ii. Create UI item:
    - - Call file_manager.create_folder_item(folder, sub_count)
    - iii. Append to folder_list.controls

  - 6. **Handle Errors**:
    - a. Catch any Exception (network, API, parsing)
    - b. Append error message: "Error loading your folders" (RED)

  - 7. **Update Display**:
    - a. Call dash.page.update()
    - b. Renders all changes to UI

## Interactions

- **DriveService.list_files()**: Fetches root and subfolder contents
- **FileManager.create_folder_item()**: Creates UI components
- **Dashboard.folder_list**: UI control for display
- **ft.Text**: Status and error messages

## Example

```python
# Load My Drive root view
navigator.load_your_folders()
# Dashboard shows:
# - "Documents" (5 folders)
# - "Photos" (2 folders)
# - "Projects" (0 folders)

# Empty root
navigator.load_your_folders()
# Shows: "No folders found"

# Network error
navigator.load_your_folders()
# Shows: "Failed to load folders."
```

## See Also

- `show_folder_contents()`: Navigate into folder
- `load_shared_drives()`: Alternative root view
- `list_files()`: API method

## Notes

- Only shows folders (not files) at root level
- Counts subfolders for each (depth 1 only)
- Subfolder count may be slow for many folders
- Clears history and previous view
- Network errors handled gracefully
- Empty state shows friendly message
- Page size 100 (Drive API limit 1000)
