---
id: "update_file"
sidebar_position: 17
title: "update_file"
---

# ⚙️ update_file

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`drive_service.py`](./drive_service.py) | **Line:** 1458
:::

Update existing file's content and optionally rename.

Replaces file content with new data from local file. Can also
rename file in single operation.

## Parameters

- **`file_id`** (str): ID of file to update in Drive.
- **`file_path`** (str): Path to local file with new content.
- **`new_name`** (str, optional): New name for file in Drive. If None, name unchanged. Defaults to None.

## Returns

**Type**: `dict or None`

                - id (str): File ID (unchanged)
                - name (str): File name (new if renamed)
                - mimeType (str): MIME type
                - modifiedTime (str): New modification timestamp
                Returns None on update failure.

## Algorithm

  - 1. **Try Update Process**:
    - a. Enter try block for error handling

  - 2. **Build Metadata**:
    - a. Create empty file_metadata dictionary
    - b. If new_name provided:
    - i. Add to metadata: file_metadata['name'] = new_name

  - 3. **Create Media Upload**:
    - a. Instantiate MediaFileUpload(file_path, resumable=True)
    - b. Loads new file content

  - 4. **Execute Update**:
    - a. Call service.files().update() with:
    - i. fileId: file_id
    - ii. body: file_metadata (name if provided)
    - iii. media_body: media object
    - iv. fields: 'id, name, mimeType, modifiedTime'
    - b. Execute request
    - c. Returns updated file dict

  - 5. **Invalidate Cache**:
    - a. Call _invalidate_cache(file_id)
    - b. Clears cached file info

  - 6. **Return Result**:
    - a. Return updated_file dictionary

  - 7. **Handle Errors**:
    - a. Catch any Exception
    - b. Print error message
    - c. Return None

## Interactions

- **MediaFileUpload**: Handles file upload
- **service.files().update()**: Drive update API
- **_invalidate_cache()**: Cache management

## Example

```python
# Update content only
result = drive.update_file('file_id', 'new_content.txt')
print(f"Updated: {result['modifiedTime']}")

# Update and rename
result = drive.update_file(
    'file_id',
    'new_content.pdf',
    new_name='Report Final.pdf'
    )

# Handle failure
result = drive.update_file('invalid_id', 'file.txt')
if not result:
    print("Update failed")
```

## See Also

- `upload_file()`: Upload new file
- `rename_file()`: Rename without updating content

## Notes

- Replaces entire file content
- Optional rename in same operation
- Resumable upload for reliability
- Invalidates file cache
- modifiedTime updated automatically
- Returns None on failure
