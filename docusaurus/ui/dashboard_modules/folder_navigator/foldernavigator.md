---
id: "foldernavigator"
sidebar_position: 2
title: "FolderNavigator"
---

# 📦 FolderNavigator

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Completeness](https://img.shields.io/badge/Docs-20%25-red)

:::info Source
**File:** [`folder_navigator.py`](./folder_navigator.py) | **Line:** 18
:::

Dashboard folder navigation system with history and breadcrumb management.

FolderNavigator manages the complete folder browsing experience in the Dashboard,
including navigation state tracking, folder content loading, back button history
stack, search functionality, and view switching between My Drive, Shared Drives,
and Paste Links. It maintains navigation context and coordinates between the
Dashboard UI and DriveService backend.
This class implements a browser-like navigation pattern with forward navigation
(clicking folders), backward navigation (back button with history stack), and
root-level view switching. It handles loading states, error conditions, and
provides smooth transitions between different folder contexts while maintaining
user's navigation history for intuitive browsing.

## Purpose

- Manage folder navigation state and history
        - Load and display folder contents
        - Handle back button with history stack
        - Switch between view contexts (My Drive, Shared Drives)
        - Execute search queries and display results
        - Refresh folder contents with cache invalidation
        - Coordinate UI updates with Drive API calls
        - Provide loading indicators and error handling

## Attributes

- **`dash`** (Dashboard): Reference to parent Dashboard instance. Provides access to current_view, current_folder_id, current_folder_name, folder_stack, folder_list UI control, drive service, file_manager, and page for updates. All navigation state stored in Dashboard for accessibility.

## Interactions

- **Dashboard**: Parent container managing overall state
- **DriveService**: Backend for Drive API operations (via dash.drive)
- **FileManager**: Creates file/folder UI items (via dash.file_manager)
- **ft.Text**: Status messages and headers
- **ft.IconButton**: Back button control
- **ft.ProgressRing**: Loading indicators
- **ft.Row**: Layout for controls and items
- Algorithm (High-Level Workflow):
- *Phase 1: Initialization**
- 1. Store Dashboard reference
- 2. Access navigation state from Dashboard
- 3. Ready to load and navigate folders
- *Phase 2: Root View Loading**
- 1. User selects view (My Drive/Shared Drives)
- 2. Set current_view and current_folder_id
- 3. Clear folder_list UI
- 4. Fetch root-level contents from Drive
- 5. Create UI items for each folder
- 6. Update page to display
- *Phase 3: Folder Navigation** (Forward)
- 1. User clicks folder item
- 2. Push current context to history stack
- 3. Update current_folder_id and name
- 4. Clear folder_list
- 5. Add back button if history exists
- 6. Show loading indicator
- 7. Fetch folder contents from Drive
- 8. Create UI items for contents
- 9. Remove loading indicator
- 10. Update page with new view
- *Phase 4: Back Navigation**
- 1. User clicks back button
- 2. Pop previous context from stack
- 3. Restore previous folder_id and name
- 4. Route to appropriate loader:
- a. root → load view (My Drive/Shared/Paste)
- b. folder → show_folder_contents
- 5. Update page with restored view
- *Phase 5: Search Execution**
- 1. User submits search query
- 2. Call drive.search_files with query
- 3. Clear folder_list
- 4. Create UI items for results
- 5. Update page with search results
- *Phase 6: Refresh Operation**
- 1. User clicks refresh button
- 2. Invalidate cache for current folder
- 3. Reload folder contents (no stack push)
- 4. Update page with fresh data

## Example

```python
# Initialize in Dashboard
from ui.dashboard_modules.folder_navigator import FolderNavigator
navigator = FolderNavigator(dashboard)

# Load My Drive root
navigator.load_your_folders()
# Displays root-level folders

# Navigate into folder
navigator.show_folder_contents(
    folder_id='folder_abc123',
    folder_name='Documents'
    )
# Shows Documents folder contents
# Back button appears
# History stack: [('root', 'My Drive')]

# Navigate deeper
navigator.show_folder_contents(
    folder_id='folder_xyz789',
    folder_name='Reports'
    )
# History stack: [('root', 'My Drive'), ('folder_abc123', 'Documents')]

# Go back
navigator.go_back()
# Returns to Documents folder
# History stack: [('root', 'My Drive')]

# Search
dashboard.search_field.value = "budget"
navigator.handle_search(event)
# Shows search results for "budget"

# Refresh current folder
navigator.refresh_folder_contents()
# Reloads current folder with fresh data
```

## See Also

- `Dashboard`: Parent container
- `DriveService`: Backend operations
- `FileManager`: UI item creation

## Notes

- Navigation state stored in Dashboard (not FolderNavigator)
- History stack enables back button functionality
- Root folder ID is "root" (Drive API convention)
- push_to_stack=False prevents duplicate history entries
- Loading indicators show during API calls
- Error messages display on API failures
- Search queries filter across entire Drive
- Shared drives treated as special folders
- Cache invalidation ensures fresh data on refresh
- Navigation State (in Dashboard):
- current_view: "your_folders", "shared_drives", or "paste_links"
- current_folder_id: Drive ID of currently displayed folder
- current_folder_name: Display name for breadcrumb/header
- folder_stack: List of (id, name) tuples for back navigation

## References

- Browser History API: [https://developer.mozilla.org/en-US/docs/Web/API/History](https://developer.mozilla.org/en-US/docs/Web/API/History)
- Google Drive API: [https://developers.google.com/drive/api/v3/reference](https://developers.google.com/drive/api/v3/reference)
- Material Design Navigation: [https://m3.material.io/components/navigation-drawer](https://m3.material.io/components/navigation-drawer)
