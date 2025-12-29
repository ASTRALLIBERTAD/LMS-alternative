---
id: "_on_hover"
sidebar_position: 4
title: "_on_hover"
---

# ⚙️ _on_hover

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`custom_controls.py`](./custom_controls.py) | **Line:** 307
:::

Handle hover events to animate button appearance with shadow and scale.

Updates button visual state when user hovers or moves away. Increases
shadow depth and scales button slightly larger on hover, then resets
to default state on mouse leave. Provides visual feedback for interaction.

## Parameters

- **`e`** (ft.ControlEvent): Hover event from Flet framework. Contains data property with string value: "true" when mouse enters hover area, "false" when mouse leaves. Event source is button_content container.

## Returns

**Type**: `None`


## Algorithm

- 1. **Check Hover State**:
    - a. Access e.data property (string: "true" or "false")
    - b. Compare: if e.data == "true"

  - 2. **Apply Hover Effects** (if hovering):
    - a. Update button_content.shadow:
    - i. spread_radius: 0 (no spread)
    - ii. blur_radius: 8px (increased from 2px)
    - iii. color: BLACK with 40% opacity (darker)
    - iv. offset: (0, 2) - more downward shadow
    - b. Update button_content.scale:
    - i. Set to 1.02 (2% larger)
    - ii. Creates subtle growth effect

  - 3. **Reset to Default** (if not hovering):
    - a. Update button_content.shadow:
    - i. spread_radius: 0
    - ii. blur_radius: 2px (original)
    - iii. color: BLACK with 30% opacity (lighter)
    - iv. offset: (0, 1) - subtle shadow
    - b. Update button_content.scale:
    - i. Set to 1.0 (normal size)

  - 4. **Apply Changes**:
    - a. Call button_content.update()
    - b. Triggers re-render with new properties
    - c. Animation makes transition smooth (100ms ease-in-out)

## Interactions

- **ft.ControlEvent**: Provides hover state data
- **ft.BoxShadow**: Shadow effect modification
- **button_content.update()**: Renders changes

## Example

```python
# User interaction flow:
# 1. Mouse enters button area
# → e.data = "true"
# → Shadow increases (blur: 2→8, opacity: 0.3→0.4)
# → Button scales to 102%
# → Smooth animation over 100ms

# 2. Mouse leaves button area
# → e.data = "false"
# → Shadow decreases (blur: 8→2, opacity: 0.4→0.3)
# → Button scales to 100%
# → Smooth animation over 100ms
```

## See Also

- `__init__()`: Registers this as hover handler
- `ft.BoxShadow`: Shadow configuration
- `ft.Animation`: Smooth transition

## Notes

- Called automatically by Flet on hover events
- e.data is string, not boolean
- Animation configured in __init__ (100ms, ease-in-out)
- Shadow changes create depth perception
- Scale change subtle but noticeable (2%)
- Update triggers smooth transition
- Hover effects standard for modern UI
- Shadow offset increases on hover (1→2)
- Opacity increases on hover (0.3→0.4)
