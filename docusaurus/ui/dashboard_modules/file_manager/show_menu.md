---
id: "show_menu"
sidebar_position: 4
title: "show_menu"
---

# ⚙️ show_menu

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`file_manager.py`](./file_manager.py) | **Line:** 238
:::

Generate context menu items for file or folder operations.

Creates list of PopupMenuItem objects representing available actions
for the given file or folder. Menu content varies based on item type
and preview service availability.

## Parameters

- **`item`** (dict): File or folder metadata dictionary containing at minimum 'id' and 'name' keys. May include 'mimeType', 'size', etc.
- **`is_folder`** (bool, optional): Whether item is a folder. Affects menu options (folders cannot be previewed). Defaults to False.
- **`is_shared_drive`** (bool, optional): Whether item is shared drive root. May affect permissions and available operations. Defaults to False.

## Returns

**Type**: `list[ft.PopupMenuItem]`

                label and on_click handler. List may include:
                - "Preview" (files only, if preview service available)
                - "Info" (always)
                - "Rename" (always)
                - "Delete" (always)
                None items filtered out before return.

## Algorithm

  - 1. **Define Action Handlers** (local closures):
    - a. on_preview(e):
    - i. Check if not folder
    - ii. Call self.preview_file(item)
    - b. on_rename(e):
    - i. Call self._rename_file_dialog(item)
    - c. on_delete(e):
    - i. Call self._delete_file_dialog(item)
    - d. on_info(e):
    - i. Call self.show_file_info(item)

  - 2. **Build Menu Items List**:
    - a. Create list with conditional items:
    - i. Preview: if file_preview exists AND not folder
    - ii. Info: always included
    - iii. Rename: always included
    - iv. Delete: always included
    - b. Use ternary: item if condition else None

  - 3. **Filter None Values**:
    - a. List comprehension: [item for item if item is not None]
    - b. Removes conditional items that weren't included

  - 4. **Return Filtered List**:
    - a. Return list of valid PopupMenuItem objects

## Interactions

- **preview_file()**: Opens preview overlay
- **_rename_file_dialog()**: Shows rename input
- **_delete_file_dialog()**: Shows delete confirmation
- **show_file_info()**: Displays file metadata
- **ft.PopupMenuItem**: Menu item controls

## Example

```python
# File menu (preview available)
file_meta = {'id': '123', 'name': 'doc.pdf', 'mimeType': 'application/pdf'}
menu = file_manager.show_menu(file_meta, is_folder=False)
print([item.text for item in menu])
# ['Preview', 'Info', 'Rename', 'Delete']

# Folder menu (no preview)
folder_meta = {'id': '456', 'name': 'Docs', 'mimeType': 'application/vnd.google-apps.folder'}
menu = file_manager.show_menu(folder_meta, is_folder=True)
print([item.text for item in menu])
# ['Info', 'Rename', 'Delete']

# Without preview service
file_manager.file_preview = None
menu = file_manager.show_menu(file_meta, is_folder=False)
print([item.text for item in menu])
# ['Info', 'Rename', 'Delete']
```

## See Also

- `preview_file()`: Preview handler
- `_rename_file_dialog()`: Rename dialog
- `_delete_file_dialog()`: Delete confirmation
- `show_file_info()`: Info display
- `ft.PopupMenuItem`: Flet menu item

## Notes

- Menu dynamically generated per item
- Preview only for files with service available
- All items get info, rename, delete options
- Closures capture item in handler scope
- Filtered list contains no None values
- is_shared_drive currently unused but available
