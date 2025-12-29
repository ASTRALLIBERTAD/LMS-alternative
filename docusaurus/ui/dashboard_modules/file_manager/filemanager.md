---
id: "filemanager"
sidebar_position: 2
title: "FileManager"
---

# 📦 FileManager

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Completeness](https://img.shields.io/badge/Docs-20%25-red)

:::info Source
**File:** [`file_manager.py`](./file_manager.py) | **Line:** 19
:::

Dashboard file and folder operations manager with UI component generation.

FileManager handles all file and folder-related UI components and user interactions
within the Dashboard. It creates visual representations (list items) for files and
folders, manages context menus with actions (preview, rename, delete, info), and
orchestrates modal dialogs for operations like creating folders, renaming items,
and confirming deletions.
This class acts as a bridge between the Dashboard UI and the DriveService backend,
translating user interactions into Drive API operations and updating the UI with
results. It implements a consistent interaction pattern across all file operations
with visual feedback, confirmation dialogs, and error handling.

## Purpose

- Generate UI components for files and folders
        - Manage context menus with file operations
        - Handle file preview initialization
        - Orchestrate rename and delete dialogs
        - Create new folder dialog and upload interface
        - Provide file information display
        - Navigate folder hierarchy
        - Coordinate between UI and Drive service

## Attributes

- **`dash`** (Dashboard): Reference to parent Dashboard instance. Provides access to page, drive service, current folder state, and UI refresh methods. Used for all Dashboard state modifications and updates.
- **`file_preview`** (FilePreviewService or None): Service for displaying file previews in modal overlays. Handles images, text, PDFs, and Office documents. None if service import fails (graceful degradation).

## Interactions

- **Dashboard**: Parent container managing overall state
- **DriveService**: Backend for Drive API operations (via dash.drive)
- **FilePreviewService**: File preview modal display
- **ft.Container**: File/folder list item containers
- **ft.PopupMenuButton**: Context menu implementation
- **ft.FilePicker**: System file selection dialog
- **utils.common**: Utility functions (format_file_size, create_icon_button, etc.)
- Algorithm (High-Level Workflow):
- *Phase 1: Initialization**
- 1. Store Dashboard reference
- 2. Import FilePreviewService (graceful failure if unavailable)
- 3. Initialize preview service with page and drive
- 4. Ready to create file/folder components
- *Phase 2: UI Component Creation**
- 1. Dashboard requests file/folder items
- 2. FileManager creates styled containers:
- a. Folders: Icon, name, subfolder count, menu
- b. Files: Icon, name, size, preview button, menu
- 3. Attach click handlers and context menus
- 4. Return components to Dashboard for display
- *Phase 3: User Interaction Handling**
- 1. User clicks item:
- a. Folders → navigate to folder contents
- b. Files → open preview overlay
- 2. User opens context menu:
- a. Preview (files only) → show preview
- b. Info → display file metadata dialog
- c. Rename → show rename input dialog
- d. Delete → show confirmation dialog
- *Phase 4: Operation Execution**
- 1. User confirms action in dialog
- 2. Call appropriate DriveService method
- 3. Update Dashboard UI (refresh or optimistic update)
- 4. Invalidate Drive cache if needed
- 5. Close dialog and show feedback
- *Phase 5: File Operations**
- 1. Create Folder: Input → API call → Optimistic UI update
- 2. Upload File: File picker → Upload → Refresh
- 3. Rename: Input → API call → Refresh
- 4. Delete: Confirm → API call → Refresh

## Example

```python
# Initialize in Dashboard
from ui.dashboard_modules.file_manager import FileManager
file_manager = FileManager(dashboard)

# Create folder item for display
folder_metadata = {
    'id': 'folder_123',
    'name': 'Documents',
    'mimeType': 'application/vnd.google-apps.folder'
    }
folder_item = file_manager.create_folder_item(
    folder_metadata,
    subfolder_count=5
    )
dashboard.folder_list.controls.append(folder_item)

# Create file item
file_metadata = {
    'id': 'file_456',
    'name': 'report.pdf',
    'mimeType': 'application/pdf',
    'size': '2048576'
    }
file_item = file_manager.create_file_item(file_metadata)

# User interactions handled automatically
# Click folder → navigates to folder
# Click file → opens preview
# Right-click/menu → shows context actions

# Programmatic operations
file_manager.create_new_folder_dialog()  # Shows dialog
file_manager.select_file_to_upload()     # Opens picker
```

## See Also

- `Dashboard`: Parent container
- `DriveService`: Backend operations
- `FilePreviewService`: Preview display
- `format_file_size()`: Size formatting
- `create_icon_button()`: Icon button helper

## Notes

- All file operations refresh Dashboard after completion
- Context menus dynamically generated based on item type
- Preview available only for files (not folders)
- Dialogs use overlay system (modal, blocks interaction)
- Optimistic UI updates for folder creation
- Cache invalidation ensures data consistency
- Graceful degradation if preview service unavailable
- Truncates long names (>40 chars) with ellipsis
- Shared drive flag affects menu options

## References

- Material Design Lists: [https://m3.material.io/components/lists](https://m3.material.io/components/lists)
- Flet Controls: [https://flet.dev/docs/controls](https://flet.dev/docs/controls)
- Google Drive API: [https://developers.google.com/drive/api/v3/reference](https://developers.google.com/drive/api/v3/reference)
