---
id: "module"
sidebar_position: 1
title: "Module"
---

# 📁 Module

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Completeness](https://img.shields.io/badge/Docs-20%25-red)

:::info Source
**File:** [`main.py`](./main.py) | **Line:** 1
:::

LMS Alternative - Main Application Module.

This module serves as the entry point for the Learning Management System (LMS)
Alternative application built with Flet. It handles application initialization,
OAuth configuration, authentication flow routing, and view management.

## Functions

- setup_paths: Configure Python path for module imports.
- repair_filesystem: Fix malformed filenames from Android file system.
- load_credentials: Load OAuth credentials from JSON file.
- get_redirect_url: Get the OAuth redirect URL for desktop authentication.
- main: Main application entry point and Flet page handler.

## Example

```python
# Run the application directly::

# $ python main.py

# Or use Flet's app runner::

import flet as ft
ft.app(target=main)
```

## See Also

- `GoogleAuth`: Authentication service.
- `Dashboard`: Main dashboard view.
- `LoginView`: Desktop login view.
