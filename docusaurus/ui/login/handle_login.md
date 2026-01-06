---
id: "handle_login"
sidebar_position: 12
title: "handle_login"
---

# ⚙️ handle_login

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`login.py`](./login.py) | **Line:** 967
:::

Handle login button click with platform-specific authentication flow.

Detects the current platform and routes to the appropriate OAuth
authentication method. Desktop platforms use local server callback,
mobile platforms use external browser with redirect.

## Parameters

- **`e`** (ft.ControlEvent): Flet control event from login button click. Not used in logic but required by Flet event handler signature.

## Returns

**Type**: `None`


## Algorithm

- **Phase 1: Platform Detection**:
  - 1. Define desktop platforms list:
    - a. ft.PagePlatform.WINDOWS
    - b. ft.PagePlatform.LINUX
    - c. ft.PagePlatform.MACOS
  - 2. Check if self.page.platform in desktop platforms list
  - 3. Store result in is_desktop boolean

- **Phase 2: Route to Appropriate Handler**:
  - 1. If is_desktop is True:
    - a. Call self._handle_desktop_login()
    - b. Uses local HTTP server for OAuth callback
  - 2. If is_desktop is False (mobile):
    - a. Call self._handle_mobile_login()
    - b. Uses external browser with redirect URL

## Interactions

- **ft.Page.platform**: Reads platform enum for detection
- **_handle_desktop_login()**: Desktop OAuth flow
- **_handle_mobile_login()**: Mobile OAuth flow

## Example

```python
# On Windows desktop
login.page.platform = ft.PagePlatform.WINDOWS
login.handle_login(click_event)
# Routes to _handle_desktop_login()
# Local server starts on localhost
# Browser opens to Google OAuth

# On Android mobile
login.page.platform = ft.PagePlatform.ANDROID
login.handle_login(click_event)
# Routes to _handle_mobile_login()
# External browser opens to Google OAuth
# Redirect handled externally
```

## See Also

- `_handle_desktop_login()`: Desktop authentication flow
- `_handle_mobile_login()`: Mobile authentication flow
- `ft.PagePlatform`: Platform enumeration

## Notes

- Platform detection automatic via Flet
- Desktop: Windows, Linux, macOS
- Mobile: Android, iOS, other platforms
- Clear separation between desktop and mobile flows
- Event parameter required but unused
