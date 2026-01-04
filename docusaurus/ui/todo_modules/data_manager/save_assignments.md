---
id: "save_assignments"
sidebar_position: 10
title: "save_assignments"
---

# ⚙️ save_assignments

![Completeness](https://img.shields.io/badge/Docs-20%25-red)

:::info Source
**File:** [`data_manager.py`](./data_manager.py) | **Line:** 346
:::

Persist assignment list to storage.

## Purpose

Saves the current state of assignments.

## Parameters

- **`assignments`** (list[dict]): The list of assignments to save.

## Interactions

- Calls `_save_to_local_and_drive`.
