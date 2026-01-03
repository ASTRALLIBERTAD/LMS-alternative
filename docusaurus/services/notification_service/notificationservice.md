---
id: "notificationservice"
sidebar_position: 2
title: "NotificationService"
---

# 📦 NotificationService

![Completeness](https://img.shields.io/badge/Docs-0%25-red)

:::info Source
**File:** [`notification_service.py`](./notification_service.py) | **Line:** 52
:::

Manages application notifications and alerts.

Handles persistence of notification history to JSON and dispatches
OS-level notifications when possible.

## Attributes

- **`data_dir`** (Path): Directory for storing notification data.
- **`notifications_file`** (Path): Path to the JSON storage file.
- **`notifications`** (list): In-memory list of notification records.
- **`Algorithm`** (Pseudocode): 1. Initialize storage directory. 2. Load existing notifications from JSON. 3. On send_notification: add to list, save to file. 4. If plyer available, trigger OS notification. 5. Provide methods to filter, count unread, and mark read.
