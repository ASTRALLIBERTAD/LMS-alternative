"""File Manager Module.

This module handles file and folder operations within the dashboard,
managing the display and interaction logic for filesystem items.

Classes:
    FileManager: Manages file item creation, menus, and dialogs.

See Also:
    :class:`~src.ui.dashboard.Dashboard`: Connects FileManager to the UI.
    :class:`~src.services.drive_service.DriveService`: Performs the backend operations.
"""

import flet as ft
from utils.common import format_file_size, create_icon_button, show_snackbar, create_dialog, open_drive_file


class FileManager:
    """Manages file and folder UI components and interactions.

    Purpose / Responsibility:
        Handles the creation of visual representations for files and folders,
        manages context menus, and orchestrates user interactions like opening,
        previewing, renaming, deleting, and creating items.

    Attributes:
        dash (Dashboard): Reference to the main dashboard instance for UI updates.
        file_preview (FilePreviewService): Service for generating file type specific previews.

    Interactions / Calls:
        - Interacts with `src.ui.dashboard.Dashboard` to modify the UI.
        - Calls `src.services.drive_service.DriveService` (via `dash.drive`) for backend ops.
        - Uses `src.services.file_preview_service.FilePreviewService` for previews.

    Algorithm / Pseudocode:
        1. Initialize with dashboard.
        2. Set up `FilePreviewService`.
        3. `create_folder_item` / `create_file_item`: Build UI rows with icons and menus.
        4. User clicks -> `handle_file_click` -> Preview or Navigate.
        5. Context menu -> `show_menu` -> Rename/Delete/Info actions.
        6. Dialogs (`_rename_file_dialog`, etc.) capture input and call Drive methods.

    Examples:
        >>> manager = FileManager(dashboard)
        >>> item_control = manager.create_file_item(file_metadata)

    See Also:
        - :class:`~src.ui.dashboard.Dashboard`
        - :class:`~src.services.drive_service.DriveService`
    """

    def __init__(self, dashboard):
        """Initialize the FileManager.

        Purpose:
            Sets up the manager and tries to initialize the preview service.

        Args:
            dashboard (Dashboard): The parent dashboard instance.

        Interactions:
            - Imports and instantiates `FilePreviewService`.
            - Stores `dashboard` reference.

        Examples:
            >>> fm = FileManager(my_dashboard)
        """
        self.dash = dashboard
        
        try:
            from services.file_preview_service import FilePreviewService
            self.file_preview = FilePreviewService(dashboard.page, dashboard.drive)
        except ImportError:
            self.file_preview = None

    def show_menu(self, item, is_folder=False, is_shared_drive=False):
        """Generate context menu items for a file or folder.

        Purpose:
            Creates a list of actions (Preview, Info, Rename, Delete) available for a specific item.

        Args:
            item (dict): The file or folder metadata.
            is_folder (bool): Whether the item is a folder.
            is_shared_drive (bool): Whether the item is a shared drive root.

        Returns:
            list[ft.PopupMenuItem]: proper list of menu action items.

        Interactions:
            - Calls internal methods: `preview_file`, `_rename_file_dialog`, `_delete_file_dialog`, `show_file_info`.

        Algorithm:
            1. Define local callback functions for each action (preview, rename, delete, info).
            2. Create a list of `ft.PopupMenuItem`.
            3. Conditionally include "Preview" if it's a file and preview service exists.
            4. Return the valid items.

        Examples:
            >>> menu = fm.show_menu(file_data, is_folder=False)
        """
        
        def on_preview(e):
            if not is_folder:
                self.preview_file(item)

        def on_rename(e):
            self._rename_file_dialog(item)

        def on_delete(e):
            self._delete_file_dialog(item)

        def on_info(e):
            self.show_file_info(item)
        
        menu_items = [
            ft.PopupMenuItem(text="Preview", on_click=on_preview) if self.file_preview and not is_folder else None,
            ft.PopupMenuItem(text="Info", on_click=on_info),
            ft.PopupMenuItem(text="Rename", on_click=on_rename),
            ft.PopupMenuItem(text="Delete", on_click=on_delete),
        ]

        return [item for item in menu_items if item is not None]

    def create_folder_item(self, folder, subfolder_count, is_shared_drive=False):
        """Create a UI component representing a folder.

        Purpose:
            Builds a standardized visual row for a folder, including icon, name, count, and menu.

        Args:
            folder (dict): Folder metadata (must include 'name' and 'id').
            subfolder_count (int): Number of subfolders contained.
            is_shared_drive (bool): Whether this is a shared drive.

        Returns:
            ft.Container: Clickable folder list item control.

        Interactions:
            - Calls `show_menu` to get options.
            - Calls `open_folder` on click.

        Algorithm:
            1. Get folder name and truncate if > 40 chars.
            2. Generate menu items via `show_menu`.
            3. Construct `ft.Row` with Folder Icon, Name/Count Column, and Menu Button.
            4. Wrap in `ft.Container` with padding and border.
            5. Bind `on_click` to `open_folder`.
        """
        folder_name = folder.get("name", "Untitled")
        display_name = folder_name if len(folder_name) < 40 else folder_name[:37] + "..."
        
        menu_items = self.show_menu(folder, is_folder=True, is_shared_drive=is_shared_drive)

        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.FOLDER, size=24),
                ft.Column([
                    ft.Text(display_name, size=14),
                    ft.Text(f"{subfolder_count} folders", size=12, color=ft.Colors.GREY_600),
                ], expand=True),

                ft.PopupMenuButton(items=menu_items),
            ]),
            padding=10,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_300)),
            on_click=lambda e, f=folder: self.open_folder(f, is_shared_drive),
        )
    
    def create_file_item(self, file):
        """Create a UI component representing a file.

        Purpose:
            Builds a standardized visual row for a file, including icon, name, size, and actions.

        Args:
            file (dict): File metadata.

        Returns:
            ft.Container: Clickable file list item control.

        Interactions:
            - Calls `show_menu`.
            - Calls `preview_file` or `handle_file_click`.
            - Uses `utils.common.format_file_size`.

        Algorithm:
            1. Check `mimeType` to distinguish files from folders (rare case of folder in file list).
            2. Determine Icon and Size string.
            3. Generate menu items.
            4. If it's a file, add a direct "Preview" icon button.
            5. Construct `ft.Row` with Icon, Details, and Action Buttons.
            6. Wrap in `ft.Container` and bind click event.
        """
        is_folder = file.get("mimeType") == "application/vnd.google-apps.folder"
        icon = ft.Icons.FOLDER if is_folder else ft.Icons.INSERT_DRIVE_FILE
        size_str = "Folder" if is_folder else format_file_size(file.get("size"))

        menu_items = self.show_menu(file, is_folder=is_folder)
        action_buttons = []
        if not is_folder and self.file_preview:
            action_buttons.append(
                create_icon_button(ft.Icons.VISIBILITY, "Preview", 
                                  lambda e, f=file: self.preview_file(f))
            )
        action_buttons.append(
            ft.PopupMenuButton(items=menu_items)
        )

        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=24),
                ft.Column([
                    ft.Text(file.get("name", "Untitled"), size=14),
                    ft.Text(size_str, size=12, color=ft.Colors.GREY_600),
                ], expand=True),
                *action_buttons
            ]),
            padding=10,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_200)),
            on_click=lambda e, f=file: self.handle_file_click(f) if is_folder else self.preview_file(f),
        )
    
    def preview_file(self, file):
        """Initiate file preview.

        Purpose:
            Opens the preview overlay for a selected file.

        Args:
            file (dict): File metadata.

        Interactions:
            - Calls `self.file_preview.show_preview`.

        Algorithm:
            1. Check if `file_preview` service is available.
            2. Verify item is not a folder.
            3. Call `show_preview` with file ID and Name.
        """
        if self.file_preview and file.get("mimeType") != "application/vnd.google-apps.folder":
            self.file_preview.show_preview(
                file_id=file.get("id"),
                file_name=file.get("name", "File")
            )
    
    def open_folder(self, folder, is_shared_drive=False):
        """Navigate to a folder.

        Purpose:
            Triggers the dashboard to change the current view to the specified folder.

        Args:
            folder (dict): Folder metadata.
            is_shared_drive (bool): Shared drive flag.

        Interactions:
            - Calls `self.dash.show_folder_contents`.
        """
        self.dash.show_folder_contents(folder["id"], folder.get("name", folder["id"]), is_shared_drive)
    
    def handle_file_click(self, file):
        """Handle click on a file list item.

        Purpose:
            Decides whether to navigate (if folder) or preview (if file).

        Args:
            file (dict): File metadata.

        Interactions:
            - Calls `dash.show_folder_contents` or `preview_file`.

        Algorithm:
            1. Check MIME type.
            2. If 'application/vnd.google-apps.folder', call `show_folder_contents`.
            3. Otherwise, call `preview_file`.
        """
        if file.get("mimeType") == "application/vnd.google-apps.folder":
            self.dash.show_folder_contents(file["id"], file["name"])
        else:
            self.preview_file(file)
    
    def show_folder_menu(self, folder, is_shared_drive=False):
        """Open folder (alias method).

        Purpose:
            Legacy support or alternate entry point for opening a folder.

        Args:
            folder (dict): Folder metadata.
            is_shared_drive (bool): Shared drive flag.

        See Also:
            - :meth:`open_folder`
        """
        self.open_folder(folder, is_shared_drive)
    
    def _rename_file_dialog(self, file):
        """Show dialog to rename a file.

        Purpose:
            Presents a modal input for renaming a file and handles the API call.

        Args:
            file (dict): File to rename.

        Interactions:
            - Accesses `dash.drive.rename_file`.
            - Updates `dash.page.overlay`.
            - Calls `dash.refresh_folder_contents`.

        Algorithm:
            1. Create TextField pre-filled with current name.
            2. Define `rename` action:
               a. Validate input.
               b. Call `drive.rename_file`.
               c. Refresh dashboard content.
               d. Close dialog.
            3. Show overlay with Cancel/Rename buttons.
        """
        name_field = ft.TextField(value=file["name"], autofocus=True)

        def rename(e):
            new_name = name_field.value.strip()
            if new_name and new_name != file["name"]:
                self.dash.drive.rename_file(file["id"], new_name)
                self.dash.refresh_folder_contents()
            dialog_container.visible = False
            self.dash.page.update()

        def cancel(e):
            dialog_container.visible = False
            self.dash.page.update()

        dialog_container = ft.Container(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Rename", size=20, weight=ft.FontWeight.BOLD),
                    name_field,
                    ft.Row([
                        ft.TextButton("Cancel", on_click=cancel),
                        ft.ElevatedButton("Rename", on_click=rename)
                    ], alignment=ft.MainAxisAlignment.END),
                ], tight=True, spacing=15),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=10,
                width=400,
            ),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
        )

        self.dash.page.overlay.append(dialog_container)
        self.dash.page.update()
    
    def _delete_file_dialog(self, file):
        """Show confirmation dialog to delete a file.

        Purpose:
            Safeguards deletion by asking for user confirmation before executing.

        Args:
            file (dict): File to delete.

        Interactions:
            - Accesses `dash.drive.delete_file`.
            - Updates `dash.page.overlay`.

        Algorithm:
            1. Define `delete` action:
               a. Call `drive.delete_file`.
               b. Refresh dashboard.
               c. Close dialog.
            2. Show warning text and Confirm/Cancel buttons in overlay.
        """
        def delete(e):
            self.dash.drive.delete_file(file["id"])
            self.dash.refresh_folder_contents()
            dialog_container.visible = False
            self.dash.page.update()

        def cancel(e):
            dialog_container.visible = False
            self.dash.page.update()

        dialog_container = ft.Container(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Confirm Delete", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Delete '{file.get('name', '')}'?"),
                    ft.Row([
                        ft.TextButton("Cancel", on_click=cancel),
                        ft.ElevatedButton("Delete", on_click=delete, bgcolor=ft.Colors.RED)
                    ], alignment=ft.MainAxisAlignment.END),
                ], tight=True, spacing=15),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=10,
                width=400,
            ),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
        )

        self.dash.page.overlay.append(dialog_container)
        self.dash.page.update()


    
    def show_file_info(self, file):
        """Display detailed file metadata in a dialog.

        Purpose:
            Shows file properties (name, type, size, modified date) and options to preview or open externally.

        Args:
            file (dict): File object or metadata.

        Interactions:
            - Calls `dash.drive.get_file_info` (if full info needed).
            - Calls `utils.common.open_drive_file`.

        Algorithm:
            1. Retrieve full file info if necessary.
            2. Format size string.
            3. Construct UI column with Name, Type, Size, Date.
            4. Add 'Preview' (if supported) and 'Open in Browser' buttons.
            5. Display in overlay.
        """
        info = self.dash.drive.get_file_info(file["id"]) if isinstance(file, dict) and "id" in file else file
        if not info:
            return
        
        size_str = format_file_size(info.get('size')) if info.get('size') else "N/A"
        
        def close_dialog(e):
            dialog_container.visible = False
            self.dash.page.update()
        
        def on_preview(e):
            self.preview_file(info)
            dialog_container.visible = False
            self.dash.page.update()
        
        preview_button = (
            ft.ElevatedButton(
                "Preview",
                icon=ft.Icons.VISIBILITY,
                on_click=on_preview
            ) if self.file_preview else ft.Container()
        )
        
        browser_button = ft.ElevatedButton(
            "Open in Browser",
            icon=ft.Icons.OPEN_IN_NEW,
            on_click=lambda e: open_drive_file(info.get('id'))
        )
        
        dialog_container = ft.Container(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("File Information", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Name: {info.get('name', 'N/A')}"),
                    ft.Text(f"Type: {info.get('mimeType', 'N/A')}"),
                    ft.Text(f"Size: {size_str}"),
                    ft.Text(f"Modified: {info.get('modifiedTime', 'N/A')[:10]}"),
                    ft.Divider(),
                    ft.Row([preview_button, browser_button], spacing=10),
                    ft.Row([
                        ft.TextButton("Close", on_click=close_dialog)
                    ], alignment=ft.MainAxisAlignment.END),
                ], tight=True, spacing=10),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=10,
                width=400,
            ),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
        )

        self.dash.page.overlay.append(dialog_container)
        self.dash.page.update()

    
    def create_new_folder_dialog(self):
        """Show input dialog to create a new folder.

        Purpose:
            Handles creation of a new folder in the current directory.

        Interactions:
            - Calls `dash.drive.create_folder`.
            - Updates `dash.folder_list`.
            - Invalidates cache via `dash.drive._invalidate_cache`.

        Algorithm:
            1. Show name input field in overlay.
            2. On Create:
               a. Validate name.
               b. Call `drive.create_folder`.
               c. Create new UI item (`create_folder_item`).
               d. Insert item into `folder_list` (optimistic UI update).
               e. Invalidate cache for current folder.
               f. Close overlay.

        See Also:
            - :class:`~src.services.drive_service.DriveService`
        """
        name_field = ft.TextField(label="Folder name", autofocus=True)
        loading_text = ft.Text("")

        def create(e):
            folder_name = name_field.value.strip()
            if not folder_name:
                return
            loading_text.value = "Creating folder..."
            self.dash.page.update()

            folder = self.dash.drive.create_folder(folder_name, parent_id=self.dash.current_folder_id)
            if folder:
                self.dash.page.overlay.pop()
                new_folder_item = self.create_folder_item({
                    'id': folder['id'],
                    'name': folder['name'],
                    'mimeType': 'application/vnd.google-apps.folder'
                }, 0)
                insert_position = 1
                if len(self.dash.folder_list.controls) > insert_position:
                    self.dash.folder_list.controls.insert(insert_position, new_folder_item)
                else:
                    self.dash.folder_list.controls.append(new_folder_item)

                self.dash.drive._invalidate_cache(self.dash.current_folder_id)
                self.dash.page.update()
            else:
                loading_text.value = "Failed to create folder."
                self.dash.page.update()

        dialog_container = ft.Container(
            content=ft.Column([
                ft.Text("Create New Folder"),
                name_field,
                loading_text,
                ft.Row([
                    ft.TextButton("Cancel", on_click=lambda e: (self.dash.page.overlay.pop(), self.dash.page.update())),
                    ft.ElevatedButton("Create", on_click=create),
                ], alignment=ft.MainAxisAlignment.END),
            ]),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            width=350,
            height=200,
        )

        self.dash.page.overlay.append(dialog_container)
        self.dash.page.update()
    
    def select_file_to_upload(self):
        """Open system file picker for upload.

        Purpose:
            Allows user to pick local files and uploads them to the current Drive folder.

        Interactions:
            - Uses `ft.FilePicker`.
            - Calls `dash.drive.upload_file`.

        Algorithm:
            1. Define result handler:
               a. Iterate through picked files.
               b. Call `drive.upload_file` for each.
               c. Refresh content.
            2. specific to `file_picker`.
            3. Add picker to overlay and call `pick_files()`.
        """
        def on_result(e: ft.FilePickerResultEvent):
            if not e.files:
                return
            for f in e.files:
                self.dash.drive.upload_file(f.path, parent_id=self.dash.current_folder_id)
            self.dash.refresh_folder_contents()

        file_picker = ft.FilePicker(on_result=on_result)
        self.dash.page.overlay.append(file_picker)
        self.dash.page.update()
        file_picker.pick_files()