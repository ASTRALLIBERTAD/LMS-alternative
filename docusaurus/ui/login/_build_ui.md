---
id: "_build_ui"
sidebar_position: 4
title: "_build_ui"
---

# ⚙️ _build_ui

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`login.py`](./login.py) | **Line:** 245
:::

Construct and arrange all login interface UI components.

Builds the complete user interface by creating and configuring all UI
elements including header, status text, login button, and security notice.
Arranges components in a centered, vertically-stacked layout with
consistent spacing and styling.

## Returns

**Type**: `None`

                Also stores references to status_text and login_button in
                instance attributes for dynamic updates.

## Algorithm

- **Phase 1: Detect Platform**:
  - 1. Call _get_platform_name() to get human-readable platform name
  - 2. Store result in platform_name variable
  - 3. Use result for display text (e.g., "Platform: Windows")

- **Phase 2: Add Header Components**:
  - 1. Add 50px vertical spacing Container at top
  - 2. Add cloud icon (ft.Icons.CLOUD_CIRCLE):
    - a. Size: 100px
    - b. Color: BLUE_600 (brand blue)
  - 3. Add title text "Learning Management System":
    - a. Size: 32px (large, prominent)
    - b. Weight: BOLD
    - c. Alignment: CENTER
  - 4. Add subtitle text "Access your learning materials anywhere":
    - a. Size: 16px (medium)
    - b. Color: GREY_700 (subtle)
    - c. Alignment: CENTER
  - 5. Add 10px vertical spacing Container
  - 6. Add platform indicator text:
    - a. Format: "Platform: &#123;platform_name&#125;"
    - b. Size: 12px (small)
    - c. Color: GREY_600 (very subtle)
    - d. Alignment: CENTER
  - 7. Add 20px vertical spacing Container

- **Phase 3: Create Status Text**:
  - 1. Instantiate ft.Text with initial message
  - 2. Set text: "Please log in to continue"
  - 3. Set color: GREY_700 (neutral, informative)
  - 4. Set text_align: CENTER
  - 5. Store reference in self.status_text
  - 6. Append to self.controls

- **Phase 4: Create Login Button**:
  - 1. Instantiate ft.ElevatedButton with configuration:
    - a. text: "Login with Google"
    - b. icon: ft.Icons.LOGIN (sign-in icon)
    - c. on_click: self.handle_login (delegated to subclass)
  - 2. Define button style:
    - a. bgcolor: BLUE_600 (Google blue theme)
    - b. color: WHITE (text color)
    - c. padding: symmetric(horizontal=30, vertical=15)
  - 3. Set height to 50px (prominent, touch-friendly)
  - 4. Store reference in self.login_button
  - 5. Add 10px spacing Container before button
  - 6. Append button to self.controls

- **Phase 5: Add Security Notice**:
  - 1. Add 20px vertical spacing Container
  - 2. Add security text:
    - a. Content: "Secure authentication via Google OAuth 2.0"
    - b. Size: 12px (small, informational)
    - c. Color: GREY_500 (very subtle)
    - d. Alignment: CENTER
    - e. Italic: True (distinguishes from other text)
  - 3. Append to self.controls

## Interactions

- **_get_platform_name()**: Retrieves platform name for display
- **ft.Text, ft.Icon, ft.Container, ft.ElevatedButton**:
- Flet UI components for interface construction
- **handle_login()**: Abstract method called on button click

## Example

```python
# After initialization
login = ConcreteLoginSubclass(page, auth, callback)
# _build_ui already called in __init__
print(len(login.controls))
# 14  # Header + status + button + security notice + spacing
print(login.status_text.value)
# Please log in to continue
print(login.login_button.text)
# Login with Google
print(login.login_button.disabled)
# False
```

## See Also

- `_get_platform_name()`: Platform detection helper
- `handle_login()`: Login button click handler (abstract)
- `__init__()`: Calls this method during initialization

## Notes

- Components added to self.controls in display order (top to bottom)
- Status text and login button stored for later updates
- Button enabled initially, disabled during authentication
- Spacing containers provide visual separation between sections
- All text elements centered for mobile-friendly layout
- Button height (50px) and padding optimized for touch input
- Security notice builds user trust and transparency
