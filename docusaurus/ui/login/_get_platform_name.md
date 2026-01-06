---
id: "_get_platform_name"
sidebar_position: 5
title: "_get_platform_name"
---

# ⚙️ _get_platform_name

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`login.py`](./login.py) | **Line:** 385
:::

Retrieve human-readable name of the current platform.

Maps Flet's platform enumeration values to user-friendly display
names for showing in the login interface. Helps users confirm
they're on the correct device/platform.

## Returns

**Type**: `str`

                platforms (e.g., 'Windows', 'Android', 'macOS') or string
                representation of platform enum for unknown platforms.

## Algorithm

- **Phase 1: Define Platform Mapping**:
  - 1. Create dictionary mapping ft.PagePlatform enums to strings
  - 2. Define mappings:
    - a. WINDOWS -> "Windows"
    - b. LINUX -> "Linux"
    - c. MACOS -> "macOS"
    - d. ANDROID -> "Android"
    - e. IOS -> "iOS"
  - 3. Store mappings in platform_map variable

- **Phase 2: Lookup Current Platform**:
  - 1. Access self.page.platform (Flet PagePlatform enum)
  - 2. Use dict.get() with platform_map
  - 3. If platform exists in map, return mapped string
  - 4. If platform is unknown, return str(self.page.platform)

- **Phase 3: Return Result**:
  - 1. Return human-readable platform name string

## Interactions

- **ft.Page**: Reads platform property for device detection
- **ft.PagePlatform**: Enum values for different platforms

## Example

```python
# On Windows desktop
login._get_platform_name()
# 'Windows'

# On Android device
login._get_platform_name()
# 'Android'

# On macOS
login._get_platform_name()
# 'macOS'

# On unknown/future platform
login._get_platform_name()
# 'PagePlatform.NEW_PLATFORM'
```

## See Also

- `_build_ui()`: Uses this for platform display text
- `ft.PagePlatform`: Flet platform enumeration

## Notes

- Called during UI construction to display platform info
- Provides user confirmation of correct device/platform
- Gracefully handles unknown platforms with string conversion
- Platform detection automatic via Flet framework
- No external API calls or complex detection logic needed
