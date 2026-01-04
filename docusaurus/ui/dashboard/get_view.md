---
id: "get_view"
sidebar_position: 12
title: "get_view"
---

# ⚙️ get_view

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`dashboard.py`](./dashboard.py) | **Line:** 1005
:::

Build and return the complete dashboard layout.

Constructs the full dashboard user interface including sidebar,
top bar with search, tab navigation, and main content area.
Assembles all components into a responsive layout that adapts
to different screen sizes.

## Returns

**Type**: `ft.Row`

                Structure: Row[sidebar_container, VerticalDivider, main_content]
                where main_content is Column[top_bar, tabs, folder_list].
                Component expands to fill available space with expand=True.

## Algorithm

- **Phase 1: Create Sidebar Container**:
  - 1. Instantiate ft.Container with fixed width=170px
  - 2. Set bgcolor to light grey (ft.Colors.GREY_100)
  - 3. Add padding=20 for internal spacing
  - 4. Calculate visibility:
    - a. visible = (page.width &gt;= 900) OR menu_open
    - b. Shows on desktop or when toggled on mobile
  - 5. Create Column content with four buttons:
    - a. ButtonWithMenu: "+ NEW" with dropdown menu
    - - Menu items: ["Create Folder", "Upload File"]
    - - on_menu_select: self.handle_action
    - b. ElevatedButton: "SETTINGS" (no-op currently)
    - c. ElevatedButton: "TO-DO" with self.show_todo_view
    - d. ElevatedButton: "ACCOUNT" with self.handle_logout
  - 6. Set button spacing=15 in Column
  - 7. Store in self.sidebar_container

- **Phase 2: Create Top Bar**:
  - 1. Instantiate ft.Container with padding=20
  - 2. Create Row content with three elements:
    - a. IconButton: hamburger menu (ft.Icons.MENU)
    - a. on_click: self.toggle_menu
    - b. visible: True (always shown)
    - b. self.search_field: search TextField (expands)
    - c. IconButton: account circle (ft.Icons.ACCOUNT_CIRCLE)
    - a. icon_size: 36
    - b. tooltip: self.user_email
  - 3. Set Row alignment to SPACE_BETWEEN
  - 4. Store in top_bar variable

- **Phase 3: Create Tab Navigation**:
  - 1. Instantiate ft.Container with padding=10
  - 2. Create Row content with three tab buttons:
    - a. ElevatedButton: "YOUR FOLDERS"
    - a. on_click: folder_navigator.reset_to_root()
    - b. ElevatedButton: "PASTE LINKS"
    - b. on_click: paste_links_manager.load_paste_links_view()
    - c. ElevatedButton: "SHARED DRIVES"
    - a. on_click: folder_navigator.load_shared_drives()
  - 3. Set Row spacing=10, alignment=CENTER
  - 4. Store in tabs variable

- **Phase 4: Create Main Content Area**:
  - 1. Instantiate ft.Column with three components:
    - a. top_bar: search and account controls
    - b. tabs: view switching buttons
    - c. Container with folder_list (expand=True)
  - 2. Set Column expand=True to fill vertical space
  - 3. Store in main_content variable

- **Assemble Final Layout**:
  - 1. Create ft.Row with three components:
    - a. self.sidebar_container: navigation sidebar
    - b. ft.VerticalDivider(width=1): separator line
    - c. main_content: main display area
  - 2. Set Row expand=True to fill available space
  - 3. Return assembled Row component

## Interactions

- **ButtonWithMenu**: Custom dropdown for action menu
- **FileManager**: Handles menu action selections
- **FolderNavigator**: Handles tab navigation and search
- **PasteLinksManager**: Handles paste links view
- **TodoView**: Loaded when TO-DO button clicked

## Example

```python
# Initialize dashboard
dashboard = Dashboard(page, auth, logout_handler)

# Get complete layout
layout = dashboard.get_view()
print(type(layout))
# <class 'flet.Row'>

# Add to page for rendering
page.add(layout)
page.update()
# Full dashboard now visible with all components
```

## See Also

- `__init__()`: Initializes components used in layout
- `ButtonWithMenu`: Dropdown button
- `show_todo_view()`: TO-DO button click handler
- `handle_logout()`: ACCOUNT button click handler
- `handle_action()`: Menu selection handler

## Notes

- Layout is responsive with 900px breakpoint
- Sidebar hides on mobile, toggled by hamburger menu
- Tab buttons switch between different view modes
- Search field expands to fill available width
- folder_list populated dynamically based on view
- VerticalDivider provides visual separation
- All components configured before return
- expand=True ensures full viewport usage
