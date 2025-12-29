---
id: "_handle_menu_click"
sidebar_position: 5
title: "_handle_menu_click"
---

# ⚙️ _handle_menu_click

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`custom_controls.py`](./custom_controls.py) | **Line:** 405
:::

Handle menu item selection and invoke registered callback.

Processes menu item click event by extracting selected text and
calling the on_menu_select callback if registered. Logs selection
for debugging purposes.

## Parameters

- **`e`** (ft.ControlEvent): Click event from PopupMenuItem. Contains control property with reference to clicked menu item. e.control.text holds the menu item text (string).

## Returns

**Type**: `None`


## Algorithm

- 1. **Log Selection** (debugging):
    - a. Print "MENU CLICKED:" with e.control.text
    - b. Helps debug menu interaction

  - 2. **Log Callback State** (debugging):
    - a. Print "CALLING on_menu_select:" with callback reference
    - b. Shows if callback registered

  - 3. **Check Callback Registration**:
    - a. If self.on_menu_select is not None:
    - i. Callback registered, proceed
    - b. If None:
    - i. No callback, return early

  - 4. **Invoke Callback**:
    - a. Extract menu item text: e.control.text
    - b. Call self.on_menu_select(text)
    - c. Pass selected item text as parameter
    - d. Callback handles application logic

## Interactions

- **ft.ControlEvent**: Provides clicked control reference
- **ft.PopupMenuItem**: Source of text property
- **on_menu_select callback**: User-provided handler

## Example

```python
# Setup with callback
def handle_selection(item):
    print(f"Selected: {item}")
    if item == "Delete":
    confirm_delete()
    elif item == "Edit":
    open_editor()

button = ButtonWithMenu(
    text="Actions",
    menu_items=["Edit", "Delete", "Share"],
    on_menu_select=handle_selection
    )

# User clicks "Delete" menu item
# → _handle_menu_click called with event
# → Prints: "MENU CLICKED: Delete"
# → Prints: "CALLING on_menu_select: <function...>"
# → Calls: handle_selection("Delete")
# → Output: "Selected: Delete"
# → Executes: confirm_delete()
```

## See Also

- `__init__()`: Registers this handler for all menu items
- `ft.PopupMenuItem`: Menu item control

## Notes

- Called automatically when menu item clicked
- All menu items share this handler
- Item identification by text property
- Debug prints help troubleshoot menu issues
- Callback receives item text as string
- No action if callback not registered
- Menu auto-closes after selection (parent behavior)
- Event contains full control reference
