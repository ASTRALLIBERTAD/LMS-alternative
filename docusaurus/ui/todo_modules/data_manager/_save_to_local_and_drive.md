---
id: "_save_to_local_and_drive"
sidebar_position: 6
title: "_save_to_local_and_drive"
---

# ⚙️ _save_to_local_and_drive

![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-20%25-red)

:::info Source
**File:** [`data_manager.py`](./data_manager.py) | **Line:** 138
:::

Save data locally and sync to Drive if connected.

## Purpose

Persists data to disk and synchronizes changes to the cloud backend.

## Parameters

- **`filepath`** (Path): Target local file path.
- **`data`** (any): Python object (dict/list) to serialize and save.

## Algorithm

- 1. Save data to local JSON file immediately.
  - 2. Check if Drive Service is connected.
  - 3. If yes:
    - a. Search for file by name in Drive root.
    - b. If found -> Update file content.
    - c. If not found -> Upload new file.

## Interactions

- Calls `utils.common.save_json_file`.
- Calls `drive_service.find_file`.
- Calls `drive_service.update_file` or `drive_service.upload_file`.
