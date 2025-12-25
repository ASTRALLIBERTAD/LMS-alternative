"""Paste Links Manager Module.

This module handles the functionality for pasting and processing Google Drive
links (files and folders), managing saved links history, and displaying
the paste links UI view.

Classes:
    PasteLinksManager: Manages link processing, saving, and UI rendering.

See Also:
    :class:`~src.ui.dashboard.Dashboard`: Connects this manager to the UI.
"""

import flet as ft
import json
import os

SAVED_LINKS_FILE = "saved_links.json"


class PasteLinksManager:
    """Manages the 'Paste Drive Links' view and logic.

    Purpose / Responsibility:
        Responsible for parsing pasted Drive URLs, resolving them to file IDs via the backend,
        saving valid links to persistent local storage, and rendering the UI for both
        pasting new links and navigating previously saved ones.

    Attributes:
        dash (Dashboard): Reference to the main dashboard instance for UI updates.
        file_preview (FilePreviewService): Service for rendering file previews.

    Interactions / Calls:
        - Interacts with `src.ui.dashboard.Dashboard` to update the main view area.
        - Calls `src.services.drive_service.DriveService` (via `dash.drive`) to resolve links and fetch info.
        - Calls `src.services.file_preview_service.FilePreviewService` to show previews.
        - Reads/Writes to local JSON file (`saved_links.json`).

    Algorithm / Pseudocode:
        1. Initialize with dashboard and setup preview service.
        2. `load_paste_links_view`: Build UI with input field and list of saved links.
        3. User pastes link -> `handle_paste_link`:
           a. Resolve link via Drive API.
           b. If valid, save to local JSON (`add_saved_link`).
           c. Open folder (navigation) or file (preview / info).
        4. User clicks saved link -> `open_saved_link`: Restore context.

    Examples:
        >>> manager = PasteLinksManager(dashboard)
        >>> manager.load_paste_links_view()

    See Also:
        - :class:`~src.ui.dashboard.Dashboard`
        - :class:`~src.services.drive_service.DriveService`
    """

    def __init__(self, dashboard):
        """Initialize the PasteLinksManager.

        Purpose:
            Sets up the manager and initializes the file preview service.

        Args:
            dashboard (Dashboard): Parent dashboard instance.

        Interactions:
            - Stores `dashboard` reference.
            - Imports `FilePreviewService`.
        """
        self.dash = dashboard
        
        try:
            from services.file_preview_service import FilePreviewService
            self.file_preview = FilePreviewService(dashboard.page, dashboard.drive)
        except ImportError:
            self.file_preview = None
    
    def load_saved_links(self):
        """Load saved links from local JSON file.

        Purpose:
            Retrieves the history of saved Drive links from disk.

        Returns:
            list[dict]: List of saved link dictionaries containing 'id', 'name', 'mimeType', 'url'.

        Interactions:
            - Reads from `saved_links.json`.
            - Uses `json.load`.

        Algorithm:
            1. Check if file exists.
            2. If yes, open and parse JSON.
            3. Return 'links' list.
            4. Handle exceptions (return empty list).
        """
        if os.path.exists(SAVED_LINKS_FILE):
            try:
                with open(SAVED_LINKS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("links", [])
            except Exception as e:
                print(f"Error loading saved links: {e}")
                return []
        return []
    
    def save_saved_links(self, links):
        """Save storage links to local JSON file.

        Purpose:
            Persists the current list of saved links to disk.

        Args:
            links (list[dict]): List of link dictionaries to save.

        Interactions:
            - Writes to `saved_links.json`.
            - Uses `json.dump`.

        Algorithm:
            1. Open file in write mode.
            2. Dump dictionary `{"links": links}` to JSON.
        """
        try:
            with open(SAVED_LINKS_FILE, "w", encoding="utf-8") as f:
                json.dump({"links": links}, f, indent=2)
        except Exception as e:
            print(f"Error saving saved links: {e}")
    
    def add_saved_link(self, file_id, info, original_url):
        """Add a new link to saved history.

        Purpose:
            Appends a new valid link to the saved history if not already present.

        Args:
            file_id (str): Drive file ID.
            info (dict): File metadata (name, mimeType).
            original_url (str): The original pasted URL.

        Returns:
            bool: True if added, False if already exists.

        Interactions:
            - Calls `load_saved_links`.
            - Calls `save_saved_links`.

        Algorithm:
            1. Load current links.
            2. Check for duplicates (by ID).
            3. If new, append dict with details.
            4. Save updated list.
            5. Return success status.
        """
        links = self.load_saved_links()
        if any(l.get("id") == file_id for l in links):
            return False
        links.append({
            "id": file_id,
            "name": info.get("name", file_id),
            "mimeType": info.get("mimeType", ""),
            "url": original_url,
        })
        self.save_saved_links(links)
        return True
    
    def delete_saved_link(self, item):
        """Remove a link from history.

        Purpose:
            Deletes a specific link from the saved history.

        Args:
            item (dict): The link item to remove (must contain 'id').

        Interactions:
            - Calls `load_saved_links`.
            - Calls `save_saved_links`.
            - Calls `load_paste_links_view` (refresh).

        Algorithm:
            1. Load current links.
            2. Filter out item with matching ID.
            3. Save updated list.
            4. If current view is active, refresh UI.
        """
        links = self.load_saved_links()
        links = [l for l in links if l.get("id") != item.get("id")]
        self.save_saved_links(links)
        
        if self.dash.current_view == "paste_links":
            self.load_paste_links_view()
    
    def open_saved_link(self, item):
        """Open a saved link (folder or file).

        Purpose:
            Navigates to the saved item: enters folder if it's a folder, previews/shows info if it's a file.

        Args:
            item (dict): Saved link item metadata.

        Interactions:
            - Calls `dash.folder_navigator.show_folder_contents` (for folders).
            - Calls `file_preview.show_preview` (for files).
            - Calls `dash.file_manager.show_file_info` (fallback).

        Algorithm:
            1. Check mimeType.
            2. If folder: Call `navigator.show_folder_contents`.
            3. If file:
               a. Try `file_preview.show_preview`.
               b. Fallback: fetch info and show via `file_manager`.
        """
        if item.get("mimeType") == "application/vnd.google-apps.folder":
            self.dash.folder_navigator.show_folder_contents(item["id"], item.get("name", item["id"]))
        else:
            if self.file_preview:
                self.file_preview.show_preview(
                    file_id=item["id"],
                    file_name=item.get("name", "File")
                )
            else:
                info = self.dash.drive.get_file_info(item["id"])
                if info:
                    self.dash.file_manager.show_file_info(info)
                else:
                    self.dash.page.snack_bar = ft.SnackBar(ft.Text("Failed to open saved link"), open=True)
                    self.dash.page.update()
    
    def load_paste_links_view(self):
        """Render the main 'Paste Links' view.

        Purpose:
            Builds and displays the UI for managing Drive links, including the input area and saved list.

        Interactions:
            - Modifies `dash.current_view`.
            - Clears and updates `dash.folder_list`.
            - Calls `build_saved_links_ui`.

        Algorithm:
            1. Set current view state.
            2. Clear main content area.
            3. Build Header.
            4. Build Paste Section (Input + Button + Help text).
            5. Build Saved Links Section (Header + List from `build_saved_links_ui`).
            6. Add all to `dash.folder_list`.
            7. Update page.
        """
        self.dash.current_view = "paste_links"
        self.dash.folder_list.controls.clear()

        header = ft.Container(
            content=ft.Text("Paste Drive Links", size=20, weight=ft.FontWeight.BOLD),
            padding=10
        )

        paste_section = ft.Container(
            content=ft.Column([
                ft.Text("Paste a Google Drive folder or file link:" , size=14),
                self.dash.paste_link_field,
                ft.ElevatedButton(
                    "Open Link",
                    on_click=self.handle_paste_link,
                    bgcolor=ft.Colors.BLUE_400,
                    color=ft.Colors.WHITE,
                    icon=ft.Icons.LINK
                ),
                ft.Text(
                    "Supported formats:\n"
                    "• https://drive.google.com/drive/folders/FOLDER_ID\n"
                    "• https://drive.google.com/file/d/FILE_ID\n"
                    "• https://drive.google.com/...?id=ID",
                    size=12,
                    color=ft.Colors.GREY_600
                )
            ], spacing=10),
            padding=20,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10
        )

        saved_links_header = ft.Container(
            content=ft.Text("Saved Links", size=16, weight=ft.FontWeight.BOLD),
            padding=ft.padding.only(top=20, bottom=10, left=10)
        )

        saved_links_list = ft.Container(
            content=self.build_saved_links_ui(),
            padding=10
        )

        self.dash.folder_list.controls.extend([
            header,
            paste_section,
            saved_links_header,
            saved_links_list
        ])

        self.dash.page.update()
    
    def handle_paste_link(self, e):
        """Process the pasted link from the input field.

        Purpose:
             Validates user input, resolves the Drive link, saves it, and opens the content.

        Args:
            e (ft.ControlEvent): Button click event.

        Interactions:
            - Reads `dash.paste_link_field`.
            - Calls `dash.drive.resolve_drive_link`.
            - Calls `add_saved_link`.
            - Calls `folder_navigator` or `file_preview`.
            - Shows Snackbars.

        Algorithm:
            1. Get text from input; validate not empty.
            2. Show "Loading" snackbar.
            3. Call `drive.resolve_drive_link(link)`.
            4. If invalid: Show error snackbar.
            5. If valid:
               a. Call `add_saved_link`.
               b. Show success snackbar.
               c. If folder: Open via navigator.
               d. If file: Open via preview service or show info.
            6. Clear input field.
            7. Refresh view if active.
            8. Handle exceptions.

        See Also:
            - :meth:`src.services.drive_service.DriveService.resolve_drive_link`
        """
        link = self.dash.paste_link_field.value.strip()
        print(f"DEBUG: handle_paste_link called with: {link}")

        if not link:
            print("DEBUG: Empty link")
            return
        
        loading_snack = ft.SnackBar(
            content=ft.Text("Loading Drive link..."),
            open=True
        )
        self.dash.page.snack_bar = loading_snack
        self.dash.page.update()

        try:
            file_id, info = self.dash.drive.resolve_drive_link(link)

            print(f"DEBUG: file_id={file_id}, info={info}")

            if not file_id or not info:
                error_snack = ft.SnackBar(
                    content=ft.Text("Invalid or inaccessible Drive link"),
                    bgcolor=ft.Colors.RED_400,
                    open=True
                )
                self.dash.page.snack_bar = error_snack
                self.dash.page.update()
                return

            mime_type = info.get("mimeType", "")
            name = info.get("name", "Shared Item")

            print(f"DEBUG: mime_type={mime_type}, name={name}")

            try:
                saved_added = self.add_saved_link(file_id, info, link)
                if saved_added:
                    self.dash.page.snack_bar = ft.SnackBar(ft.Text("Saved link"), open=True)
                else:
                    self.dash.page.snack_bar = ft.SnackBar(ft.Text("Link already saved"), open=True)
            except Exception as ex:
                print(f"ERROR: Failed to save link: {ex}")

            if mime_type == "application/vnd.google-apps.folder":
                success_snack = ft.SnackBar(
                    content=ft.Text(f"Opening folder: {name}"),
                    bgcolor=ft.Colors.GREEN_400,
                    open=True
                )
                self.dash.page.snack_bar = success_snack
                self.dash.page.update()
                self.dash.folder_navigator.show_folder_contents(file_id, name)
            else:
                if self.file_preview:
                    info_snack = ft.SnackBar(
                        content=ft.Text(f"Opening preview: {name}"),
                        bgcolor=ft.Colors.BLUE_400,
                        open=True
                    )
                    self.dash.page.snack_bar = info_snack
                    self.dash.page.update()
                    self.file_preview.show_preview(file_id=file_id, file_name=name)
                else:
                    info_snack = ft.SnackBar(
                        content=ft.Text(f"File detected: {name}"),
                        bgcolor=ft.Colors.BLUE_400,
                        open=True
                    )
                    self.dash.page.snack_bar = info_snack
                    self.dash.page.update()
                    self.dash.file_manager.show_file_info(info)

            self.dash.paste_link_field.value = ""

        except Exception as ex:
            print(f"ERROR: Exception in handle_paste_link: {ex}")
            error_snack = ft.SnackBar(
                content=ft.Text(f"Error: {str(ex)}"),
                bgcolor=ft.Colors.RED_400,
                open=True
            )
            self.dash.page.snack_bar = error_snack

        if self.dash.current_view == "paste_links":
            self.load_paste_links_view()

        self.dash.page.update()
    
    def build_saved_links_ui(self):
        """Construct the UI for the list of saved links.

        Purpose:
            Generates the list of visual cards/rows for each saved link.

        Returns:
            ft.Column: A column control containing the list items.

        Interactions:
            - Calls `load_saved_links`.
            - Binds `open_saved_link` and `delete_saved_link` handlers.

        Algorithm:
            1. Load saved links.
            2. If empty, return "No saved links" text.
            3. Iterate links:
               a. Determine icon (Folder vs File).
               b. Create Row with Icon, Name, Preview/Open Button, Delete Button.
               c. Wrap in styled Container.
            4. Return Column of containers.
        """
        saved = self.load_saved_links()
        col = ft.Column(spacing=4)

        if not saved:
            col.controls.append(ft.Text("No saved links yet.", color=ft.Colors.GREY_600))
            return col

        for item in saved:
            is_folder = item.get("mimeType") == "application/vnd.google-apps.folder"
            icon = ft.Icons.FOLDER if is_folder else ft.Icons.DESCRIPTION

            row = ft.Container(
                content=ft.Row([
                    ft.Icon(icon, size=20),
                    ft.Text(item["name"], expand=True),
                    ft.IconButton(
                        icon=ft.Icons.VISIBILITY,
                        tooltip="Preview" if not is_folder else "Open",
                        on_click=lambda e, it=item: self.open_saved_link(it)
                    ) if self.file_preview or is_folder else ft.Container(),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        tooltip="Delete",
                        on_click=lambda e, it=item: self.delete_saved_link(it)
                    )
                ]),
                padding=8,
                ink=True,
                on_click=lambda e, it=item: self.open_saved_link(it),
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=8
            )

            col.controls.append(row)

        return col