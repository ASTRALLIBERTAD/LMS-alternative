---
id: "show_snackbar"
sidebar_position: 14
title: "show_snackbar"
---

# ⚙️ show_snackbar

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`todo_view.py`](./todo_view.py) | **Line:** 1338
:::

Display a transient notification message at the bottom of screen.

Creates and shows a snackbar with the specified message and color,
providing temporary user feedback that auto-dismisses after a few seconds.

## Parameters

- **`message`** (str): Text message to display in snackbar. Should be concise and informative. Examples: "Assignment created!", "File uploaded successfully", "Error: Invalid input".
- **`color`** (ft.Colors, optional): Background color for snackbar. Used to indicate message type (blue=info, green=success, red=error, orange=warning). Defaults to ft.Colors.BLUE.

## Returns

**Type**: `None`


## Algorithm

- 1. **Create Snackbar**:
    - a. Instantiate ft.SnackBar
    - b. Set content to ft.Text(message)
    - c. Set bgcolor to specified color

  - 2. **Attach to Page**:
    - a. Assign snackbar to self.page.snack_bar
    - b. Replaces any existing snackbar

  - 3. **Show Snackbar**:
    - a. Set self.page.snack_bar.open = True
    - b. Makes snackbar visible

  - 4. **Update Page**:
    - a. Call self.page.update()
    - b. Renders snackbar at bottom of screen

## Interactions

- **ft.SnackBar**: Creates notification component
- **ft.Text**: Message content
- **ft.Page**: Displays and updates snackbar

## Example

```python
# Success message
todo_view.show_snackbar(
    "Assignment created successfully!",
    ft.Colors.GREEN
    )

# Error message
todo_view.show_snackbar(
    "Failed to upload file",
    ft.Colors.RED
    )

# Info message (default color)
todo_view.show_snackbar("Loading...")
```

## See Also

- `show_overlay()`: Alternative for modal dialogs
- `ft.SnackBar`: Flet snackbar component

## Notes

- Snackbar appears at bottom of screen
- Auto-dismisses after a few seconds
- Only one snackbar visible at a time
- New snackbar replaces existing one
- Color coding helps indicate message type
- Non-blocking (doesn't pause execution)
