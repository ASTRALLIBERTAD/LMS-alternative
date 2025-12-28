---
id: "close_dialog"
sidebar_position: 8
title: "close_dialog"
---

# ⚙️ close_dialog

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`dashboard.py`](./dashboard.py) | **Line:** 731
:::

Close an open modal dialog.

Dismisses a dialog by setting its open property to False and
updating the page to remove it from the screen. Used for
closing file operation dialogs, confirmation prompts, and
form modals.

## Parameters

- **`dialog`** (ft.AlertDialog): Flet AlertDialog instance to close. Must be a dialog that was previously opened and added to page.overlay. Can be any dialog type (confirmation, form, etc.).

## Returns

**Type**: `None`


## Algorithm

- 1. **Set Dialog State**:
    - a. Access dialog.open property
    - b. Set value to False
    - c. Marks dialog as closed in Flet's state system

  - 2. **Update UI**:
    - a. Call self.page.update()
    - b. Flet removes dialog from screen
    - c. Restores focus to main content
    - d. Re-enables underlying UI interaction

## Interactions

- **ft.AlertDialog**: Modifies open property
- **ft.Page**: Updates to remove dialog from overlay

## Example

```python
# Create and show confirmation dialog
confirm_dialog = ft.AlertDialog(
    title=ft.Text("Confirm Delete"),
    content=ft.Text("Delete this file?"),
    actions=[
    ft.TextButton("Cancel", on_click=lambda e: dashboard.close_dialog(confirm_dialog)),
    ft.TextButton("Delete", on_click=lambda e: delete_and_close(e, confirm_dialog))
    ]
    )
confirm_dialog.open = True
page.overlay.append(confirm_dialog)
page.update()

# User clicks Cancel
dashboard.close_dialog(confirm_dialog)
# Dialog disappears from screen
```

## See Also

- `FileManager`: Creates file operation dialogs
- `handle_action()`: Opens dialogs for new folder/upload

## Notes

- Dialog must be in page.overlay before closing
- Does not remove dialog from overlay list (just hides it)
- Safe to call multiple times on same dialog
- Commonly used in dialog action button callbacks
- Restores keyboard focus to main content automatically
