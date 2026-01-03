---
id: "load_assignments"
sidebar_position: 7
title: "load_assignments"
---

# ⚙️ load_assignments

![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-20%25-red)

:::info Source
**File:** [`data_manager.py`](./data_manager.py) | **Line:** 272
:::

Load list of assignments.

## Purpose

Retrieves assignment data and ensures data integrity (assigning IDs if missing).

## Returns

**Type**: `list[dict]`


## Algorithm

  - 1. Load data via `_load_from_drive_or_local`.
  - 2. Iterate through assignments.
  - 3. Check if 'id' exists; if not, generate one based on timestamp.
  - 4. If any IDs generated, save the repaired list.
  - 5. Return list.

## Interactions

- Calls `_load_from_drive_or_local`.
- Calls `save_assignments` (if integrity repair needed).
