---
id: "buttonwithmenu"
sidebar_position: 2
title: "ButtonWithMenu"
---

# 📦 ButtonWithMenu

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Completeness](https://img.shields.io/badge/Docs-20%25-red)

:::info Source
**File:** [`custom_controls.py`](./custom_controls.py) | **Line:** 12
:::

Custom dropdown button styled as an elevated button with hover animations.

ButtonWithMenu extends Flet's PopupMenuButton to create a visually enhanced
dropdown control that resembles a standard ElevatedButton. It features smooth
hover animations (shadow expansion and scale effects), consistent styling with
primary theme colors, and simplified menu item handling through callbacks.
This component bridges the gap between Flet's functional PopupMenuButton and
the visual design language of ElevatedButton, providing a dropdown that feels
cohesive with other button components while maintaining the menu functionality.
It's particularly useful for action buttons that offer multiple related options
(e.g., "Download as... → PDF/DOCX/TXT").

## Purpose

- Provide dropdown button with ElevatedButton appearance
        - Support hover animations (shadow and scale effects)
        - Simplify menu item selection with callback pattern
        - Maintain consistent button styling across application
        - Enable dynamic menu content through item list
        - Provide visual feedback for user interactions

## Attributes

- **`page`** (ft.Page or None): Flet page instance for UI updates. Used for manual page updates if needed. May be None if updates handled elsewhere. Not currently used in implementation but available.
- **`on_menu_select`** (Callable or None): Callback function invoked when user selects menu item. Signature: (item_text: str) -> None. Receives the text of selected menu item. None if no callback registered.
- **`button_content`** (ft.Container): Styled container wrapping button visual. Contains Row with text label and dropdown arrow icon. Manages shadow, scale, and animation properties. Updated on hover events.

## Interactions

- **ft.PopupMenuButton**: Parent class providing menu functionality
- **ft.Container**: Button visual container with styling
- **ft.Row**: Layout for text and icon
- **ft.Text**: Button label display
- **ft.Icon**: Dropdown arrow indicator
- **ft.PopupMenuItem**: Menu item controls
- **ft.BoxShadow**: Shadow effects for depth
- **ft.Animation**: Smooth transitions
- Algorithm (High-Level Workflow):
- *Phase 1: Initialization**
- 1. Store page reference (optional)
- 2. Convert menu_items strings to PopupMenuItem objects
- 3. Create styled button_content Container:
- a. Build Row with label text and dropdown icon
- b. Apply PRIMARY bgcolor and padding
- c. Add initial BoxShadow for depth
- d. Configure animation for smooth transitions
- e. Register hover event handler
- 4. Call parent PopupMenuButton constructor with button_content
- 5. Store on_menu_select callback reference
- *Phase 2: Hover Animation** (_on_hover)
- 1. Check hover state from event data
- 2. If hovering (data == "true"):
- a. Increase shadow blur and spread
- b. Scale button to 1.02 (2% larger)
- 3. If not hovering (data == "false"):
- a. Reset shadow to default
- b. Reset scale to 1.0
- 4. Update button_content to render changes
- *Phase 3: Menu Selection** (_handle_menu_click)
- 1. Extract selected item text from event
- 2. Log selection for debugging
- 3. Check if callback registered
- 4. Invoke on_menu_select with item text

## Example

```python
# Create dropdown button for file export
def handle_export(format_type):
    print(f"Exporting as {format_type}")
    # Export logic here

export_button = ButtonWithMenu(
    text="Export File",
    menu_items=["PDF", "DOCX", "TXT", "CSV"],
    on_menu_select=handle_export,
    page=page
    )
page.add(export_button)

# User clicks button → menu appears
# User selects "PDF" → handle_export("PDF") called

# Without callback
simple_menu = ButtonWithMenu(
    text="Options",
    menu_items=["Option 1", "Option 2", "Option 3"]
    )
# Menu works but no action on selection

# With hover effects
# User hovers → shadow increases, button scales to 102%
# User moves away → shadow and scale reset
```

## See Also

- `ft.PopupMenuButton`: Parent Flet class
- `ft.ElevatedButton`: Standard button for comparison
- `ft.Container`: Container styling reference
- `ft.PopupMenuItem`: Menu item class

## Notes

- Extends ft.PopupMenuButton (inherits menu behavior)
- Styled to match ElevatedButton appearance
- Hover animations enhance user feedback
- Primary color from theme (adaptive)
- Arrow icon indicates dropdown functionality
- Callback receives string (item text)
- Menu opens on click automatically (parent behavior)
- Animation duration: 100ms with ease-in-out curve
- Scale effect: 1.0 (normal) to 1.02 (hover)
- Shadow increases on hover (visual depth)
- Page reference optional (not used in current implementation)

## References

- Flet PopupMenuButton: [https://flet.dev/docs/controls/popupmenubutton](https://flet.dev/docs/controls/popupmenubutton)
- Material Design Buttons: [https://m3.material.io/components/buttons](https://m3.material.io/components/buttons)
- Animation Curves: [https://api.flutter.dev/flutter/animation/Curves-class.html](https://api.flutter.dev/flutter/animation/Curves-class.html)
