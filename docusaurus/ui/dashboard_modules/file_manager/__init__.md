---
id: "__init__"
sidebar_position: 3
title: "__init__"
---

# 🔧 __init__

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`file_manager.py`](./file_manager.py) | **Line:** 173
:::

Initialize FileManager with Dashboard reference and preview service.

Sets up file management capabilities by storing Dashboard reference and
initializing FilePreviewService for file preview functionality. Handles
import failure gracefully for preview service.

## Parameters

- **`dashboard`** (Dashboard): Parent Dashboard instance providing access to page, Drive service, current folder state, and UI update methods. Must have page, drive, and folder-related attributes initialized.

## Algorithm

- 1. **Store Dashboard Reference**:
    - a. Assign dashboard parameter to self.dash
    - b. Used for all Dashboard state access and updates

  - 2. **Initialize Preview Service**:
    - a. Enter try block for graceful failure handling
    - b. Import FilePreviewService from services module
    - c. Instantiate with dashboard.page and dashboard.drive
    - d. Store in self.file_preview

  - 3. **Handle Import Failure**:
    - a. Catch ImportError if service unavailable
    - b. Set self.file_preview = None
    - c. Preview functionality disabled but other features work
    - d. No error raised (graceful degradation)

## Interactions

- **Dashboard**: Stores reference for state access
- **FilePreviewService**: Initializes if available

## Example

```python
# Standard initialization
dashboard = Dashboard(page, auth_service)
file_manager = FileManager(dashboard)
print(file_manager.file_preview)
# <FilePreviewService instance>

# Preview service unavailable
# (service not installed or import error)
file_manager = FileManager(dashboard)
print(file_manager.file_preview)
# None
# Manager still functional, preview disabled
```

## See Also

- `Dashboard`: Parent container
- `FilePreviewService`: Preview service

## Notes

- Dashboard must be initialized before FileManager
- Preview service optional (graceful degradation)
- No exceptions raised on initialization
- file_preview checked before use in other methods
