---
id: "__init__"
sidebar_position: 3
title: "__init__"
---

# 🔧 __init__

![Completeness](https://img.shields.io/badge/Docs-20%25-red)

:::info Source
**File:** [`data_manager.py`](./data_manager.py) | **Line:** 60
:::

Initialize the DataManager.

## Purpose

Sets up file paths and initial configuration for data storage.

## Parameters

- **`data_dir`** (str | Path): Directory path for local data storage.
- **`drive_service`** (DriveService, optional): Service instance for Drive syncing.

## Interactions

- Calls `_load_lms_root_id` to fetch configuration.
- Sets public attributes for file paths.
