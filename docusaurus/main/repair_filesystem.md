---
id: "repair_filesystem"
sidebar_position: 3
title: "repair_filesystem"
---

# ⚙️ repair_filesystem

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`main.py`](./main.py) | **Line:** 124
:::

Repair malformed filenames from Android file system issues.

Fixes filenames containing backslashes that occur when files are created
on Android's file system and then synced to other platforms. Android may
create files with literal backslashes in names which appear as directory
separators on other systems, causing path resolution failures.

## Purpose

- Fix Android file system compatibility issues
        - Repair backslash-containing filenames
        - Ensure proper directory structure
        - Enable cross-platform file access

## Parameters

- **`cwd`** (str): Current working directory to scan for malformed filenames. Typically the directory where application data is stored. Only this directory is scanned (not recursive).

## Returns

**Type**: `None`


## Algorithm

- 1. **Try File System Scan**:
- a. Enter outer try block for error handling
- b. Call os.listdir(cwd) to get list of files
- c. Store in files list

- 2. **Process Each File**:
- a. For each filename in files list:
  - i. Check if "\\" (backslash) in filename
  - ii. If backslash not present, skip to next file

- 3. **Repair Malformed Filename**:
- a. If backslash present:
  - i. Replace "\\" with os.sep (platform separator)
    - - Windows: os.sep = "\\"
    - - Unix/Mac: os.sep = "/"
  - ii. Store result in new_path variable

- 4. **Create Missing Directories**:
- a. Extract directory from new_path using os.path.dirname()
- b. Store in dir_name variable
- c. If dir_name not empty and doesn't exist:
  - i. Call os.makedirs(dir_name, exist_ok=True)
  - ii. Creates all intermediate directories

- 5. **Rename File**:
- a. Enter inner try block for rename operation
- b. Call os.rename(filename, new_path)
- c. Moves file to corrected path
- d. If OSError occurs:
  - i. Pass silently (file may be locked or permission denied)

- 6. **Handle All Errors**:
- a. Outer except catches any Exception
- b. Pass silently (don't interrupt app startup)
- c. Errors include: directory not accessible, permission issues

## Interactions

- **os.listdir()**: Lists files in directory
- **os.path.dirname()**: Extracts directory from path
- **os.path.exists()**: Checks directory existence
- **os.makedirs()**: Creates directory hierarchy
- **os.rename()**: Renames/moves file
- **os.sep**: Platform-specific path separator

## Example

```python
# Android creates file: "data\\config.json"
# (backslash literally in filename)
repair_filesystem('/home/user/lms')
# After repair on Unix: "data/config.json"
# Directory "data" created, file moved to data/config.json

# Windows example: no change needed
# File: "data\\config.json" is already correct on Windows
repair_filesystem('C:\\Users\\User\\lms')
# os.sep = "\\" so replacement has no effect
```

## See Also

- `main()`: Calls this during initialization
- `os.path`: Path manipulation utilities

## Notes

- Only processes top-level directory (not recursive)
- Fails silently to avoid startup interruption
- Android-specific issue but safe on all platforms
- Creates intermediate directories as needed
- Handles permission and lock errors gracefully
- Only processes filenames with backslashes
- Safe to call on directories without issues
