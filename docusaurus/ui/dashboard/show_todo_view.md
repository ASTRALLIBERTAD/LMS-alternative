---
id: "show_todo_view"
sidebar_position: 9
title: "show_todo_view"
---

# ⚙️ show_todo_view

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`dashboard.py`](./dashboard.py) | **Line:** 766
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

- **Phase 1: Update View State**:
  - 1. Set self.current_view to "todo"
  - 2. Marks dashboard as displaying assignment view
  - 3. Used by other methods to check active view

- **Phase 2: Clear Current Content**:
  - 1. Access self.folder_list.controls
  - 2. Call clear() to remove all folder/file cards
  - 3. Prepares container for TodoView

- **Phase 3: Create TodoView Instance**:
  - 1. Instantiate TodoView with three parameters:
    - a. self.page: for UI rendering and updates
    - b. on_back: callback set to folder_navigator.load_your_folders
    - - Provides back button functionality
    - - Returns user to folder view when clicked
    - c. drive_service: self.drive for file operations
    - - Enables assignment file uploads/downloads
  - 2. TodoView initializes with assignment data loading

- **Phase 4: Display TodoView**:
  - 1. Call todo_view.get_view() to build UI component
  - 2. Returns ft.Column or ft.Container with TodoView UI
  - 3. Append returned component to folder_list.controls

- **Phase 5: Refresh UI**:
  - 1. Call self.page.update()
  - 2. Renders TodoView in main content area
  - 3. Folder view replaced with assignment interface

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
