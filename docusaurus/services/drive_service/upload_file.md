---
id: "upload_file"
sidebar_position: 16
title: "upload_file"
---

# ⚙️ upload_file

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`drive_service.py`](./drive_service.py) | **Line:** 1305
:::

Upload a file to Google Drive with progress tracking.

Uploads a local file to Drive using resumable upload for reliability.
Supports progress callbacks for UI updates.

## Parameters

- **`file_path`** (str): Absolute or relative path to local file to upload. File must exist and be readable.
- **`parent_id`** (str, optional): Destination folder ID. Use 'root' for root folder. Defaults to 'root'.
- **`file_name`** (str, optional): Name for file in Drive. If None, uses basename of file_path. Defaults to None.
- **`progress_callback`** (Callable, optional): Progress handler function. Signature: (current_bytes: int, total_bytes: int) -> None. Called periodically during upload. Defaults to None.

## Returns

**Type**: `dict or None`

                - id (str): File ID in Drive
                - name (str): File name
                - mimeType (str): Detected MIME type
                - size (str): File size in bytes
                - webViewLink (str): URL to view file
                - parents (list): Parent folder IDs
                Returns None on upload failure.

## Algorithm

- 1. **Try Upload Process**:
    - a. Enter try block for error handling

  - 2. **Determine File Name**:
    - a. If file_name not provided:
    - i. Import os module
    - ii. Extract basename: os.path.basename(file_path)
    - iii. Use as file_name

  - 3. **Build Metadata**:
    - a. Create file_metadata dictionary:
    - i. name: file_name
    - ii. parents: [parent_id]

  - 4. **Create Media Upload**:
    - a. Instantiate MediaFileUpload(file_path, resumable=True)
    - b. resumable=True enables chunked upload
    - c. Automatically detects MIME type

  - 5. **Create Upload Request**:
    - a. Call service.files().create() with:
    - i. body: file_metadata
    - ii. media_body: media object
    - iii. fields: comprehensive field list
    - b. Returns upload request object

  - 6. **Upload with Progress**:
    - a. Initialize response = None
    - b. While response is None:
    - i. Call request.next_chunk()
    - ii. Returns (status, response)
    - iii. If status exists and progress_callback:
    - - Call progress_callback(status.resumable_progress, status.total_size)
    - iv. Continue until upload complete

  - 7. **Invalidate Cache**:
    - a. Call _invalidate_cache(parent_id)
    - b. Updates parent folder cache

  - 8. **Return Response**:
    - a. Return uploaded file info

  - 9. **Handle Errors**:
    - a. Catch any Exception
    - b. Print error message
    - c. Return None

## Interactions

- **os.path.basename()**: Extracts filename
- **MediaFileUpload**: Handles file upload
- **service.files().create()**: Drive upload API
- **_invalidate_cache()**: Cache management

## Example

```python
# Simple upload
result = drive.upload_file('document.pdf', parent_id='folder_id')
print(f"Uploaded: {result['name']} (ID: {result['id']})")

# Custom filename
result = drive.upload_file('local.txt', file_name='remote.txt')

# Progress tracking
def show_progress(current, total):
    percent = (current / total) * 100
    print(f"Upload: {percent:.1f}%")

result = drive.upload_file(
    'large_file.zip',
    parent_id='root',
    progress_callback=show_progress
    )

# Handle failure
result = drive.upload_file('nonexistent.txt')
if result:
    print("Success")
    else:
    print("Failed")
```

## See Also

- `update_file()`: Update existing file
- `create_folder()`: Create folder first
- `googleapiclient.http.MediaFileUpload`: Upload handler

## Notes

- Resumable upload handles large files
- MIME type auto-detected from file
- Progress callback optional
- Invalidates parent cache on success
- Returns comprehensive file info
- File must exist at file_path
- Returns None on any error
