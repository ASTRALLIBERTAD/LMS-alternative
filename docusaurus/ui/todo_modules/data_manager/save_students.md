---
id: "save_students"
sidebar_position: 11
title: "save_students"
---

# ⚙️ save_students

![Completeness](https://img.shields.io/badge/Docs-20%25-red)

:::info Source
**File:** [`data_manager.py`](./data_manager.py) | **Line:** 249
:::

Persist student list to storage.

## Purpose

Saves the current registry of students.

## Parameters

- **`students`** (list[dict]): The list of students to save.

## Interactions

- Calls `_save_to_local_and_drive`.
