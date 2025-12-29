---
id: "notify_new_assignment"
sidebar_position: 6
title: "notify_new_assignment"
---

# ⚙️ notify_new_assignment

![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-20%25-red)

:::info Source
**File:** [`notification_service.py`](./notification_service.py) | **Line:** 122
:::

Notify students of a newly created assignment.

## Parameters

- **`assignment`** (dict): Assignment details.
- **`students`** (list): List of student records.

## Algorithm

- 1. Create notification message.
  - 2. Send individual notifications to each student.
  - 3. Send single OS summary notification to instructor.
