---
id: "on_resize"
sidebar_position: 5
title: "on_resize"
---

# ⚙️ on_resize

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`dashboard.py`](./dashboard.py) | **Line:** 467
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

- **Check Window Width**:
  - 1. Read self.page.width (current window width in pixels)
  - 2. Compare against desktop breakpoint (900px)

- **Desktop Layout** (width &gt;= 900px):
  - 1. If self.page.width &gt;= 900:
    - a. Set self.sidebar_container.visible = True
    - b. Sidebar permanently visible on desktop
    - c. Set self.menu_open = False
    - d. Disable mobile toggle state
  - 2. Desktop users see sidebar without toggle button

- **Mobile/Tablet Layout** (width < 900px):
  - 1. If self.page.width < 900:
    - a. Set sidebar_container.visible = self.menu_open
    - b. Sidebar shows only if toggle is active
    - c. Hamburger menu button controls visibility
  - 2. Mobile users can toggle sidebar on/off

- **Refresh UI**:
  - 1. Call self.page.update()
  - 2. Apply visibility changes with smooth transition
  - 3. Re-render affected layout components

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
