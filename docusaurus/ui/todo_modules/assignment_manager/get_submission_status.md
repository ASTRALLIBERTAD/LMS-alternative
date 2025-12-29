---
id: "get_submission_status"
sidebar_position: 14
title: "get_submission_status"
---

# ⚙️ get_submission_status

![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`assignment_manager.py`](./assignment_manager.py) | **Line:** 870
:::

Check if a specific student has submitted an assignment.

## Purpose

Retrieves the submission record for a given assignment/student pair.

## Parameters

- **`assignment_id`** (str): Assignment ID.
- **`student_email`** (str): Student email.

## Returns

**Type**: `dict | None`


## Interactions

- Iterates `todo.submissions`.
