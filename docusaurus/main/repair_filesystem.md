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

- **Phase 1: Try File System Scan**:
  - 1. Enter outer try block for error handling
  - 2. Call os.listdir(cwd) to get list of files
  - 3. Store in files list

- **Phase 2: Process Each File**:
  - 1. For each filename in files list:
    - a. Check if "\\" (backslash) in filename
    - b. If backslash not present, skip to next file

- **Phase 3: Repair Malformed Filename**:
  - 1. If backslash present:
    - a. Replace "\\" with os.sep (platform separator)
    - - Windows: os.sep = "\\"
    - - Unix/Mac: os.sep = "/"
    - b. Store result in new_path variable

- **Phase 4: Create Missing Directories**:
  - 1. Extract directory from new_path using os.path.dirname()
  - 2. Store in dir_name variable
  - 3. If dir_name not empty and doesn't exist:
    - a. Call os.makedirs(dir_name, exist_ok=True)
    - b. Creates all intermediate directories

- **Phase 5: Rename File**:
  - 1. Enter inner try block for rename operation
  - 2. Call os.rename(filename, new_path)
  - 3. Moves file to corrected path
  - 4. If OSError occurs:
    - a. Pass silently (file may be locked or permission denied)

- **Phase 6: Handle All Errors**:
  - 1. Outer except catches any Exception
  - 2. Pass silently (don't interrupt app startup)
  - 3. Errors include: directory not accessible, permission issues

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
