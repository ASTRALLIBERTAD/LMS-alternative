---
id: "on_resize"
sidebar_position: 5
title: "on_resize"
---

# ⚙️ on_resize

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`dashboard.py`](./dashboard.py) | **Line:** 495
:::

Handle window resize events for responsive sidebar layout.

Adjusts sidebar visibility based on window width breakpoints to
provide optimal user experience across desktop, tablet, and mobile
devices. Implements responsive design pattern where sidebar is
always visible on desktop but collapsible on smaller screens.

## Parameters

- **`e`** (ft.ControlEvent): Flet control event triggered by window resize. Contains new page dimensions. Not directly accessed but available for extension. Required by Flet event signature.

## Returns

**Type**: `None`


## Algorithm

- 1. **Check Window Width**:
    - a. Read self.page.width (current window width in pixels)
    - b. Compare against desktop breakpoint (900px)

  - 2. **Desktop Layout** (width &gt;= 900px):
    - a. If self.page.width &gt;= 900:
    - i. Set self.sidebar_container.visible = True
    - ii. Sidebar permanently visible on desktop
    - iii. Set self.menu_open = False
    - iv. Disable mobile toggle state
    - b. Desktop users see sidebar without toggle button

  - 3. **Mobile/Tablet Layout** (width < 900px):
    - a. If self.page.width < 900:
    - i. Set sidebar_container.visible = self.menu_open
    - ii. Sidebar shows only if toggle is active
    - iii. Hamburger menu button controls visibility
    - b. Mobile users can toggle sidebar on/off

  - 4. **Refresh UI**:
    - a. Call self.page.update()
    - b. Apply visibility changes with smooth transition
    - c. Re-render affected layout components

## Interactions

- **ft.Page**: Reads width property and triggers update
- **sidebar_container**: Visibility modified based on width
- **toggle_menu()**: Complementary method for manual toggle

## Example

```python
# User resizes from mobile to desktop
dashboard.page.width = 600  # Mobile width
dashboard.menu_open = False
dashboard.on_resize(resize_event)
dashboard.sidebar_container.visible
# False  # Hidden on mobile when toggle off

# User expands window to desktop size
dashboard.page.width = 1200
dashboard.on_resize(resize_event)
dashboard.sidebar_container.visible
# True  # Always visible on desktop
dashboard.menu_open
# False  # Toggle state reset

# User shrinks back to tablet
dashboard.page.width = 800
dashboard.on_resize(resize_event)
dashboard.sidebar_container.visible
# False  # Hidden again (menu_open still False)
```

## See Also

- `toggle_menu()`: Manual sidebar toggle for mobile users
- `__init__()`: Registers this handler to page.on_resize
- `get_view()`: Creates responsive layout structure

## Notes

- Breakpoint at 900px chosen for optimal sidebar usability
- Desktop mode (&gt;=900px) disables toggle state for consistency
- Mobile mode (&lt;900px) respects user's toggle preference
- Event triggered automatically by Flet on window dimension changes
- Provides seamless responsive experience across device types
- Toggle state only meaningful on mobile/tablet viewports
