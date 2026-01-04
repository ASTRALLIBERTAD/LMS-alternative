---
id: "_load_from_drive_or_local"
sidebar_position: 5
title: "_load_from_drive_or_local"
---

# ⚙️ _load_from_drive_or_local

![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`data_manager.py`](./data_manager.py) | **Line:** 119
:::

Load data from Drive if available, falling back to local file.

## Purpose

Ensures the most up-to-date data is loaded, preferring the cloud version
            if connected to Google Drive to support cross-device usage.

## Parameters

- **`filepath`** (Path): Local path where the file is expected to be.
- **`default`** (any, optional): Value to return if data cannot be loaded. Defaults to None.

## Returns

**Type**: `any`


## Algorithm

  - 1. Check if Drive Service and Root ID are available.
  - 2. If yes:
    - a. Search for file by name in LMS root folder.
    - b. If found, download content string.
    - c. Parse JSON and return.
  - 3. Fallback: Load directly from local file path.

## Interactions

- Calls `drive_service.find_file`.
- Calls `drive_service.read_file_content`.
- Calls `utils.common.load_json_file`.
