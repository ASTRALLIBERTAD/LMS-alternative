---
id: "show_todo_view"
sidebar_position: 9
title: "show_todo_view"
---

# ⚙️ show_todo_view

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`dashboard.py`](./dashboard.py) | **Line:** 795
:::

Switch to the to-do/assignment management view.

Transitions the main content area from folder browsing to the
assignment management interface. Clears current folder display
and loads the TodoView component with full assignment functionality.

## Parameters

- **`e`** (ft.ControlEvent): Flet control event from button click. Typically from "TO-DO" sidebar button. Not used in logic but required by Flet event handler signature.

## Returns

**Type**: `None`


## Algorithm

- 1. **Update View State**:
    - a. Set self.current_view to "todo"
    - b. Marks dashboard as displaying assignment view
    - c. Used by other methods to check active view

  - 2. **Clear Current Content**:
    - a. Access self.folder_list.controls
    - b. Call clear() to remove all folder/file cards
    - c. Prepares container for TodoView

  - 3. **Create TodoView Instance**:
    - a. Instantiate TodoView with three parameters:
    - i. self.page: for UI rendering and updates
    - ii. on_back: callback set to folder_navigator.load_your_folders
    - - Provides back button functionality
    - - Returns user to folder view when clicked
    - iii. drive_service: self.drive for file operations
    - - Enables assignment file uploads/downloads
    - b. TodoView initializes with assignment data loading

  - 4. **Display TodoView**:
    - a. Call todo_view.get_view() to build UI component
    - b. Returns ft.Column or ft.Container with TodoView UI
    - c. Append returned component to folder_list.controls

  - 5. **Refresh UI**:
    - a. Call self.page.update()
    - b. Renders TodoView in main content area
    - c. Folder view replaced with assignment interface

## Interactions

- **TodoView**: Instantiated with page, back callback, drive service
- **FolderNavigator**: Provides load_your_folders as back callback
- **DriveService**: Passed to TodoView for assignment file operations
- **folder_list**: Cleared and repopulated with TodoView

## Example

```python
# User clicks "TO-DO" button in sidebar
dashboard.current_view
# 'your_folders'
dashboard.show_todo_view(click_event)
dashboard.current_view
# 'todo'
# Main area now shows assignment list and management interface

# User clicks back button in TodoView
# on_back callback triggers:
dashboard.folder_navigator.load_your_folders()
dashboard.current_view
# 'your_folders'
# Returns to folder browsing
```

## See Also

- `TodoView`: Assignment management interface
- `show_folder_contents()`: Switch to folder view
- `FolderNavigator`: Back navigation

## Notes

- TodoView receives drive_service for file upload functionality
- Back callback allows seamless return to folder view
- Current view state tracked in current_view attribute
- folder_list completely replaced (not added to)
- TodoView has independent state management
- Event parameter required but unused in implementation
