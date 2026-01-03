---
id: "_load_lms_root_id"
sidebar_position: 4
title: "_load_lms_root_id"
---

# ⚙️ _load_lms_root_id

![Completeness](https://img.shields.io/badge/Docs-20%25-red)

:::info Source
**File:** [`data_manager.py`](./data_manager.py) | **Line:** 86
:::

Read the LMS root folder ID from local config.

## Purpose

Retrieves the Google Drive Folder ID used as the root for LMS data.

## Returns

**Type**: `str | None`


## Interactions

- Reads `lms_config.json` via `load_json_file`.
