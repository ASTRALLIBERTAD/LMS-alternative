"""Dashboard UI Module.

This module provides the main dashboard interface for the LMS application,
integrating file management, folder navigation, and to-do functionality.

Classes:
    Dashboard: Main application dashboard with Drive integration.

See Also:
    :class:`~src.services.drive_service.DriveService`: Drive API wrapper.
    :class:`~src.ui.todo_view.TodoView`: Assignment management view.
"""

import flet as ft
from services.drive_service import DriveService
from utils.common import show_snackbar
from ui.custom_control.custom_controls import ButtonWithMenu
from ui.custom_control.gmail_profile_menu import GmailProfileMenu
from ui.custom_control.multi_account_manager import MultiAccountManager
from ui.todo_view import TodoView
from ui.dashboard_modules.file_manager import FileManager
from ui.dashboard_modules.folder_navigator import FolderNavigator
from ui.dashboard_modules.paste_links_manager import PasteLinksManager


class Dashboard:
    """Main application dashboard with Google Drive integration and file management.

    The Dashboard class serves as the central hub of the Learning Management System,
    providing a unified interface for Google Drive file operations, folder navigation,
    assignment management (to-do), and link-based access to shared resources. It
    orchestrates multiple specialized manager modules and handles responsive layout
    adjustments for various screen sizes.
    
    This class acts as the coordinator between the UI layer and backend services,
    managing the overall application state including current folder context, view
    modes (folders vs to-do), and user session information. It implements a sidebar
    navigation system with context-aware content display and supports both direct
    Drive folder browsing and paste-link-based access.

    Purpose:
        - Provide main dashboard interface for LMS file management
        - Integrate Google Drive operations with user-friendly UI
        - Coordinate between file management, navigation, and assignment modules
        - Handle responsive layout for desktop and mobile viewports
        - Manage application view states (folder view, to-do view, paste links)
        - Support both authenticated Drive access and link-based sharing

    Attributes:
        page (ft.Page): Flet page instance for UI rendering and event handling.
            Provides access to window dimensions, overlay system, and update mechanism.
        auth (GoogleAuth): Authentication service managing OAuth2 credentials
            and user session. Provides access to Drive API service and user info.
        on_logout (Callable): Callback function invoked when user logs out.
            Typically returns user to login screen or clears session data.
        drive (DriveService): Google Drive service wrapper providing high-level
            API methods for file/folder operations, metadata queries, and permissions.
        current_folder_id (str): Google Drive ID of currently displayed folder.
            Default is "root" representing user's My Drive root folder.
        current_folder_name (str): Display name of currently active folder.
            Used in breadcrumb navigation and title displays. Default "My Drive".
        folder_stack (list): Navigation history stack storing folder IDs for
            back navigation. Enables breadcrumb trail and "go up" functionality.
        current_view (str): Active view mode identifier. Values: "your_folders"
            (default Drive view), "todo" (assignment management), "paste_links"
            (link-based access), "shared_drives" (team drive view).
        user_email (str): Email address of authenticated user. Retrieved from
            auth service user info. Displayed in account tooltip. Default "User".
        file_manager (FileManager): Module handling file operations including
            upload, download, delete, rename, and folder creation. Manages file
            picker dialogs and progress indicators.
        folder_navigator (FolderNavigator): Module managing folder traversal,
            search functionality, and view switching between folder types.
            Handles breadcrumb generation and folder content loading.
        paste_links_manager (PasteLinksManager): Module processing Google Drive
            share links, extracting file/folder IDs, and displaying linked content
            without requiring direct Drive permissions.
        search_field (ft.TextField): Search input component with magnifying glass
            icon. Triggers folder_navigator.handle_search on submit (Enter key).
        menu_open (bool): Sidebar visibility state for mobile/tablet viewports.
            Toggled by hamburger menu button. Always visible on desktop (>900px).
        paste_link_field (ft.TextField): Input field for pasting Google Drive
            share links. Processes links on Enter key via paste_links_manager.
        folder_list (ft.Column): Main content container displaying folder contents,
            search results, or to-do view. Scrollable with dynamic content updates.

    Interactions:
        - **GoogleAuth**: Authenticates user and provides Drive API service
        - **DriveService**: Wraps Google Drive API for file/folder operations
        - **FileManager**: Handles file uploads, downloads, and folder creation
        - **FolderNavigator**: Manages navigation, search, and folder content display
        - **PasteLinksManager**: Processes shared Drive links and displays content
        - **TodoView**: Assignment management interface accessible from sidebar
        - **ButtonWithMenu**: Custom dropdown button component for action menu
        - **ft.Page**: Flet page for UI updates and responsive layout handling

    Algorithm:
        **Phase 1: Initialization**
            1. Store references to page, auth service, and logout callback
            2. Create DriveService instance from auth.get_service()
            3. Initialize folder navigation state (root folder, empty stack)
            4. Set default view mode to "your_folders"
            5. Retrieve user email from auth service for display
            6. Instantiate manager modules (FileManager, FolderNavigator, PasteLinksManager)
            7. Create search field with submit handler
            8. Create paste link field for shared link processing
            9. Create scrollable folder list container
            10. Register resize event handler for responsive layout
            11. Set page title and alignment properties
            12. Trigger initial folder load (your_folders view)
        
        **Phase 2: View Management**
            1. Monitor current_view state variable
            2. When view changes:
               a. Clear folder_list contents
               b. If "your_folders": load Drive root folder contents
               c. If "todo": instantiate TodoView and display
               d. If "paste_links": show paste link input interface
               e. If "shared_drives": load team drives list
            3. Update page to render new view
        
        **Phase 3: Responsive Layout Handling**
            1. Listen for window resize events via page.on_resize
            2. Check page.width against breakpoints
            3. If width >= 900px (desktop):
               a. Show sidebar permanently
               b. Set menu_open to False (disable toggle state)
            4. If width < 900px (mobile/tablet):
               a. Show sidebar only if menu_open is True
               b. Enable hamburger menu toggle functionality
            5. Update page to apply visibility changes
        
        **Phase 4: Navigation Flow**
            1. User clicks folder in folder_list
            2. Delegate to folder_navigator.show_folder_contents()
            3. Push current folder to folder_stack for back navigation
            4. Update current_folder_id and current_folder_name
            5. Load and display new folder contents
            6. Update breadcrumb trail in UI
        
        **Phase 5: Action Handling**
            1. User clicks action button (+ NEW, TO-DO, SETTINGS, etc.)
            2. Route to appropriate handler method
            3. For file operations: delegate to file_manager
            4. For navigation: delegate to folder_navigator
            5. For view switches: update current_view and rebuild UI
            6. Update page to reflect changes

    Example:
        >>> # Initialize dashboard with auth service
        >>> from services.google_auth import GoogleAuth
        >>> auth = GoogleAuth()
        >>> def logout_handler():
        ...     print("User logged out")
        >>> 
        >>> dashboard = Dashboard(page, auth, logout_handler)
        >>> 
        >>> # Dashboard automatically loads root folder
        >>> print(f"Current folder: {dashboard.current_folder_name}")
        Current folder: My Drive
        >>> 
        >>> # User navigates to subfolder
        >>> dashboard.show_folder_contents('folder_abc123', 'Documents')
        >>> print(f"Current folder: {dashboard.current_folder_name}")
        Current folder: Documents
        >>> 
        >>> # User switches to to-do view
        >>> dashboard.show_todo_view(None)
        >>> print(f"Current view: {dashboard.current_view}")
        Current view: todo
        >>> 
        >>> # Get dashboard layout for rendering
        >>> layout = dashboard.get_view()
        >>> page.add(layout)

    See Also:
        - :class:`~services.drive_service.DriveService`: Google Drive API wrapper
        - :class:`~services.google_auth.GoogleAuth`: Authentication service
        - :class:`~ui.todo_view.TodoView`: Assignment management interface
        - :class:`~ui.dashboard_modules.file_manager.FileManager`: File operations
        - :class:`~ui.dashboard_modules.folder_navigator.FolderNavigator`: Navigation
        - :class:`~ui.dashboard_modules.paste_links_manager.PasteLinksManager`: Link handling
        - :class:`~ui.custom_control.custom_controls.ButtonWithMenu`: Dropdown button
        - :mod:`flet`: Flet UI framework documentation

    Notes:
        - Sidebar automatically hides on mobile (<900px width) with toggle button
        - All file operations delegated to specialized manager modules
        - View state persists until explicitly changed by user action
        - Folder navigation maintains history stack for back button functionality
        - User email displayed in account icon tooltip for easy identification
        - Search functionality scans current folder and subfolders recursively
        - Paste links allow access without direct Drive permissions

    References:
        - Google Drive API v3: https://developers.google.com/drive/api/v3/reference
        - Flet Framework: https://flet.dev/docs/
        - Material Design Icons: https://fonts.google.com/icons
    """

    def __init__(self, page, auth_service, on_logout, on_add_account=None, on_switch_account=None):
        """Initialize the Dashboard with authentication and layout setup.

        Constructs the main dashboard by setting up Google Drive integration,
        initializing manager modules, creating UI components, and loading the
        default folder view. Establishes the foundation for all dashboard
        functionality including file management, navigation, and responsive layout.

        Args:
            page (ft.Page): Flet page instance providing UI rendering context,
                window dimensions, overlay system, and event handling. Must be
                a valid, initialized Flet page object.
            auth_service (GoogleAuth): Authentication service managing OAuth2
                credentials, user session, and Drive API access. Must be
                authenticated before Dashboard initialization.
            on_logout (Callable): Callback function with no parameters, invoked
                when user clicks logout button. Typically handles cleanup and
                navigation to login screen. Signature: () -> None.

        Algorithm:
            **Phase 1: Store Core References**:
               1. Assign page parameter to self.page
               2. Assign auth_service to self.auth
               3. Assign on_logout callback to self.on_logout

            **Phase 2: Initialize Drive Service**:
               1. Call auth_service.get_service() to obtain Drive API service
               2. Pass service to DriveService constructor
               3. Store DriveService instance in self.drive

            **Phase 3: Setup Navigation State**:
               1. Set self.current_folder_id to "root" (Drive root folder)
               2. Set self.current_folder_name to "My Drive"
               3. Initialize self.folder_stack as empty list []
               4. Set self.current_view to "your_folders" (default view)

            **Phase 4: Retrieve User Information**:
               1. Call auth.get_user_info() to get user profile data
               2. Extract emailAddress from user_info dictionary
               3. Store in self.user_email (default to "User" if unavailable)

            **Phase 5: Instantiate Manager Modules**:
               1. Create FileManager instance: FileManager(self)
                    a. Passes self reference for access to page, drive, etc.
               2. Create FolderNavigator instance: FolderNavigator(self)
                    b. Handles navigation and folder content display
               3. Create PasteLinksManager instance: PasteLinksManager(self)
                    c. Processes shared Drive links

            **Phase 6: Create Search Field Component**:
               1. Instantiate ft.TextField with hint_text "Search"
               2. Set prefix_icon to ft.Icons.SEARCH (magnifying glass)
               3. Bind on_submit event to folder_navigator.handle_search
               4. Configure styling: border_color, filled=True, expand=True
               5. Store in self.search_field

            **Phase 7: Initialize Menu State**:
               1. Set self.menu_open to False (sidebar hidden on mobile initially)

            **Phase 8: Create Paste Link Field Component**:
               1. Instantiate ft.TextField with paste instruction hint text
               2. Bind on_submit to paste_links_manager.handle_paste_link
               3. Configure styling: expand=True, blue border colors
               4. Store in self.paste_link_field

            **Phase 9: Create Folder List Container**:
               1. Instantiate ft.Column with spacing=0
               2. Set scroll mode to ALWAYS for scrollable content
               3. Set expand=True to fill available vertical space
               4. Store in self.folder_list

            **Phase 10: Register Resize Handler**:
                1. Bind self.on_resize to page.on_resize event
                2. Enables responsive sidebar visibility on window resize

            **Phase 11: Configure Page Properties**:
                1. Set page.title to "Drive Manager"
                2. Set vertical_alignment to MainAxisAlignment.START
                3. Set horizontal_alignment to CrossAxisAlignment.STRETCH

            **Phase 12: Load Initial View**:
                1. Call folder_navigator.load_your_folders()
                2. Displays root folder contents in folder_list
                3. Dashboard now ready for user interaction

        Interactions:
            - **GoogleAuth**: Retrieves Drive API service and user information
            - **DriveService**: Initialized with Drive API service for file ops
            - **FileManager**: Instantiated with dashboard reference
            - **FolderNavigator**: Instantiated and called to load initial view
            - **PasteLinksManager**: Instantiated with dashboard reference
            - **ft.Page**: Configured with title, alignment, and resize handler

        Example:
            >>> # Create dashboard after user authentication
            >>> auth = GoogleAuth()
            >>> auth.authenticate()  # User logs in via OAuth2
            >>> 
            >>> def handle_logout():
            ...     page.clean()
            ...     show_login_screen()
            >>> 
            >>> dashboard = Dashboard(page, auth, handle_logout)
            >>> # Dashboard now displays root folder contents
            >>> 
            >>> # Access dashboard components
            >>> print(dashboard.user_email)
            user@example.com
            >>> print(dashboard.current_folder_name)
            My Drive
            >>> print(len(dashboard.folder_stack))
            0

        See Also:
            - :class:`~services.google_auth.GoogleAuth`: Authentication service
            - :class:`~services.drive_service.DriveService`: Drive API wrapper
            - :class:`~ui.dashboard_modules.file_manager.FileManager`: File operations
            - :class:`~ui.dashboard_modules.folder_navigator.FolderNavigator`: Navigation
            - :meth:`get_view`: Builds and returns dashboard layout

        Notes:
            - Auth service must be authenticated before initialization
            - Initial view loads "root" folder (My Drive) automatically
            - Sidebar visibility initially based on window width
            - Manager modules receive self reference for accessing dashboard state
            - Page resize handler registered for responsive behavior
            - User email extracted safely with fallback to "User"
        """

        self.page = page
        self.auth = auth_service
        self.on_logout = on_logout
        self.on_add_account_callback = on_add_account
        self.on_switch_account_callback = on_switch_account
        self.drive = DriveService(auth_service.get_service())

        self.current_folder_id = "root"
        self.current_folder_name = "My Drive"
        self.folder_stack = []
        self.current_view = "your_folders"

        self.account_manager = MultiAccountManager()

        user_info = self.auth.get_user_info()
        self.user_email = user_info.get("emailAddress", "User") if user_info else "User"
        
        if user_info and not user_info.get("name") and not user_info.get("displayName"):
            user_info["name"] = self.user_email.split("@")[0]
        
        self.user_info = user_info if user_info else {
            "name": "User",
            "emailAddress": self.user_email,
            "photoLink": None
        }

        self.file_manager = FileManager(self)
        self.folder_navigator = FolderNavigator(self)
        self.paste_links_manager = PasteLinksManager(self)

        self.search_field = ft.TextField(
            hint_text="Search",
            prefix_icon=ft.Icons.SEARCH,
            on_submit=self.folder_navigator.handle_search,
            border_color=ft.Colors.GREY_400,
            filled=True,
            expand=True,
        )

        self.menu_open = False

        self.paste_link_field = ft.TextField(
            hint_text="Paste Google Drive folder or file link and press Enter",
            on_submit=self.paste_links_manager.handle_paste_link,
            expand=True,
            border_color=ft.Colors.BLUE_400,
            focused_border_color=ft.Colors.BLUE_700,
        )

        self.folder_list = ft.Column(spacing=0, scroll=ft.ScrollMode.ALWAYS, expand=True)

        self.page.on_resize = self.on_resize

        self.page.title = "Drive Manager"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

        self.folder_navigator.load_your_folders()

    def toggle_menu(self, e):
        """Toggle sidebar menu visibility on mobile/tablet devices.

        Switches the sidebar visibility state when the hamburger menu button
        is clicked. Only affects behavior on smaller screens (<900px width)
        where the sidebar is collapsible. On desktop (>=900px), sidebar
        remains permanently visible.

        Args:
            e (ft.ControlEvent): Flet control event from IconButton click.
                Contains event source and related data. Not used in logic
                but required by Flet event handler signature.

        Returns:
            None: Updates UI state and triggers page refresh as side effect.

        Algorithm:
            **Phase 1: Toggle State**:
               1. Read current value of self.menu_open boolean
               2. Invert value: self.menu_open = not self.menu_open
               3. Store new state (True becomes False, False becomes True)

            **Phase 2: Update Sidebar Visibility**:
               1. Calculate visibility condition:
                  a. visible = self.menu_open OR self.page.width > 700
               2. Assign result to self.sidebar_container.visible property
               3. Sidebar shows if: menu toggled on OR window is wide

            **Phase 3: Refresh UI**:
               1. Call self.page.update()
               2. Triggers Flet to re-render affected components
               3. Sidebar appears or disappears with animation

        Interactions:
            - **ft.Page**: Updates page to render visibility changes
            - **sidebar_container**: Visibility property modified based on state
            - **on_resize()**: Complementary method handling window resize events

        Example:
            >>> # User clicks hamburger menu on mobile device
            >>> dashboard.menu_open
            False
            >>> dashboard.toggle_menu(click_event)
            >>> dashboard.menu_open
            True
            >>> dashboard.sidebar_container.visible
            True
            >>> 
            >>> # User clicks again to close
            >>> dashboard.toggle_menu(click_event)
            >>> dashboard.menu_open
            False
            >>> dashboard.sidebar_container.visible
            False
            >>> 
            >>> # On desktop (width > 700), sidebar stays visible
            >>> dashboard.page.width = 1200
            >>> dashboard.menu_open = False
            >>> dashboard.toggle_menu(click_event)
            >>> dashboard.sidebar_container.visible
            True  # Visible due to width, despite menu_open=True

        See Also:
            - :meth:`on_resize`: Handles window resize for responsive layout
            - :meth:`get_view`: Creates sidebar_container with toggle button

        Notes:
            - Event parameter required by Flet but not used in logic
            - Sidebar visibility uses OR logic: menu_open OR wide_screen
            - State persists until next toggle or window resize
            - Animation handled automatically by Flet framework
            - Does not affect desktop layout (width >= 900px)
        """
        self.menu_open = not self.menu_open
        self.sidebar_container.visible = self.menu_open or self.page.width > 700
        self.page.update()

    def on_resize(self, e):
        """Handle window resize events for responsive sidebar layout.

        Adjusts sidebar visibility based on window width breakpoints to
        provide optimal user experience across desktop, tablet, and mobile
        devices. Implements responsive design pattern where sidebar is
        always visible on desktop but collapsible on smaller screens.

        Args:
            e (ft.ControlEvent): Flet control event triggered by window resize.
                Contains new page dimensions. Not directly accessed but
                available for extension. Required by Flet event signature.

        Returns:
            None: Updates UI layout and triggers page refresh as side effect.

        Algorithm:
            **Check Window Width**:
               1. Read self.page.width (current window width in pixels)
               2. Compare against desktop breakpoint (900px)

            **Desktop Layout** (width >= 900px):
               1. If self.page.width >= 900:
                  a. Set self.sidebar_container.visible = True
                  b. Sidebar permanently visible on desktop
                  c. Set self.menu_open = False
                  d. Disable mobile toggle state
               2. Desktop users see sidebar without toggle button
            
            **Mobile/Tablet Layout** (width < 900px):
               1. If self.page.width < 900:
                  a. Set sidebar_container.visible = self.menu_open
                  b. Sidebar shows only if toggle is active
                  c. Hamburger menu button controls visibility
               2. Mobile users can toggle sidebar on/off

            **Refresh UI**:
               1. Call self.page.update()
               2. Apply visibility changes with smooth transition
               3. Re-render affected layout components

        Interactions:
            - **ft.Page**: Reads width property and triggers update
            - **sidebar_container**: Visibility modified based on width
            - **toggle_menu()**: Complementary method for manual toggle

        Example:
            >>> # User resizes from mobile to desktop
            >>> dashboard.page.width = 600  # Mobile width
            >>> dashboard.menu_open = False
            >>> dashboard.on_resize(resize_event)
            >>> dashboard.sidebar_container.visible
            False  # Hidden on mobile when toggle off
            >>> 
            >>> # User expands window to desktop size
            >>> dashboard.page.width = 1200
            >>> dashboard.on_resize(resize_event)
            >>> dashboard.sidebar_container.visible
            True  # Always visible on desktop
            >>> dashboard.menu_open
            False  # Toggle state reset
            >>> 
            >>> # User shrinks back to tablet
            >>> dashboard.page.width = 800
            >>> dashboard.on_resize(resize_event)
            >>> dashboard.sidebar_container.visible
            False  # Hidden again (menu_open still False)

        See Also:
            - :meth:`toggle_menu`: Manual sidebar toggle for mobile users
            - :meth:`__init__`: Registers this handler to page.on_resize
            - :meth:`get_view`: Creates responsive layout structure

        Notes:
            - Breakpoint at 900px chosen for optimal sidebar usability
            - Desktop mode (>=900px) disables toggle state for consistency
            - Mobile mode (<900px) respects user's toggle preference
            - Event triggered automatically by Flet on window dimension changes
            - Provides seamless responsive experience across device types
            - Toggle state only meaningful on mobile/tablet viewports
        """
        if self.page.width >= 900:
            self.sidebar_container.visible = True
            self.menu_open = False
        else:
            self.sidebar_container.visible = self.menu_open
        self.page.update()

    def show_folder_contents(self, folder_id, folder_name=None, is_shared_drive=False, push_to_stack=True):
        """Display contents of a specific Google Drive folder.

        Navigates to a folder and displays its contents in the main view area.
        Delegates actual loading and display logic to the folder_navigator
        module while maintaining a simple interface for external callers.

        Args:
            folder_id (str): Google Drive ID of the folder to display. Must be
                a valid Drive folder ID accessible by authenticated user.
                Example: '1abc...xyz' (33-character alphanumeric string).
            folder_name (str, optional): Display name for the folder, shown in
                breadcrumb navigation and title. If None, name is fetched from
                Drive API. Defaults to None.
            is_shared_drive (bool, optional): Whether this folder is in a shared
                (team) drive rather than user's personal My Drive. Affects
                permission handling and API parameters. Defaults to False.
            push_to_stack (bool, optional): Whether to add current folder to
                navigation history stack for back button functionality. Set to
                False when going backward to prevent stack duplication.
                Defaults to True.

        Returns:
            None: Updates folder_list with new contents as side effect.
                Does not return folder data directly.

        Algorithm:
            **Phase 1: Delegate to FolderNavigator**:
               1. Access self.folder_navigator instance
               2. Call show_folder_contents() method on navigator
               3. Pass all four parameters through unchanged:
                  a. folder_id: target folder identifier
                  b. folder_name: optional display name
                  c. is_shared_drive: team drive flag
                  d. push_to_stack: history tracking flag

            **Phase 2: FolderNavigator Processing** (handled internally):
               1. Update current_folder_id and current_folder_name
               2. Push previous folder to folder_stack if push_to_stack=True
               3. Query Drive API for folder contents
               4. Clear folder_list.controls
               5. Build UI cards for files and subfolders
               6. Populate folder_list with new content
               7. Update breadcrumb navigation trail
               8. Call page.update() to render changes

        Interactions:
            - **FolderNavigator**: Delegates all folder display logic
            - **DriveService**: Navigator uses this to query folder contents
            - **folder_list**: Navigator populates with folder contents
            - **folder_stack**: Navigator manages navigation history

        Example:
            >>> # Navigate to a subfolder from current folder
            >>> dashboard.show_folder_contents(
            ...     'folder_abc123',
            ...     'Documents',
            ...     is_shared_drive=False,
            ...     push_to_stack=True
            ... )
            >>> # folder_list now shows contents of Documents folder
            >>> print(dashboard.current_folder_name)
            Documents
            >>> 
            >>> # Navigate to team drive folder
            >>> dashboard.show_folder_contents(
            ...     'shared_xyz789',
            ...     'Team Projects',
            ...     is_shared_drive=True,
            ...     push_to_stack=True
            ... )
            >>> 
            >>> # Go back without adding to stack
            >>> previous_folder_id = dashboard.folder_stack.pop()
            >>> dashboard.show_folder_contents(
            ...     previous_folder_id,
            ...     push_to_stack=False
            ... )

        See Also:
            - :class:`~ui.dashboard_modules.folder_navigator.FolderNavigator`: Handles logic
            - :meth:`refresh_folder_contents`: Reload current folder
            - :meth:`show_todo_view`: Switch to assignment view

        Notes:
            - This is a convenience wrapper for external callers
            - All folder display logic encapsulated in FolderNavigator
            - folder_name is optional; fetched from API if not provided
            - push_to_stack=False used for back navigation to avoid loops
            - Shared drives require different API parameters (handled internally)
            - Invalid folder_id will result in error from Drive API
        """
        self.folder_navigator.show_folder_contents(folder_id, folder_name, is_shared_drive, push_to_stack)

    def refresh_folder_contents(self):
        """Refresh the currently displayed folder contents.

        Reloads the current folder to reflect any changes made since it was
        last loaded. Useful after file uploads, deletions, renames, or when
        syncing with changes made in other clients or by other users.

        Returns:
            None: Updates folder_list with refreshed contents as side effect.

        Algorithm:
            **Delegate to FolderNavigator**:
               1. Access self.folder_navigator instance
               2. Call refresh_folder_contents() method

            **Navigator Refresh Process** (handled internally):
               1. Read current_folder_id from dashboard state
               2. Query Drive API for latest folder contents
               3. Clear existing folder_list.controls
               4. Rebuild UI cards for current files and subfolders
               5. Preserve current breadcrumb navigation
               6. Call page.update() to render changes
               7. Maintain scroll position if possible

        Interactions:
            - **FolderNavigator**: Executes refresh logic
            - **DriveService**: Queries API for current folder state
            - **folder_list**: Repopulated with refreshed content

        Example:
            >>> # User uploads a file
            >>> dashboard.file_manager.upload_file('document.pdf')
            >>> 
            >>> # Refresh to show newly uploaded file
            >>> dashboard.refresh_folder_contents()
            >>> # folder_list now includes document.pdf
            >>> 
            >>> # Another user shares a file to this folder
            >>> # Refresh to see the new shared file
            >>> dashboard.refresh_folder_contents()

        See Also:
            - :meth:`show_folder_contents`: Navigate to different folder
            - :class:`~ui.dashboard_modules.folder_navigator.FolderNavigator`: Refresh logic

        Notes:
            - Does not change current folder or navigation history
            - Useful after file operations to show updated state
            - Preserves current scroll position in folder_list
            - No API optimization (always fetches full folder data)
            - Consider calling after uploads, deletes, or renames
        """
        self.folder_navigator.refresh_folder_contents()

    def close_dialog(self, dialog):
        """Close an open modal dialog.

        Dismisses a dialog by setting its open property to False and
        updating the page to remove it from the screen. Used for
        closing file operation dialogs, confirmation prompts, and
        form modals.

        Args:
            dialog (ft.AlertDialog): Flet AlertDialog instance to close.
                Must be a dialog that was previously opened and added to
                page.overlay. Can be any dialog type (confirmation, form, etc.).

        Returns:
            None: Updates page to remove dialog as side effect.

        Algorithm:
            **Set Dialog State**:
               1. Access dialog.open property
               2. Set value to False
               3. Marks dialog as closed in Flet's state system

            **Update UI**:
               1. Call self.page.update()
               2. Flet removes dialog from screen
               3. Restores focus to main content
               4. Re-enables underlying UI interaction
        Interactions:
            - **ft.AlertDialog**: Modifies open property
            - **ft.Page**: Updates to remove dialog from overlay

        Example:
            >>> # Create and show confirmation dialog
            >>> confirm_dialog = ft.AlertDialog(
            ...     title=ft.Text("Confirm Delete"),
            ...     content=ft.Text("Delete this file?"),
            ...     actions=[
            ...         ft.TextButton("Cancel", on_click=lambda e: dashboard.close_dialog(confirm_dialog)),
            ...         ft.TextButton("Delete", on_click=lambda e: delete_and_close(e, confirm_dialog))
            ...     ]
            ... )
            >>> confirm_dialog.open = True
            >>> page.overlay.append(confirm_dialog)
            >>> page.update()
            >>> 
            >>> # User clicks Cancel
            >>> dashboard.close_dialog(confirm_dialog)
            >>> # Dialog disappears from screen

        See Also:
            - :class:`~ui.dashboard_modules.file_manager.FileManager`: Creates file operation dialogs
            - :meth:`handle_action`: Opens dialogs for new folder/upload

        Notes:
            - Dialog must be in page.overlay before closing
            - Does not remove dialog from overlay list (just hides it)
            - Safe to call multiple times on same dialog
            - Commonly used in dialog action button callbacks
            - Restores keyboard focus to main content automatically
        """
        dialog.open = False
        self.page.update()

    def show_todo_view(self, e):
        """Switch to the to-do/assignment management view.

        Transitions the main content area from folder browsing to the
        assignment management interface. Clears current folder display
        and loads the TodoView component with full assignment functionality.

        Args:
            e (ft.ControlEvent): Flet control event from button click.
                Typically from "TO-DO" sidebar button. Not used in logic
                but required by Flet event handler signature.

        Returns:
            None: Updates folder_list with TodoView component as side effect.

        Algorithm:
            **Phase 1: Update View State**:
               1. Set self.current_view to "todo"
               2. Marks dashboard as displaying assignment view
               3. Used by other methods to check active view

            **Phase 2: Clear Current Content**:
               1. Access self.folder_list.controls
               2. Call clear() to remove all folder/file cards
               3. Prepares container for TodoView

            **Phase 3: Create TodoView Instance**:
               1. Instantiate TodoView with three parameters:
                  a. self.page: for UI rendering and updates
                  b. on_back: callback set to folder_navigator.load_your_folders
                      - Provides back button functionality
                      - Returns user to folder view when clicked
                  c. drive_service: self.drive for file operations
                       - Enables assignment file uploads/downloads
               2. TodoView initializes with assignment data loading

            **Phase 4: Display TodoView**:
               1. Call todo_view.get_view() to build UI component
               2. Returns ft.Column or ft.Container with TodoView UI
               3. Append returned component to folder_list.controls

            **Phase 5: Refresh UI**:
               1. Call self.page.update()
               2. Renders TodoView in main content area
               3. Folder view replaced with assignment interface

        Interactions:
            - **TodoView**: Instantiated with page, back callback, drive service
            - **FolderNavigator**: Provides load_your_folders as back callback
            - **DriveService**: Passed to TodoView for assignment file operations
            - **folder_list**: Cleared and repopulated with TodoView

        Example:
            >>> # User clicks "TO-DO" button in sidebar
            >>> dashboard.current_view
            'your_folders'
            >>> dashboard.show_todo_view(click_event)
            >>> dashboard.current_view
            'todo'
            >>> # Main area now shows assignment list and management interface
            >>> 
            >>> # User clicks back button in TodoView
            >>> # on_back callback triggers:
            >>> dashboard.folder_navigator.load_your_folders()
            >>> dashboard.current_view
            'your_folders'
            >>> # Returns to folder browsing

        See Also:
            - :class:`~ui.todo_view.TodoView`: Assignment management interface
            - :meth:`show_folder_contents`: Switch to folder view
            - :class:`~ui.dashboard_modules.folder_navigator.FolderNavigator`: Back navigation

        Notes:
            - TodoView receives drive_service for file upload functionality
            - Back callback allows seamless return to folder view
            - Current view state tracked in current_view attribute
            - folder_list completely replaced (not added to)
            - TodoView has independent state management
            - Event parameter required but unused in implementation
        """
        self.current_view = "todo"
        self.folder_list.controls.clear()
        todo_view = TodoView(self.page, on_back=self.folder_navigator.load_your_folders, drive_service=self.drive)
        self.folder_list.controls.append(todo_view.get_view())
        self.page.update()

    def handle_logout(self, e):
        """Handle user logout process.

        Terminates the user's authenticated session and triggers the
        logout callback to return to the login screen. Cleans up
        authentication state and invalidates access tokens.

        Args:
            e (ft.ControlEvent): Flet control event from button click.
                Typically from "ACCOUNT" or logout button. Not used in
                logic but required by Flet event handler signature.

        Returns:
            None: Triggers logout callback as side effect, typically
                navigating to login screen or clearing session.

        Algorithm:
            **Phase 1: Clear Authentication**:
               1. Call self.auth.logout()
               2. Auth service clears stored credentials
               3. Invalidates OAuth2 access and refresh tokens
               4. Removes cached user information

            **Phase 2: Trigger Logout Callback**:
               1. Call self.on_logout() (callback from __init__)
               2. Callback typically performs:
                  a. Clear page contents (page.clean())
                  b. Reset application state
                  c. Navigate to login screen
                  d. Display logout confirmation message

            **Phase 3: Session Termination**:
               1. User returned to unauthenticated state
               2. Dashboard instance effectively terminated
               3. New login required to access Drive features

        Interactions:
            - **GoogleAuth**: Calls logout() to clear credentials
            - **on_logout callback**: Executes provided logout handler
            - **ft.Page**: Callback typically clears and rebuilds page

        Example:
            >>> # Define logout handler
            >>> def return_to_login():
            ...     page.clean()
            ...     page.add(LoginScreen(page))
            ...     page.update()
            >>> 
            >>> dashboard = Dashboard(page, auth, return_to_login)
            >>> 
            >>> # User clicks logout button
            >>> dashboard.handle_logout(click_event)
            >>> # auth.logout() called -> credentials cleared
            >>> # return_to_login() called -> page reset to login screen

        See Also:
            - :class:`~services.google_auth.GoogleAuth`: Handles logout process
            - :meth:`__init__`: Receives on_logout callback parameter

        Notes:
            - Logout callback provided during dashboard initialization
            - Auth service handles credential cleanup
            - Event parameter required but unused
            - Callback should handle page navigation/cleanup
            - User must re-authenticate to access dashboard again
            - No confirmation dialog (implement in callback if needed)
        """
        self.auth.logout()
        self.on_logout()

    def handle_add_account(self, e):
        if self.on_add_account_callback:
            self.on_add_account_callback()
            show_snackbar(self.page, "Redirecting to add account...", ft.Colors.PRIMARY)
        else:
            show_snackbar(self.page, "Redirecting to add account...", ft.Colors.PRIMARY)

    def handle_switch_account(self, email):
        if self.on_switch_account_callback:
            self.on_switch_account_callback(email)
        else:
            show_snackbar(self.page, f"Switching to {email}...", ft.Colors.PRIMARY)


    def handle_action(self, selected_item):
        """Handle sidebar menu action selection.

        Routes user-selected actions from the dropdown menu to appropriate
        handler methods. Supports file operations like creating folders
        and uploading files through the file_manager module.

        Args:
            selected_item (str): Selected menu option text. Expected values:
                "Create Folder", "Upload File". Must match exact button text
                from ButtonWithMenu component. Case-sensitive.

        Returns:
            None: Delegates to appropriate handler and updates page as side effect.

        Algorithm:
            **Phase 1: Action Routing**:
               1. Check if selected_item == "Create Folder"
                  a. If True, call file_manager.create_new_folder_dialog()
                  b. Opens dialog for entering new folder name
                  c. Dialog handles folder creation on confirm
               2. Check elif selected_item == "Upload File"
                  a. If True, call file_manager.select_file_to_upload()
                  b. Opens system file picker dialog
                  c. Handles file selection and upload process

            **Phase 2: Update UI**:
               1. Call self.page.update()
               2. Ensures any dialog or state changes are rendered
               3. Maintains UI responsiveness

        Interactions:
            - **FileManager**: Delegates to create_new_folder_dialog() or select_file_to_upload()
            - **ButtonWithMenu**: Provides selected_item from dropdown
            - **ft.Page**: Updates to render dialogs or changes

        Example:
            >>> # User clicks "+ NEW" and selects "Create Folder"
            >>> dashboard.handle_action("Create Folder")
            >>> # Opens folder creation dialog
            >>> # User enters "My Project" and confirms
            >>> # New folder created in current directory
            >>> 
            >>> # User clicks "+ NEW" and selects "Upload File"
            >>> dashboard.handle_action("Upload File")
            >>> # Opens system file picker
            >>> # User selects file and confirms
            >>> # File uploads to current folder

        See Also:
            - :class:`~ui.dashboard_modules.file_manager.FileManager`: File operations
            - :class:`~ui.custom_control.custom_controls.ButtonWithMenu`: Dropdown menu
            - :meth:`get_view`: Creates "+ NEW" button with menu

        Notes:
            - Only handles file operations currently
            - Extensible for additional menu actions
            - selected_item must match exact menu option text
            - file_manager handles all dialog creation and logic
            - Page update called regardless of action taken
            - Invalid selected_item values are ignored (no action)
        """
        if selected_item == "Create Folder":
            self.file_manager.create_new_folder_dialog()
        elif selected_item == "Upload File":
            self.file_manager.select_file_to_upload()
        self.page.update()

    def get_view(self):
        """Build and return the complete dashboard layout.

        Constructs the full dashboard user interface including sidebar,
        top bar with search, tab navigation, and main content area.
        Assembles all components into a responsive layout that adapts
        to different screen sizes.

        Returns:
            ft.Row: Main dashboard layout containing sidebar and content area.
                Structure: Row[sidebar_container, VerticalDivider, main_content]
                where main_content is Column[top_bar, tabs, folder_list].
                Component expands to fill available space with expand=True.

        Algorithm:
            **Phase 1: Create Sidebar Container**:
               1. Instantiate ft.Container with fixed width=170px
               2. Set bgcolor to light grey (ft.Colors.GREY_100)
               3. Add padding=20 for internal spacing
               4. Calculate visibility:
                  a. visible = (page.width >= 900) OR menu_open
                  b. Shows on desktop or when toggled on mobile
               5. Create Column content with four buttons:
                  a. ButtonWithMenu: "+ NEW" with dropdown menu
                     - Menu items: ["Create Folder", "Upload File"]
                     - on_menu_select: self.handle_action
                  b. ElevatedButton: "SETTINGS" (no-op currently)
                  c. ElevatedButton: "TO-DO" with self.show_todo_view
                  d. ElevatedButton: "ACCOUNT" with self.handle_logout
               6. Set button spacing=15 in Column
               7. Store in self.sidebar_container

            **Phase 2: Create Top Bar**:
               1. Instantiate ft.Container with padding=20
               2. Create Row content with three elements:
                  a. IconButton: hamburger menu (ft.Icons.MENU)
                      a. on_click: self.toggle_menu
                      b. visible: True (always shown)
                  b. self.search_field: search TextField (expands)
                  c. IconButton: account circle (ft.Icons.ACCOUNT_CIRCLE)
                      a. icon_size: 36
                      b. tooltip: self.user_email
               3. Set Row alignment to SPACE_BETWEEN
               4. Store in top_bar variable

            **Phase 3: Create Tab Navigation**:
               1. Instantiate ft.Container with padding=10
               2. Create Row content with three tab buttons:
                  a. ElevatedButton: "YOUR FOLDERS"
                    a. on_click: folder_navigator.reset_to_root()
                  b. ElevatedButton: "PASTE LINKS"
                    b. on_click: paste_links_manager.load_paste_links_view()
                  c. ElevatedButton: "SHARED DRIVES"
                    a. on_click: folder_navigator.load_shared_drives()
               3. Set Row spacing=10, alignment=CENTER
               4. Store in tabs variable

            **Phase 4: Create Main Content Area**:
               1. Instantiate ft.Column with three components:
                  a. top_bar: search and account controls
                  b. tabs: view switching buttons
                  c. Container with folder_list (expand=True)
               2. Set Column expand=True to fill vertical space
               3. Store in main_content variable
            
            **Assemble Final Layout**:
               1. Create ft.Row with three components:
                  a. self.sidebar_container: navigation sidebar
                  b. ft.VerticalDivider(width=1): separator line
                  c. main_content: main display area
               2. Set Row expand=True to fill available space
               3. Return assembled Row component

        Interactions:
            - **ButtonWithMenu**: Custom dropdown for action menu
            - **FileManager**: Handles menu action selections
            - **FolderNavigator**: Handles tab navigation and search
            - **PasteLinksManager**: Handles paste links view
            - **TodoView**: Loaded when TO-DO button clicked

        Example:
            >>> # Initialize dashboard
            >>> dashboard = Dashboard(page, auth, logout_handler)
            >>> 
            >>> # Get complete layout
            >>> layout = dashboard.get_view()
            >>> print(type(layout))
            <class 'flet.Row'>
            >>> 
            >>> # Add to page for rendering
            >>> page.add(layout)
            >>> page.update()
            >>> # Full dashboard now visible with all components

        See Also:
            - :meth:`__init__`: Initializes components used in layout
            - :class:`~ui.custom_control.custom_controls.ButtonWithMenu`: Dropdown button
            - :meth:`show_todo_view`: TO-DO button click handler
            - :meth:`handle_logout`: ACCOUNT button click handler
            - :meth:`handle_action`: Menu selection handler

        Notes:
            - Layout is responsive with 900px breakpoint
            - Sidebar hides on mobile, toggled by hamburger menu
            - Tab buttons switch between different view modes
            - Search field expands to fill available width
            - folder_list populated dynamically based on view
            - VerticalDivider provides visual separation
            - All components configured before return
            - expand=True ensures full viewport usage
        """
        self.sidebar_container = ft.Container(
            width=170,
            bgcolor=ft.Colors.GREY_100,
            padding=20,
            visible=(self.page.width >= 900) or self.menu_open,
            content=ft.Column([
                ButtonWithMenu(
                    text="+ NEW",
                    menu_items=["Create Folder", "Upload File"],
                    on_menu_select=self.handle_action,
                    page=self.page
                ),
                ft.ElevatedButton("TO-DO", on_click=self.show_todo_view),
            ], spacing=15)
        )

        saved_accounts = self.account_manager.get_all_accounts()
        
        profile_menu_instance = GmailProfileMenu(
            page=self.page,
            user_info=self.user_info,
            on_logout=self.handle_logout,
            on_add_account=self.handle_add_account,
            on_switch_account=self.handle_switch_account,
            saved_accounts=saved_accounts,
            account_manager=self.account_manager
        )
        profile_menu = profile_menu_instance.build()

        top_bar = ft.Container(
            padding=20,
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.MENU,
                    on_click=self.toggle_menu,
                    visible=True
                ),
                self.search_field,
                profile_menu,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

        tabs = ft.Container(
            padding=10,
            content=ft.Row([
                ft.ElevatedButton(
                    "YOUR FOLDERS",
                    on_click=lambda e: (self.folder_navigator.reset_to_root()),
                ),
                ft.ElevatedButton(
                    "PASTE LINKS",
                    on_click=lambda e: (self.paste_links_manager.load_paste_links_view()),
                ),
            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
        )

        main_content = ft.Column([
            top_bar,
            tabs,
            ft.Container(expand=True, content=self.folder_list),
        ], expand=True)

        return ft.Row([
            self.sidebar_container,
            ft.VerticalDivider(width=1),
            main_content,
        ], expand=True)