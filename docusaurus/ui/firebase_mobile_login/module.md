---
id: "module"
sidebar_position: 1
title: "Module"
---

# 📁 Module

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Completeness](https://img.shields.io/badge/Docs-20%25-red)

:::info Source
**File:** [`firebase_mobile_login.py`](./firebase_mobile_login.py) | **Line:** 1
:::

Firebase Mobile Login Module.

This module provides a mobile-friendly OAuth authentication UI component
for the Learning Management System. It handles Google OAuth 2.0 authentication
on mobile platforms where native OAuth popups are unavailable.

## Example

```python
login_view = FirebaseMobileLogin(
    page=page,
    auth_service=auth,
    firebase_config=config,
    oauth_client_id="client_id",
    on_success=lambda: page.go("/dashboard")
    )
page.add(login_view)
```
