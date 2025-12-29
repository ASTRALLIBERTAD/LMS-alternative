---
id: "_preview_file"
sidebar_position: 8
title: "_preview_file"
---

# ⚙️ _preview_file

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`submission_manager.py`](./submission_manager.py) | **Line:** 1351
:::

Launch file preview overlay for submitted assignment file.

Opens a modal overlay displaying the contents of a Google Drive file
using the FilePreviewService. Supports various file types including
documents, spreadsheets, presentations, images, and PDFs.

## Parameters

- **`file_id`** (str): Google Drive file ID to preview.
- **`file_name`** (str): Display name of the file (shown in preview header).

## Returns

**Type**: `None`


## Algorithm

- 1. **Service Availability Check**:
    - a. Check if self.file_preview attribute is not None
    - b. If file_preview is None:
    - i. FilePreviewService failed to import or initialize
    - ii. Preview functionality unavailable
    - iii. Proceed to step 5 (silent return)

  - 2. **File ID Validation**:
    - a. Check if file_id parameter is provided
    - b. Check if file_id is not None and not empty string
    - c. If file_id invalid:
    - i. No file to preview
    - ii. Proceed to step 5 (silent return)

  - 3. **Preview Service Invocation**:
    - a. Both conditions met (service available, file_id valid)
    - b. Call self.file_preview.show_preview() method
    - c. Pass file_id parameter (Google Drive file identifier)
    - d. Pass file_name parameter (display name for preview header)

  - 4. **Preview Display**:
    - a. FilePreviewService handles:
    - i. Fetching file content from Google Drive
    - ii. Determining file type (doc, pdf, image, etc.)
    - iii. Rendering appropriate preview interface
    - iv. Creating modal overlay with preview content
    - v. Adding close button for user to dismiss
    - b. Preview overlay appears on screen
    - c. User can view file content without leaving application

  - 5. **Silent Failure**:
    - a. If any condition failed (service unavailable or invalid file_id):
    - i. Function returns immediately with no action
    - ii. No error message displayed to user
    - iii. No exception raised
    - iv. Graceful degradation (button simply has no effect)

  - 6. **Return to Caller**:
    - a. Function completes (no return value needed)
    - b. Control returns to event handler
    - c. Application continues normal operation

## Interactions

- **FilePreviewService**: Calls show_preview() method to display file
- **DriveService**: Service uses Drive API to fetch file content

## Example

```python
# Preview student's submitted document
submission_mgr._preview_file(
    '1abc...xyz',
    'Project_Report.docx'
    )
# Modal overlay appears with document preview

# Handle missing file_id gracefully
submission_mgr._preview_file(None, 'file.txt')
# No action taken, no error raised
```

## See Also

- `view_submissions_dialog()`: Calls this from "Preview File" button
- `FilePreviewService`: Preview service
- `_open_drive_file()`: Alternative to open file in browser

## Notes

- Requires FilePreviewService to be initialized (checked in __init__)
- Silently fails if file_preview is None (service unavailable)
- Silently fails if file_id is None or empty
- Preview overlay provides close button for user
- Supports multiple file formats depending on service implementation
- Does not handle file download (use browser link for that)
