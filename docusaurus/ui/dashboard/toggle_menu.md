---
id: "toggle_menu"
sidebar_position: 4
title: "toggle_menu"
---

# ⚙️ toggle_menu

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`dashboard.py`](./dashboard.py) | **Line:** 390
:::

Toggle sidebar menu visibility on mobile/tablet devices.

Switches the sidebar visibility state when the hamburger menu button
is clicked. Only affects behavior on smaller screens (&lt;900px width)
where the sidebar is collapsible. On desktop (&gt;=900px), sidebar
remains permanently visible.

## Parameters

- **`e`** (ft.ControlEvent): Flet control event from IconButton click. Contains event source and related data. Not used in logic but required by Flet event handler signature.

## Returns

**Type**: `None`


## Algorithm

- 1. **Toggle State**:
    - a. Read current value of self.menu_open boolean
    - b. Invert value: self.menu_open = not self.menu_open
    - c. Store new state (True becomes False, False becomes True)

  - 2. **Update Sidebar Visibility**:
    - a. Calculate visibility condition:
    - - visible = self.menu_open OR self.page.width > 700
    - b. Assign result to self.sidebar_container.visible property
    - c. Sidebar shows if: menu toggled on OR window is wide

  - 3. **Refresh UI**:
    - a. Call self.page.update()
    - b. Triggers Flet to re-render affected components
    - c. Sidebar appears or disappears with animation

## Interactions

- **ft.Page**: Updates page to render visibility changes
- **sidebar_container**: Visibility property modified based on state
- **on_resize()**: Complementary method handling window resize events

## Example

```python
# User clicks hamburger menu on mobile device
dashboard.menu_open
# False
dashboard.toggle_menu(click_event)
dashboard.menu_open
# True
dashboard.sidebar_container.visible
# True

# User clicks again to close
dashboard.toggle_menu(click_event)
dashboard.menu_open
# False
dashboard.sidebar_container.visible
# False

# On desktop (width > 700), sidebar stays visible
dashboard.page.width = 1200
dashboard.menu_open = False
dashboard.toggle_menu(click_event)
dashboard.sidebar_container.visible
# True  # Visible due to width, despite menu_open=True
```

## See Also

- `on_resize()`: Handles window resize for responsive layout
- `get_view()`: Creates sidebar_container with toggle button

## Notes

- Event parameter required by Flet but not used in logic
- Sidebar visibility uses OR logic: menu_open OR wide_screen
- State persists until next toggle or window resize
- Animation handled automatically by Flet framework
- Does not affect desktop layout (width &gt;= 900px)
