---
id: "_show_snackbar"
sidebar_position: 18
title: "_show_snackbar"
---

# ⚙️ _show_snackbar

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`file_preview_service.py`](./file_preview_service.py) | **Line:** 1626
:::

Display temporary feedback message at bottom of screen.

Shows transient notification for user actions (downloads, errors).
Auto-dismisses after brief period.

## Parameters

- **`message`** (str): Feedback text to display. Should be concise. Examples: "✓ Downloaded to: file.pdf", "✗ Download failed: ..."
- **`color`** (ft.Colors): Background color for message type indication. GREEN for success, RED for errors, BLUE for info.

## Returns

**Type**: `None`


## Algorithm

- 1. **Create Snackbar**:
    - a. Instantiate ft.SnackBar
    - b. Set content: ft.Text(message)
    - c. Set bgcolor: color parameter

  - 2. **Show Snackbar**:
    - a. Assign to page.snack_bar
    - b. Set open = True
    - c. Call page.update()

## Interactions

- **ft.SnackBar**: Notification component
- **page.update()**: Renders snackbar

## Example

```python
# Success message
preview_service._show_snackbar(
    "✓ Downloaded successfully",
    ft.Colors.GREEN
    )

# Error message
preview_service._show_snackbar(
    "✗ Operation failed",
    ft.Colors.RED
    )
```

## See Also

- `_download_file()`: Uses for feedback
- `ft.SnackBar`: Flet snackbar component

## Notes

- Appears at bottom of screen
- Auto-dismisses after few seconds
- Color coding for message type
- Non-blocking (doesn't pause)
- Only one snackbar at a time
