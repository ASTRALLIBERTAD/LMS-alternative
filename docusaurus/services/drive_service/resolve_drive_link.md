---
id: "resolve_drive_link"
sidebar_position: 13
title: "resolve_drive_link"
---

# ⚙️ resolve_drive_link

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`drive_service.py`](./drive_service.py) | **Line:** 1063
:::

Parse Google Drive URL and retrieve file information.

Extracts file ID from Drive URL and fetches file metadata.
Handles multiple URL formats (folders, files, query parameters).

## Parameters

- **`link`** (str): Google Drive URL or raw file ID. Supported formats: - File URL: "`https://drive.google.com/file/d/&#123;id&#125;/view"` - Folder URL: "`https://drive.google.com/drive/folders/&#123;id&#125;"` - Query param: "...?id=&#123;id&#125;" - Raw ID: "&#123;id&#125;" (33-char alphanumeric)

## Returns

**Type**: `tuple`

                - file_id (str): Extracted Drive ID or None
                - file_info (dict): File metadata from get_file_info() or None
                Returns (None, None) if parsing fails or file not found.

## Algorithm

  - 1. **Extract File ID**:
    - a. Call extract_drive_id(link)
    - b. Handles URL parsing with regex patterns
    - c. Returns file ID or None

  - 2. **Validate Extraction**:
    - a. If file_id is None:
    - i. Print error message with link
    - ii. Return (None, None)

  - 3. **Get File Info**:
    - a. Call self.get_file_info(file_id)
    - b. Returns file metadata dict or None

  - 4. **Validate Info**:
    - a. If info is None:
    - i. Print error message with file_id
    - ii. Return (None, None)

  - 5. **Return Success**:
    - a. Return tuple (file_id, info)

## Interactions

- **utils.common.extract_drive_id()**: URL parsing utility
- **get_file_info()**: Metadata retrieval

## Example

```python
# Parse file URL
url = "https://drive.google.com/file/d/1abc...xyz/view"
file_id, info = drive.resolve_drive_link(url)
if file_id:
    print(f"File: {info['name']}")

# Parse folder URL
url = "https://drive.google.com/drive/folders/1def...uvw"
folder_id, info = drive.resolve_drive_link(url)

# Handle raw ID
file_id, info = drive.resolve_drive_link('1abc...xyz')

# Handle failure
file_id, info = drive.resolve_drive_link('invalid_url')
if not file_id:
    print("Could not resolve link")
```

## See Also

- `extract_drive_id()`: URL parsing
- `get_file_info()`: Metadata retrieval

## Notes

- Supports multiple URL formats
- Handles raw file IDs
- Returns (None, None) on any failure
- Prints error messages for debugging
- Useful for user-provided Drive links
