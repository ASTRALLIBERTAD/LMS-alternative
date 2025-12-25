"""Folder Navigator Module.

This module handles filesystem navigation logic for the dashboard,
managing current view state, folder loading, and history navigation.

Classes:
    FolderNavigator: Manages folder browsing and navigation state.

See Also:
    :class:`~src.ui.dashboard.Dashboard`: Main UI connect.
    :class:`~src.services.drive_service.DriveService`: Data source.
"""

import flet as ft


class FolderNavigator:
    """Manages navigation state and folder browsing logic.

    Purpose / Responsibility:
        Controls the dashboard's folder navigation system, including traversing folder structures,
        managing the navigation history stack (back button functionality), listing contents,
        and handling search queries.

    Attributes:
        dash (Dashboard): Reference to the main dashboard instance for UI manipulation and state access.

    Interactions / Calls:
        - Interacts with `src.ui.dashboard.Dashboard` to update `current_view`, `current_folder_id`.
        - Calls `src.services.drive_service.DriveService` (via `dash.drive`) to fetch files/folders.
        - Uses `src.ui.dashboard_modules.file_manager.FileManager` (via `dash.file_manager`) to create UI items.

    Algorithm / Pseudocode:
        1. Initialize with dashboard.
        2. `load_your_folders`: Fetch root files and populate list.
        3. `show_folder_contents`: Switch context to specific folder, update UI, push to history stack.
        4. `go_back`: Pop from history stack and restore previous context.
        5. `handle_search`: Query Drive API and display results.

    Examples:
        >>> navigator = FolderNavigator(dashboard)
        >>> navigator.load_your_folders()

    See Also:
        - :class:`~src.ui.dashboard.Dashboard`
        - :class:`~src.services.drive_service.DriveService`
    """

    def __init__(self, dashboard):
        """Initialize the FolderNavigator.

        Purpose:
            Sets up the navigator with access to the dashboard context.

        Args:
            dashboard (Dashboard): The parent dashboard instance.

        Interactions:
            - Stores `dashboard` reference.
        """
        self.dash = dashboard
    
    def load_your_folders(self):
        """Load and display the root 'My Drive' view.

        Purpose:
            Resets view to the user's personal drive root, fetching and displaying top-level folders.

        Interactions:
            - Calls `dash.drive.list_files("root")`.
            - Calls `dash.file_manager.create_folder_item`.
            - Updates `dash.folder_list`.

        Algorithm:
            1. Set view state vars (`current_view="your_folders"`, `current_folder_id="root"`).
            2. Clear UI list.
            3. Call `drive.list_files` for root.
            4. If success:
               a. Filter for folders.
               b. For each folder, fetch sub-content count (depth=1 check).
               c. Create UI item and append to list.
            5. Handle errors/empty states.
            6. Update page.
        """
        self.dash.current_view = "your_folders"
        self.dash.current_folder_id = "root"
        self.dash.current_folder_name = "My Drive"
        self.dash.folder_list.controls.clear()

        try:
            result = self.dash.drive.list_files("root", page_size=100)
            if result is None:
                self.dash.folder_list.controls.append(ft.Text("Failed to load folders."))
            else:
                files = result.get("files", [])
                folders = [f for f in files if f.get("mimeType") == "application/vnd.google-apps.folder"]
                if not folders:
                    self.dash.folder_list.controls.append(ft.Text("No folders found"))
                else:
                    for folder in folders:
                        sub_result = self.dash.drive.list_files(folder["id"], page_size=100)
                        sub_count = 0 if sub_result is None else len([
                            f for f in sub_result.get("files", [])
                            if f.get("mimeType") == "application/vnd.google-apps.folder"
                        ])
                        self.dash.folder_list.controls.append(self.dash.file_manager.create_folder_item(folder, sub_count))
        except:
            self.dash.folder_list.controls.append(ft.Text("Error loading your folders", color=ft.Colors.RED))

        self.dash.page.update()
    
    def load_shared_drives(self):
        """List available shared drives.

        Purpose:
            Switches view to Shared Drives and lists all accessible Team Drives.

        Interactions:
            - Calls `dash.drive.service.drives().list()`.
            - Updates `dash.folder_list`.

        Algorithm:
            1. Set view state (`current_view="shared_drives"`).
            2. Clear history stack.
            3. Call Google Drive API `drives().list()`.
            4. Iterate through drives and create 'fake' folder items (treated as folders).
            5. Append to UI.
        """
        self.dash.current_view = "shared_drives"
        self.dash.folder_stack = []
        self.dash.folder_list.controls.clear()

        try:
            results = self.dash.drive.service.drives().list(pageSize=100, fields="drives(id, name)").execute()
            shared_drives = results.get("drives", [])
            if not shared_drives:
                self.dash.folder_list.controls.append(ft.Text("No shared drives found"))
            else:
                for d in shared_drives:
                    fake_folder = {"id": d["id"], "name": d["name"], "mimeType": "application/vnd.google-apps.folder"}
                    self.dash.folder_list.controls.append(self.dash.file_manager.create_folder_item(fake_folder, 0, is_shared_drive=True))
        except:
            self.dash.folder_list.controls.append(ft.Text("Error loading shared drives", color=ft.Colors.RED))

        self.dash.page.update()
    
    def show_folder_contents(self, folder_id, folder_name=None, is_shared_drive=False, push_to_stack=True):
        """Display the contents of a specific folder.

        Purpose:
            Main navigation method; clears current list and populates with target folder's items.

        Args:
            folder_id (str): Target folder ID.
            folder_name (str, optional): Display name for header. Defaults to ID if None.
            is_shared_drive (bool): Context flag to adjust behavioral logic (if needed).
            push_to_stack (bool): Whether to add the *previous* folder to history stack (Back support).

        Interactions:
            - Calls `dash.drive.list_files`.
            - Updates `dash.folder_list` and `dash.folder_stack`.

        Algorithm:
            1. Determine display name.
            2. Navigation History:
               a. If `push_to_stack` is True, save current `(id, name)` to `folder_stack`.
            3. Update current state (`current_folder_id`, `current_folder_name`).
            4. Build UI:
               a. Create "Back" button (if history exists).
               b. Create Header Row (Name + Refresh button).
               c. Show loading spinner.
            5. Fetch Data:
               a. Call `drive.list_files(folder_id)`.
            6. Render Results:
               a. Remove spinner.
               b. If empty/error -> Show message.
               c. Else -> Loop files and call `file_manager.create_file_item` for each.
            7. Update page.
        """
        display_name = folder_name or folder_id

        if push_to_stack and self.dash.current_folder_id != folder_id:
            self.dash.folder_stack.append((self.dash.current_folder_id, self.dash.current_folder_name))

        self.dash.current_folder_id = folder_id
        self.dash.current_folder_name = display_name

        self.dash.folder_list.controls.clear()

        back_controls = []

        if self.dash.folder_stack:
            back_controls.append(
                ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: self.go_back())
            )

        back_btn = ft.Row(
            [
                *back_controls,
                ft.Text(display_name, size=18, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Refresh", icon=ft.Icons.REFRESH, on_click=lambda e: self.refresh_folder_contents()),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        self.dash.folder_list.controls.append(back_btn)

        loading_indicator = ft.Row([
            ft.ProgressRing(width=20, height=20),
            ft.Text("Loading folder contents...", size=14)
        ])
        self.dash.folder_list.controls.append(loading_indicator)
        self.dash.page.update()

        try:
            result = self.dash.drive.list_files(folder_id, page_size=200, use_cache=False)
            self.dash.folder_list.controls.remove(loading_indicator)

            if result is None:
                self.dash.folder_list.controls.append(ft.Text("Network error", color=ft.Colors.ORANGE))
            else:
                files = result.get("files", [])
                if not files:
                    self.dash.folder_list.controls.append(ft.Text("Folder is empty"))
                else:
                    for f in files:
                        self.dash.folder_list.controls.append(self.dash.file_manager.create_file_item(f))
        except:
            self.dash.folder_list.controls.append(ft.Text("Error loading folder contents", color=ft.Colors.RED))

        self.dash.page.update()
    
    def refresh_folder_contents(self):
        """Force refresh of current folder view.

        Purpose:
            Invalidates the local cache for the current folder and re-fetches data.

        Interactions:
            - Calls `dash.drive._invalidate_cache`.
            - Calls `show_folder_contents`.
        """
        self.dash.drive._invalidate_cache(self.dash.current_folder_id)
        self.show_folder_contents(self.dash.current_folder_id, self.dash.current_folder_name, push_to_stack=False)
    
    def go_back(self):
        """Navigate to previous folder in history stack.

        Purpose:
            Restores the view state to the previous folder/context (mimics browser Back button).

        Algorithm:
            1. Check if `folder_stack` is empty; return if so.
            2. Pop `(fid, fname)` from stack.
            3. Restore state variables.
            4. Logic Branch:
               a. If `fid == "root"`: Restore high-level view (My Drive / Shared Drives / Paste Links) based on `current_view`.
               b. Else: Call `show_folder_contents` for specific folder (with `push_to_stack=False`).
        """
        if not self.dash.folder_stack:
            return
        fid, fname = self.dash.folder_stack.pop()
        self.dash.current_folder_id = fid
        self.dash.current_folder_name = fname

        if fid == "root":
            if self.dash.current_view == "your_folders":
                self.load_your_folders()
            elif self.dash.current_view == "paste_links":
                self.dash.paste_links_manager.load_paste_links_view()
            elif self.dash.current_view == "shared_drives":
                self.load_shared_drives()
        else:
            self.show_folder_contents(fid, fname, push_to_stack=False)
    
    def reset_to_root(self):
        """Reset navigation to the root 'My Drive'.

        Purpose:
            Clears navigation history and returns user to the main entry point.

        Interactions:
            - Clears `dash.folder_stack`.
            - Calls `load_your_folders`.
        """
        self.dash.folder_stack = []
        self.dash.current_folder_id = "root"
        self.dash.current_folder_name = "My Drive"
        self.load_your_folders()
    
    def handle_search(self, e):
        """Execute search based on search field input.

        Purpose:
            Filters the view based on user query.

        Args:
            e (ft.ControlEvent): trigger event (usually "submit" from TextField).

        Interactions:
            - Reads `dash.search_field.value`.
            - Calls `dash.drive.search_files`.
            - Updates `dash.folder_list`.

        Algorithm:
            1. Get user query; strip whitespace.
            2. If empty -> `load_your_folders()` (reset).
            3. Call `drive.search_files(query)`.
            4. Clear UI list.
            5. Render results:
               a. Separate logic for folders (`create_folder_item`) vs files (`create_file_item`).
            6. Update page.

        See Also:
            - :meth:`src.services.drive_service.DriveService.search_files`
        """
        query = self.dash.search_field.value.strip()
        if not query:
            self.load_your_folders()
            return
        results = self.dash.drive.search_files(query)
        self.dash.folder_list.controls.clear()
        if not results:
            self.dash.folder_list.controls.append(ft.Text("No results"))
        else:
            for r in results:
                if r.get("mimeType") == "application/vnd.google-apps.folder":
                    self.dash.folder_list.controls.append(self.dash.file_manager.create_folder_item(r, 0))
                else:
                    self.dash.folder_list.controls.append(self.dash.file_manager.create_file_item(r))
        self.dash.page.update()