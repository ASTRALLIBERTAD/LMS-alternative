---
id: "send_notification"
sidebar_position: 5
title: "send_notification"
---

# ⚙️ send_notification

![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`notification_service.py`](./notification_service.py) | **Line:** 316
:::

Create and dispatch a notification.

## Parameters

- **`title`** (str): Notification title.
- **`message`** (str): Notification body content.
- **`student_email`** (str, optional): Recipient email.
- **`assignment_id`** (str, optional): Related assignment ID.
- **`notification_type`** (str): Category (info, warning, etc.).

## Returns

**Type**: `bool`


## Algorithm

  - 1. Construct notification record with timestamp.
  - 2. Append to internal list and save to disk.
  - 3. Attempt to show OS notification via plyer.
