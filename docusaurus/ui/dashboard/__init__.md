---
id: "__init__"
sidebar_position: 3
title: "__init__"
---

# 🔧 __init__

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`dashboard.py`](./dashboard.py) | **Line:** 202
:::

Initialize the Dashboard with authentication and layout setup.

Constructs the main dashboard by setting up Google Drive integration,
initializing manager modules, creating UI components, and loading the
default folder view. Establishes the foundation for all dashboard
functionality including file management, navigation, and responsive layout.

## Parameters

- **`page`** (ft.Page): Flet page instance providing UI rendering context, window dimensions, overlay system, and event handling. Must be a valid, initialized Flet page object.
- **`auth_service`** (GoogleAuth): Authentication service managing OAuth2 credentials, user session, and Drive API access. Must be authenticated before Dashboard initialization.
- **`on_logout`** (Callable): Callback function with no parameters, invoked when user clicks logout button. Typically handles cleanup and navigation to login screen. Signature: () -> None.

## Algorithm

- **Phase 1: Store Core References**:
  - 1. Assign page parameter to self.page
  - 2. Assign auth_service to self.auth
  - 3. Assign on_logout callback to self.on_logout

- **Phase 2: Initialize Drive Service**:
  - 1. Call auth_service.get_service() to obtain Drive API service
  - 2. Pass service to DriveService constructor
  - 3. Store DriveService instance in self.drive

- **Phase 3: Setup Navigation State**:
  - 1. Set self.current_folder_id to "root" (Drive root folder)
  - 2. Set self.current_folder_name to "My Drive"
  - 3. Initialize self.folder_stack as empty list []
  - 4. Set self.current_view to "your_folders" (default view)

- **Phase 4: Retrieve User Information**:
  - 1. Call auth.get_user_info() to get user profile data
  - 2. Extract emailAddress from user_info dictionary
  - 3. Store in self.user_email (default to "User" if unavailable)

- **Phase 5: Instantiate Manager Modules**:
  - 1. Create FileManager instance: FileManager(self)
    - a. Passes self reference for access to page, drive, etc.
  - 2. Create FolderNavigator instance: FolderNavigator(self)
    - b. Handles navigation and folder content display
  - 3. Create PasteLinksManager instance: PasteLinksManager(self)
    - c. Processes shared Drive links

- **Phase 6: Create Search Field Component**:
  - 1. Instantiate ft.TextField with hint_text "Search"
  - 2. Set prefix_icon to ft.Icons.SEARCH (magnifying glass)
  - 3. Bind on_submit event to folder_navigator.handle_search
  - 4. Configure styling: border_color, filled=True, expand=True
  - 5. Store in self.search_field

- **Phase 7: Initialize Menu State**:
  - 1. Set self.menu_open to False (sidebar hidden on mobile initially)

- **Phase 8: Create Paste Link Field Component**:
  - 1. Instantiate ft.TextField with paste instruction hint text
  - 2. Bind on_submit to paste_links_manager.handle_paste_link
  - 3. Configure styling: expand=True, blue border colors
  - 4. Store in self.paste_link_field

- **Phase 9: Create Folder List Container**:
  - 1. Instantiate ft.Column with spacing=0
  - 2. Set scroll mode to ALWAYS for scrollable content
  - 3. Set expand=True to fill available vertical space
  - 4. Store in self.folder_list

- **Phase 10: Register Resize Handler**:
  - 1. Bind self.on_resize to page.on_resize event
  - 2. Enables responsive sidebar visibility on window resize

- **Phase 11: Configure Page Properties**:
  - 1. Set page.title to "Drive Manager"
  - 2. Set vertical_alignment to MainAxisAlignment.START
  - 3. Set horizontal_alignment to CrossAxisAlignment.STRETCH

- **Phase 12: Load Initial View**:
  - 1. Call folder_navigator.load_your_folders()
  - 2. Displays root folder contents in folder_list
  - 3. Dashboard now ready for user interaction

## Interactions

- **GoogleAuth**: Retrieves Drive API service and user information
- **DriveService**: Initialized with Drive API service for file ops
- **FileManager**: Instantiated with dashboard reference
- **FolderNavigator**: Instantiated and called to load initial view
- **PasteLinksManager**: Instantiated with dashboard reference
- **ft.Page**: Configured with title, alignment, and resize handler

## Example

```python
# Create dashboard after user authentication
auth = GoogleAuth()
auth.authenticate()  # User logs in via OAuth2

def handle_logout():
    page.clean()
    show_login_screen()

dashboard = Dashboard(page, auth, handle_logout)
# Dashboard now displays root folder contents

# Access dashboard components
print(dashboard.user_email)
# user@example.com
print(dashboard.current_folder_name)
# My Drive
print(len(dashboard.folder_stack))
# 0
```

## See Also

- `GoogleAuth`: Authentication service
- `DriveService`: Drive API wrapper
- `FileManager`: File operations
- `FolderNavigator`: Navigation
- `get_view()`: Builds and returns dashboard layout

## Notes

- Auth service must be authenticated before initialization
- Initial view loads "root" folder (My Drive) automatically
- Sidebar visibility initially based on window width
- Manager modules receive self reference for accessing dashboard state
- Page resize handler registered for responsive behavior
- User email extracted safely with fallback to "User"
