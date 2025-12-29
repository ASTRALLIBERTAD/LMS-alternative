---
id: "datamanager"
sidebar_position: 2
title: "DataManager"
---

# 📦 DataManager

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-20%25-red)

:::info Source
**File:** [`data_manager.py`](./data_manager.py) | **Line:** 17
:::

Manages data persistence for the LMS application.

## Attributes

- **`data_dir`** (Path): Local file system path for storing JSON data files.
- **`drive_service`** (DriveService): Instance of the Drive service for cloud operations.
- **`lms_root_id`** (str): The ID of the root LMS folder in Google Drive.
- **`assignments_file`** (Path): Path to the local assignments JSON file.
- **`students_file`** (Path): Path to the local students JSON file.
- **`submissions_file`** (Path): Path to the local submissions JSON file.

## Examples

```python
dm = DataManager("data", drive_service)
assignments = dm.load_assignments()
dm.save_students(student_list)
```

## See Also

- `DriveService`
- `load_json_file()`
