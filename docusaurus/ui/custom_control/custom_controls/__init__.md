---
id: "__init__"
sidebar_position: 3
title: "__init__"
---

# 🔧 __init__

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`custom_controls.py`](./custom_controls.py) | **Line:** 144
:::

Initialize ButtonWithMenu with label, menu items, and callback.

Creates a styled dropdown button with specified menu options. Builds
visual appearance matching ElevatedButton and registers callback for
menu selection handling.

## Parameters

- **`text`** (str): Label text displayed on button. Shown alongside dropdown arrow. Should be concise action description. Example: "Export", "Download", "More Options".
- **`menu_items`** (list[str]): List of menu item labels. Each string becomes a selectable menu item. Order preserved in menu display. Example: ["Option 1", "Option 2", "Option 3"].
- **`on_menu_select`** (Callable, optional): Callback invoked when menu item selected. Signature: (item_text: str) -> None. Receives selected item text as parameter. None if no callback needed. Defaults to None.
- **`page`** (ft.Page, optional): Flet page instance for updates. Currently not used in implementation but stored for future enhancements. Defaults to None. **kwargs: Additional keyword arguments passed to parent PopupMenuButton constructor. Can include tooltip, disabled, etc.

## Algorithm

  - 1. **Store Page Reference**:
    - a. Assign page parameter to self.page
    - b. Available for future update operations

  - 2. **Create Menu Items**:
    - a. Initialize empty list: popup_items
    - b. For each item in menu_items:
    - i. Create ft.PopupMenuItem with text
    - ii. Set on_click to self._handle_menu_click
    - iii. Append to popup_items list
    - c. Menu items ready for popup display

  - 3. **Build Button Visual Container**:
    - a. Create ft.Row with contents:
    - i. ft.Text(text):
    - - Size: 14px
    - - Weight: W_500 (medium)
    - - Color: ON_PRIMARY (theme-based)
    - ii. ft.Icon(ARROW_DROP_DOWN):
    - - Size: 18px
    - - Color: ON_PRIMARY
    - iii. Spacing: 8px between elements
    - iv. Alignment: CENTER
    - v. Tight: True (compact layout)

    - b. Wrap Row in ft.Container (button_content):
    - i. Set bgcolor: PRIMARY (theme color)
    - ii. Set padding: horizontal=24px, vertical=10px
    - iii. Set border_radius: 20px (rounded)
    - iv. Add BoxShadow:
    - - spread_radius: 0
    - - blur_radius: 2px (subtle)
    - - color: BLACK with 30% opacity
    - - offset: (0, 1) - slight downward
    - v. Configure Animation:
    - - duration: 100ms
    - - curve: EASE_IN_OUT
    - vi. Register on_hover: self._on_hover

    - c. Store container in self.button_content

  - 4. **Initialize Parent Class**:
    - a. Call super().__init__() with:
    - i. content: button_content (styled container)
    - ii. items: popup_items (menu list)
    - iii. **kwargs: additional parameters
    - b. Parent provides menu functionality

  - 5. **Store Callback**:
    - a. Assign on_menu_select to self.on_menu_select
    - b. Used when menu item clicked

## Interactions

- **ft.PopupMenuItem**: Creates menu items
- **ft.Row**: Arranges text and icon
- **ft.Text**: Button label
- **ft.Icon**: Dropdown indicator
- **ft.Container**: Button visual styling
- **ft.PopupMenuButton.__init__()**: Parent initialization

## Example

```python
# Basic initialization
button = ButtonWithMenu(
    text="Actions",
    menu_items=["Edit", "Delete", "Share"]
    )

# With callback
def handle_action(action):
    print(f"Action selected: {action}")

button = ButtonWithMenu(
    text="File Operations",
    menu_items=["Open", "Save", "Close"],
    on_menu_select=handle_action,
    page=page
    )

# With additional PopupMenuButton parameters
button = ButtonWithMenu(
    text="Options",
    menu_items=["A", "B", "C"],
    tooltip="Select an option",
    disabled=False
    )
```

## See Also

- `_handle_menu_click()`: Callback handler
- `_on_hover()`: Hover animation handler
- `ft.PopupMenuButton`: Parent class

## Notes

- Menu items converted to PopupMenuItem objects
- All items share same click handler
- Button appearance matches ElevatedButton
- Hover effects configured during initialization
- Page parameter optional (may be None)
- **kwargs passed to parent for extended functionality
- Container stored as button_content for hover updates
- Animation configured for smooth transitions
