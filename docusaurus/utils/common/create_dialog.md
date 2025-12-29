---
id: "create_dialog"
sidebar_position: 11
title: "create_dialog"
---

# ⚙️ create_dialog

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`common.py`](./common.py) | **Line:** 811
:::

Create and display a modal alert dialog on a Flet page.

Constructs an AlertDialog with title, content, and action buttons,
then opens it as a modal overlay. Provides a default OK button if
no actions specified.

## Purpose

- Display modal dialogs for alerts, confirmations, forms
        - Provide standard dialog structure (title, content, actions)
        - Auto-generate close handlers for convenience
        - Block page interaction until dialog dismissed

## Parameters

- **`page`** (ft.Page): Flet page instance where dialog will be displayed. Must be active and rendered.
- **`title`** (str): Dialog title text displayed in header. Should be concise and descriptive. Examples: "Confirm Delete", "Error", "Assignment Details".
- **`content`** (ft.Control): Main content control displayed in dialog body. Can be any Flet control (Text, Column, Container, etc.). Examples: ft.Text("Are you sure?"), ft.Column([...])
- **`actions`** (list[ft.Control], optional): List of action button controls for dialog footer. Typically TextButton or ElevatedButton. If None, single OK button auto-generated with close handler. Defaults to None.

## Returns

**Type**: `ft.AlertDialog`

            can store reference for programmatic closing or modification.

## Algorithm

- 1. **Define Close Handler**:
- a. Create inner function close_dialog_handler(e)
- b. Implementation:
  - i. Set dialog.open = False
  - ii. Call page.update()
  - iii. Dialog closes and page interaction restored

- 2. **Create Dialog**:
- a. Instantiate ft.AlertDialog
- b. Set title to ft.Text(title)
- c. Set content to provided content control
- d. Set actions to provided list or default OK button:
  - i. If actions is None:
    - - Create [ft.TextButton("OK", on_click=close_dialog_handler)]
  - ii. Otherwise use provided actions list

- 3. **Show Dialog**:
- a. Assign dialog to page.dialog
- b. Set dialog.open = True
- c. Call page.update()
- d. Dialog appears as modal overlay

- 4. **Return Dialog**:
- a. Return dialog instance for reference

## Interactions

- **ft.AlertDialog**: Creates modal dialog component
- **ft.Text**: Dialog title content
- **ft.TextButton**: Default OK button
- **ft.Page**: Displays and updates dialog

## Example

```python
# Simple alert
dialog = create_dialog(
    page=page,
    title="Success",
    content=ft.Text("File saved successfully!")
    )
# Dialog shown with OK button (auto-closes)

# Confirmation dialog with custom actions
def handle_confirm(e):
    delete_file()
    dialog.open = False
    page.update()

dialog = create_dialog(
    page=page,
    title="Confirm Delete",
    content=ft.Text("Are you sure you want to delete this file?"),
    actions=[
    ft.TextButton("Cancel", on_click=lambda e: close_dialog(e)),
    ft.ElevatedButton("Delete", on_click=handle_confirm)
    ]
    )

# Dialog with complex content
content = ft.Column([
    ft.Text("Assignment Details"),
    ft.TextField(label="Title"),
    ft.TextField(label="Description", multiline=True)
    ])
dialog = create_dialog(page, "Edit Assignment", content)
```

## See Also

- `show_snackbar()`: Alternative for brief notifications
- `ft.AlertDialog`: Flet alert dialog component

## Notes

- Dialog is modal (blocks page interaction)
- Auto-generates OK button if no actions provided
- OK button includes auto-generated close handler
- Custom actions must handle closing explicitly
- Dialog attached to page.dialog (single dialog at a time)
- Returns dialog instance for programmatic control
- Content can be any Flet control (text, forms, etc.)
