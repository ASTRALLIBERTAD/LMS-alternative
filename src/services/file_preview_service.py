"""File Preview Service Module.

This module provides a service for previewing various file types within the app.
It handles fetching file content (local or Drive), detecting mime types,
and rendering appropriate preview widgets (image, text, or placeholders).

Classes:
    FilePreviewService: Manages file preview generation and display.

See Also:
    :class:`~src.services.drive_service.DriveService`: Source for Drive files.
"""

import flet as ft
import base64
import mimetypes
import io
from googleapiclient.http import MediaIoBaseDownload


class FilePreviewService:
    """Service to generate and display file previews.

    Purpose / Responsibility:
        Manages the retrieval of file content (local or Drive) and renders a suitable
        preview widget (Image, Text, or Placeholder) in an overlay.

    Attributes:
        page (ft.Page): The Flet page instance used for overlays.
        drive_service (DriveService): Service to fetch Drive file content.
        current_overlay (ft.Control): The currently active preview overlay control.

    Interactions / Calls:
        - Interacts with `src.services.drive_service.DriveService` to fetch files.
        - Manipulates `flet.Page.overlay` to show/hide previews.

    Algorithm / Pseudocode:
        1. `show_preview` is called.
        2. Content is fetched via `_load_from_drive` or `_load_from_path`.
        3. File type is determined.
        4. Specific renderer (`_create_image_preview`, etc.) builds the UI.
        5. Overlay is added to the page.

    Examples:
        >>> preview_service = FilePreviewService(page, drive_service)
        >>> preview_service.show_preview(file_id="12345", file_name="image.png")

    See Also:
        - :class:`src.services.drive_service.DriveService`
    """

    def __init__(self, page: ft.Page, drive_service=None):
        """Initialize the FilePreviewService.

        Purpose:
            Sets up the service with necessary dependencies.

        Args:
            page (ft.Page): The Flet page instance.
            drive_service (DriveService, optional): Service for Drive operations.

        Interactions:
            - Stores references to `page` and `drive_service`.

        Examples:
            >>> svc = FilePreviewService(page, drive_svc)
        """
        self.page = page
        self.drive_service = drive_service
        self.current_overlay = None
    
    def show_preview(self, file_id=None, file_path=None, file_name="File"):
        """Display a file preview overlay.

        Purpose:
            Initiates the preview process by showing a loading state and then
            asynchronously fetching and rendering the file.

        Args:
            file_id (str, optional): Google Drive file ID.
            file_path (str, optional): Local file path.
            file_name (str): Name of the file to display. Defaults to "File".

        Returns:
            None: output is visual (overlay).

        Interactions:
            - Calls `_load_from_drive` or `_load_from_path`.
            - Modifies `self.page.overlay`.
            - Calls `self.page.update()`.

        Algorithm:
            1. Create a loading container (ProgressRing).
            2. Build the main overlay structure (header + close button).
            3. Append overlay to `page.overlay` and update.
            4. If `file_id` is present: Call `_load_from_drive`.
            5. Else if `file_path` is present: Call `_load_from_path`.
            6. Else: Show error message in container.

        Examples:
            >>> service.show_preview(file_path="C:/data/log.txt", file_name="log.txt")

        See Also:
            - :meth:`_load_from_drive`
            - :meth:`_load_from_path`
        """
        content_container = ft.Container(
            content=ft.Column([
                ft.ProgressRing(),
                ft.Text("Loading preview...", size=14)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=700,
            height=500,
            alignment=ft.alignment.center
        )
        
        def close_preview(e):
            if self.current_overlay and self.current_overlay in self.page.overlay:
                self.page.overlay.remove(self.current_overlay)
                self.current_overlay = None
                self.page.update()
        
        self.current_overlay = ft.Container(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.VISIBILITY, size=24, color=ft.Colors.BLUE),
                        ft.Text(file_name, size=18, weight=ft.FontWeight.BOLD, expand=True),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            on_click=close_preview,
                            tooltip="Close preview"
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(height=1),
                    content_container
                ], tight=True, spacing=10),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=10,
                width=750,
                height=600,
                shadow=ft.BoxShadow(
                    blur_radius=20,
                    color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK)
                )
            ),
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
            on_click=lambda e: None 
        )
        
        self.page.overlay.append(self.current_overlay)
        self.page.update()
        
        
        if file_id and self.drive_service:
            self._load_from_drive(file_id, file_name, content_container, close_preview)
        elif file_path:
            self._load_from_path(file_path, file_name, content_container, close_preview)
        else:
            content_container.content = ft.Column([
                ft.Icon(ft.Icons.ERROR, size=48, color=ft.Colors.RED),
                ft.Text("No file to preview", color=ft.Colors.RED)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            self.page.update()
    
    def _load_from_drive(self, file_id, file_name, container, close_callback):
        """Fetch and load file content from Google Drive.

        Purpose:
            Retrieves file metadata and binary content from Drive API.

        Args:
            file_id (str): Drive file ID.
            file_name (str): File name.
            container (ft.Container): UI container to populate with content.
            close_callback (Callable): Cleanup function for the overlay.

        Returns:
            None: Updates the container in-place.

        Interactions:
            - Calls `self.drive_service.get_file_info`.
            - Calls `self.drive_service.service.files().get_media`.
            - Calls `_render_preview`.
            - Calls `_create_error_view` on failure.

        Algorithm:
            1. Get file info to determine MIME type.
            2. Initialize `MediaIoBaseDownload` request.
            3. Download content into `io.BytesIO` buffer.
            4. Read buffer to bytes.
            5. Call `_render_preview` with data.
            6. On Exception: Render error view.

        See Also:
            - :meth:`src.services.drive_service.DriveService.get_file_info`
        """
        
        try:
            
            file_info = self.drive_service.get_file_info(file_id)
            mime_type = file_info.get('mimeType', '')
            
            
            request = self.drive_service.service.files().get_media(fileId=file_id)
            file_buffer = io.BytesIO()
            downloader = MediaIoBaseDownload(file_buffer, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
            
            file_buffer.seek(0)
            file_data = file_buffer.read()
            
            
            self._render_preview(file_data, mime_type, file_name, container, file_id, close_callback)
            
        except Exception as e:
            container.content = self._create_error_view(
                f"Error loading file: {str(e)}",
                file_id=file_id
            )
            self.page.update()
    
    def _load_from_path(self, file_path, file_name, container, close_callback):
        """Load file content from local filesystem.

        Purpose:
            Reads local file in binary mode for previewing.

        Args:
            file_path (str): Path to local file.
            file_name (str): File name.
            container (ft.Container): Target container.
            close_callback (Callable): Cleanup function.

        Returns:
            None: Updates the container in-place.

        Interactions:
            - Uses `mimetypes.guess_type`.
            - Standard file I/O (`open`).
            - Calls `_render_preview`.

        Algorithm:
            1. Guess MIME type from file path.
            2. Open file in 'rb' mode.
            3. Read content.
            4. Call `_render_preview`.
            5. On Exception: Render error view.
        """
        
        try:
            mime_type, _ = mimetypes.guess_type(file_path)
            
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            self._render_preview(file_data, mime_type, file_name, container, None, close_callback)
            
        except Exception as e:
            container.content = self._create_error_view(f"Error loading file: {str(e)}")
            self.page.update()
    
    def _render_preview(self, file_data, mime_type, file_name, container, file_id=None, close_callback=None):
        """Select and render the appropriate preview widget.

        Purpose:
            Dispatches the file data to the correct renderer method based on MIME type.

        Args:
            file_data (bytes): Raw file content.
            mime_type (str): File MIME type.
            file_name (str): File name.
            container (ft.Container): Target container.
            file_id (str, optional): Drive file ID (for download/open links).
            close_callback (Callable, optional): Cleanup function.

        Returns:
            None: Updates the `container.content` and calls `page.update()`.

        Interactions:
            - Calls `_create_image_preview` etc. based on type.
            - Updates `self.page`.

        Algorithm:
            1. Calculate size in MB.
            2. Match `mime_type` against known prefixes (image/, text/, app/pdf, MS Office).
            3. Call specific creation method (e.g., `_create_image_preview`).
            4. Fallback to `_create_default_preview` if no match.
            5. Set `container.content` to result.
            6. Update page.
        """
        
        preview_widget = None
        size_mb = len(file_data) / (1024 * 1024)
        
        
        if mime_type and mime_type.startswith('image/'):
            preview_widget = self._create_image_preview(file_data, size_mb)
        
        
        elif mime_type == 'application/pdf':
            preview_widget = self._create_pdf_preview(file_data, file_name, size_mb, file_id)
        
        
        elif mime_type and mime_type.startswith('text/'):
            preview_widget = self._create_text_preview(file_data, size_mb)
        
        
        elif mime_type in [
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]:
            preview_widget = self._create_word_preview(file_data, file_name, size_mb, file_id)
        
        
        elif mime_type in [
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ]:
            preview_widget = self._create_excel_preview(file_data, file_name, size_mb, file_id)
        
        elif mime_type in [
            'application/vnd.ms-powerpoint',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        ]:
            preview_widget = self._create_powerpoint_preview(file_data, file_name, size_mb, file_id)
        
        else:
            preview_widget = self._create_default_preview(file_data, file_name, mime_type, size_mb, file_id)
        
        container.content = ft.Column(
            [preview_widget],
            scroll="auto",
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )
        self.page.update()
    
    def _create_image_preview(self, file_data, size_mb):
        """Create a widget for image preview.

        Purpose:
            Renders an image from bytes using base64 encoding.

        Args:
            file_data (bytes): Image data.
            size_mb (float): File size in MB.

        Returns:
            ft.Column: Widget containing the image and size info.

        Interactions:
            - Uses `base64` module.
            - Creates `ft.Image`.

        Algorithm:
            1. Base64 encode the `file_data`.
            2. Return `ft.Image` with `src_base64`.
        """
        
        base64_data = base64.b64encode(file_data).decode()
        return ft.Column([
            ft.Image(
                src_base64=base64_data,
                fit=ft.ImageFit.CONTAIN,
                width=650,
                height=450,
                border_radius=8
            ),
            ft.Text(f"Size: {size_mb:.2f} MB", size=12, color=ft.Colors.GREY_600)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    
    def _create_pdf_preview(self, file_data, file_name, size_mb, file_id):
        """Create a widget for PDF preview.

        Purpose:
            Renders a placeholder for PDFs, with options to download or open in browser.

        Args:
            file_data (bytes): PDF content.
            file_name (str): Document name.
            size_mb (float): Size in MB.
            file_id (str): Drive ID.

        Returns:
            ft.Column: Placeholder UI with action buttons.

        Interactions:
            - Calls `_download_file`.
            - Calls `_open_in_browser`.

        Algorithm:
            1. Show PDF icon and details.
            2. Provide 'Download' button -> `_download_file`.
            3. If `file_id` exists: Provide 'Open in Browser' button -> `_open_in_browser`.
        """
        return ft.Column([
            ft.Icon(ft.Icons.PICTURE_AS_PDF, size=100, color=ft.Colors.RED),
            ft.Text("PDF Document", size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f"Size: {size_mb:.2f} MB", size=14),
            ft.Text("PDF preview is not available in-app", size=12, italic=True, color=ft.Colors.GREY_600),
            ft.Container(height=20),
            ft.Row([
                ft.ElevatedButton(
                    "Download PDF",
                    icon=ft.Icons.DOWNLOAD,
                    on_click=lambda e: self._download_file(file_data, file_name)
                ),
                ft.ElevatedButton(
                    "Open in Browser",
                    icon=ft.Icons.OPEN_IN_NEW,
                    on_click=lambda e: self._open_in_browser(file_id),
                    bgcolor=ft.Colors.BLUE
                ) if file_id else ft.Container()
            ], spacing=10)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
    
    def _create_text_preview(self, file_data, size_mb):
        """Create a scrollable text view.

        Purpose:
            Decodes and displays UTF-8 text content. It safely handles decoding errors.

        Args:
            file_data (bytes): Text content.
            size_mb (float): Size in MB.

        Returns:
            ft.Column: Text viewer widget or Error widget if decoding fails.

        Interactions:
            - Uses `bytes.decode('utf-8')`.

        Algorithm:
            1. Attempt to decode `file_data` as UTF-8.
            2. If successful: Return scrollable `ft.Text`.
            3. If UnicodeDecodeError: Return error UI indicating binary/unsupported format.
        """
        try:
            text_content = file_data.decode('utf-8')
            return ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Text(text_content, selectable=True, size=13)
                    ], scroll="auto"),
                    padding=15,
                    bgcolor=ft.Colors.GREY_100,
                    border_radius=8,
                    width=650,
                    height=450,
                    border=ft.border.all(1, ft.Colors.GREY_300)
                ),
                ft.Text(f"Size: {size_mb:.2f} MB | {len(text_content)} characters", 
                       size=12, color=ft.Colors.GREY_600)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        except UnicodeDecodeError:
            return ft.Column([
                ft.Icon(ft.Icons.ERROR, size=48, color=ft.Colors.ORANGE),
                ft.Text("Cannot decode text file", color=ft.Colors.ORANGE),
                ft.Text("File may be binary or use unsupported encoding", size=12, italic=True)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    
    def _create_word_preview(self, file_data, file_name, size_mb, file_id):
        """Create a widget for Word document preview (placeholder).

        Purpose:
            Provides a UI for Word files, directing users to download or open externally,
            as in-app rendering is not supported.

        Args:
            file_data (bytes): File content.
            file_name (str): File name.
            size_mb (float): Size in MB.
            file_id (str): Drive ID.

        Returns:
            ft.Column: Placeholder UI with download/open actions.
        """
        return ft.Column([
            ft.Icon(ft.Icons.DESCRIPTION, size=100, color=ft.Colors.BLUE),
            ft.Text("Word Document", size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f"Size: {size_mb:.2f} MB", size=14),
            ft.Text("Word preview is not available in-app", size=12, italic=True, color=ft.Colors.GREY_600),
            ft.Text("Download to view full content", size=12, color=ft.Colors.GREY_600),
            ft.Container(height=20),
            ft.Row([
                ft.ElevatedButton(
                    "Download Document",
                    icon=ft.Icons.DOWNLOAD,
                    on_click=lambda e: self._download_file(file_data, file_name)
                ),
                ft.ElevatedButton(
                    "Open in Browser",
                    icon=ft.Icons.OPEN_IN_NEW,
                    on_click=lambda e: self._open_in_browser(file_id),
                    bgcolor=ft.Colors.BLUE
                ) if file_id else ft.Container()
            ], spacing=10)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
    
    def _create_excel_preview(self, file_data, file_name, size_mb, file_id):
        """Create a widget for Excel spreadsheet preview (placeholder).

        Purpose:
            Provides a UI for Excel files, directing users to download or open externally,
            as in-app rendering is not supported.

        Args:
            file_data (bytes): File content.
            file_name (str): File name.
            size_mb (float): Size in MB.
            file_id (str): Drive ID.

        Returns:
            ft.Column: Placeholder UI with download/open actions.
        """
        return ft.Column([
            ft.Icon(ft.Icons.TABLE_CHART, size=100, color=ft.Colors.GREEN),
            ft.Text("Spreadsheet Document", size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f"Size: {size_mb:.2f} MB", size=14),
            ft.Text("Spreadsheet preview is not available in-app", size=12, italic=True, color=ft.Colors.GREY_600),
            ft.Container(height=20),
            ft.Row([
                ft.ElevatedButton(
                    "Download Spreadsheet",
                    icon=ft.Icons.DOWNLOAD,
                    on_click=lambda e: self._download_file(file_data, file_name)
                ),
                ft.ElevatedButton(
                    "Open in Browser",
                    icon=ft.Icons.OPEN_IN_NEW,
                    on_click=lambda e: self._open_in_browser(file_id),
                    bgcolor=ft.Colors.GREEN
                ) if file_id else ft.Container()
            ], spacing=10)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
    
    def _create_powerpoint_preview(self, file_data, file_name, size_mb, file_id):
        """Create a widget for PowerPoint preview (placeholder).

        Purpose:
            Provides a UI for PPT files, directing users to download or open externally,
            as in-app rendering is not supported.

        Args:
            file_data (bytes): File content.
            file_name (str): File name.
            size_mb (float): Size in MB.
            file_id (str): Drive ID.

        Returns:
            ft.Column: Placeholder UI with download/open actions.
        """
        return ft.Column([
            ft.Icon(ft.Icons.SLIDESHOW, size=100, color=ft.Colors.ORANGE),
            ft.Text("Presentation Document", size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f"Size: {size_mb:.2f} MB", size=14),
            ft.Text("Presentation preview is not available in-app", size=12, italic=True, color=ft.Colors.GREY_600),
            ft.Container(height=20),
            ft.Row([
                ft.ElevatedButton(
                    "Download Presentation",
                    icon=ft.Icons.DOWNLOAD,
                    on_click=lambda e: self._download_file(file_data, file_name)
                ),
                ft.ElevatedButton(
                    "Open in Browser",
                    icon=ft.Icons.OPEN_IN_NEW,
                    on_click=lambda e: self._open_in_browser(file_id),
                    bgcolor=ft.Colors.ORANGE
                ) if file_id else ft.Container()
            ], spacing=10)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
    
    def _create_default_preview(self, file_data, file_name, mime_type, size_mb, file_id):
        """Create a generic preview widget for unsupported file types.

        Purpose:
            Handles any file type not covered by specific renderers. Shows generic icon based on extension.

        Args:
            file_data (bytes): File content.
            file_name (str): File name.
            mime_type (str): MIME type.
            size_mb (float): Size in MB.
            file_id (str): Drive ID.

        Returns:
            ft.Column: Generic file info UI with download/open actions.

        Interactions:
            - Checks file extension against internal `icon_map`.

        Algorithm:
            1. Extract file extension.
            2. Lookup icon and color in `icon_map`.
            3. Return UI with icon, type info, and action buttons.
        """
        ext = file_name.split('.')[-1].lower() if '.' in file_name else ''
        
        icon_map = {
            'zip': (ft.Icons.FOLDER_ZIP, ft.Colors.PURPLE),
            'rar': (ft.Icons.FOLDER_ZIP, ft.Colors.PURPLE),
            '7z': (ft.Icons.FOLDER_ZIP, ft.Colors.PURPLE),
            'mp4': (ft.Icons.VIDEO_FILE, ft.Colors.RED),
            'avi': (ft.Icons.VIDEO_FILE, ft.Colors.RED),
            'mov': (ft.Icons.VIDEO_FILE, ft.Colors.RED),
            'mp3': (ft.Icons.AUDIO_FILE, ft.Colors.BLUE),
            'wav': (ft.Icons.AUDIO_FILE, ft.Colors.BLUE),
            'json': (ft.Icons.DATA_OBJECT, ft.Colors.GREEN),
            'xml': (ft.Icons.CODE, ft.Colors.ORANGE),
            'sql': (ft.Icons.STORAGE, ft.Colors.BLUE),
        }
        
        icon, color = icon_map.get(ext, (ft.Icons.INSERT_DRIVE_FILE, ft.Colors.GREY))
        
        return ft.Column([
            ft.Icon(icon, size=100, color=color),
            ft.Text("File Preview Not Available", size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f"Type: {mime_type or 'Unknown'}", size=14, color=ft.Colors.GREY_700),
            ft.Text(f"Size: {size_mb:.2f} MB", size=14, color=ft.Colors.GREY_700),
            ft.Container(height=20),
            ft.Row([
                ft.ElevatedButton(
                    "Download File",
                    icon=ft.Icons.DOWNLOAD,
                    on_click=lambda e: self._download_file(file_data, file_name)
                ),
                ft.ElevatedButton(
                    "Open in Browser",
                    icon=ft.Icons.OPEN_IN_NEW,
                    on_click=lambda e: self._open_in_browser(file_id),
                    bgcolor=ft.Colors.BLUE
                ) if file_id else ft.Container()
            ], spacing=10)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
    
    def _create_error_view(self, error_message, file_id=None):
        """Create an error message widget.

        Purpose:
            Displays a friendly error state when loading fails.

        Args:
            error_message (str): Text to display.
            file_id (str, optional): Drive ID for fallback action.

        Returns:
            ft.Column: Error UI.
        """
        return ft.Column([
            ft.Icon(ft.Icons.ERROR, size=48, color=ft.Colors.RED),
            ft.Text(error_message, color=ft.Colors.RED, text_align=ft.TextAlign.CENTER),
            ft.Container(height=20),
            ft.ElevatedButton(
                "Open in Browser",
                icon=ft.Icons.OPEN_IN_NEW,
                on_click=lambda e: self._open_in_browser(file_id)
            ) if file_id else ft.Container()
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    
    def _download_file(self, file_data, file_name):
        """Save file content to the user's Downloads folder.

        Purpose:
            Writes binary content to the local Downloads directory, handling naming conflicts.

        Args:
            file_data (bytes): Content to save.
            file_name (str): Target filename.

        Interactions:
            - Uses `pathlib.Path` to find home directory.
            - Calls `_show_snackbar`.
            - File system writes.

        Algorithm:
            1. Locate Downloads folder.
            2. Check if file exists; append counter (e.g. "file (1).txt") if so.
            3. Write bytes to file.
            4. Show success/failure snackbar.
        """
        try:
            from pathlib import Path
            
            downloads_path = Path.home() / "Downloads" / file_name
            
            counter = 1
            original_path = downloads_path
            while downloads_path.exists():
                name, ext = original_path.stem, original_path.suffix
                downloads_path = original_path.parent / f"{name} ({counter}){ext}"
                counter += 1
            
            with open(downloads_path, 'wb') as f:
                f.write(file_data)
            
            self._show_snackbar(f"✓ Downloaded to: {downloads_path.name}", ft.Colors.GREEN)
        except Exception as e:
            self._show_snackbar(f"✗ Download failed: {str(e)}", ft.Colors.RED)
    
    def _open_in_browser(self, file_id):
        """Open the file in the default web browser using its Drive ID.

        Purpose:
            Navigates the user to the Google Drive preview URL.

        Args:
            file_id (str): Drive file ID.

        Interactions:
            - Uses `webbrowser.open`.
        """
        if file_id:
            import webbrowser
            webbrowser.open(f"https://drive.google.com/file/d/{file_id}/view")
    
    def _show_snackbar(self, message, color):
        """Display a feedback message to the user.

        Purpose:
            Shows ephemeral status messages (success/error).

        Args:
            message (str): Content text.
            color (str): Background color (e.g. `ft.Colors.GREEN`).

        Interactions:
            - Modifies `self.page.snack_bar`.
        """
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def close_preview(self):
        """Close the currently open preview overlay.

        Purpose:
            Cleanly removes the overlay from the page.

        Interactions:
            - Modifies `self.page.overlay`.
            - Calls `self.page.update()`.
        """
        if self.current_overlay and self.current_overlay in self.page.overlay:
            self.page.overlay.remove(self.current_overlay)
            self.current_overlay = None
            self.page.update()