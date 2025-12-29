---
id: "__init__"
sidebar_position: 3
title: "__init__"
---

# 🔧 __init__

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`folder_navigator.py`](./folder_navigator.py) | **Line:** 179
:::

Initialize FolderNavigator with Dashboard reference.

Sets up navigator with access to Dashboard state and services.
Navigation state stored in Dashboard for accessibility across modules.

## Parameters

- **`dashboard`** (Dashboard): Parent Dashboard instance providing access to: - current_view: View context string - current_folder_id: Active folder ID - current_folder_name: Active folder display name - folder_stack: History stack for back navigation - folder_list: UI control for displaying items - drive: DriveService instance - file_manager: FileManager instance - page: Flet page for updates

## Algorithm

- 1. **Store Dashboard Reference**:
    - a. Assign dashboard parameter to self.dash
    - b. All navigation state accessed via dash
    - c. Services accessed via dash.drive, dash.file_manager

## Interactions

- **Dashboard**: Stores reference for state and service access

## Example

```python
# Initialization during Dashboard setup
dashboard = Dashboard(page, auth_service)
navigator = FolderNavigator(dashboard)
# Navigator ready to manage folder navigation

# Access Dashboard state
current_folder = navigator.dash.current_folder_id
print(current_folder)
# root
```

## See Also

- `Dashboard`: Parent container
- `load_your_folders()`: Initial view loading

## Notes

- Single Dashboard reference for all operations
- Navigation state in Dashboard (not navigator)
- No initialization of state here (Dashboard handles)
- Lightweight initialization (just reference storage)
