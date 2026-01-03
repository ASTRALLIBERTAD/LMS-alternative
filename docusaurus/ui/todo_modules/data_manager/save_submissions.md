---
id: "save_submissions"
sidebar_position: 12
title: "save_submissions"
---

# ⚙️ save_submissions

![Completeness](https://img.shields.io/badge/Docs-20%25-red)

:::info Source
**File:** [`data_manager.py`](./data_manager.py) | **Line:** 382
:::

Persist submissions list to storage.

## Purpose

Saves the current state of all submissions.

## Parameters

- **`submissions`** (list[dict]): The list of submissions to save.

## Interactions

- Calls `_save_to_local_and_drive`.
