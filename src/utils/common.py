"""Common Utility Functions.

This module provides shared helper functions for file I/O, URL handling, string
formatting, and creating common Flet UI elements like snackbars and dialogs.
"""

import flet as ft
import json
import os
from pathlib import Path
from datetime import datetime


def load_json_file(filepath, default=None):
    """Load and parse a JSON file.

    Args:
        filepath (str | Path): Path to the JSON file.
        default (any, optional): Value to return if file doesn't exist or error occurs.
            Defaults to [].

    Returns:
        any: Parsed JSON data or the default value.
    """
    if isinstance(filepath, str):
        filepath = Path(filepath)
    if filepath.exists():
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return default if default is not None else []


def save_json_file(filepath, data):
    """Save data to a JSON file.

    Args:
        filepath (str | Path): Destination path.
        data (any): Serializable data to save.

    Returns:
        bool: True if successful, False otherwise.
    """
    if isinstance(filepath, str):
        filepath = Path(filepath)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving: {e}")
        return False


def format_file_size(size_bytes):
    """Format file size in bytes to human-readable string (B, KB, MB, etc.).

    Args:
        size_bytes (int | None): Size in bytes.

    Returns:
        str: Formatted string (e.g., "1.5 MB") or "Unknown size".
    """
    if size_bytes is None:
        return "Unknown size"
    try:
        size = int(size_bytes)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
    except (ValueError, TypeError):
        return "Unknown size"


def extract_drive_id(url):
    """Extract Google Drive file/folder ID from a URL.

    Supports various Drive URL formats.

    Args:
        url (str): The URL to parse.

    Returns:
        str | None: The extracted ID if found, else None (or the input if it looks like an ID).
    """
    import re
    patterns = [
        r"/folders/([a-zA-Z0-9_-]+)",
        r"/file/d/([a-zA-Z0-9_-]+)",
        r"[?&]id=([a-zA-Z0-9_-]+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    if len(url) > 20 and "/" not in url:
        return url
    
    return None


def open_url(url):
    """Open a URL in the default web browser.

    Args:
        url (str): URL to open.
    """
    import webbrowser
    webbrowser.open(url)


def open_drive_file(file_id):
    """Open a Google Drive file in the browser.

    Args:
        file_id (str): Drive file ID.
    """
    open_url(f"https://drive.google.com/file/d/{file_id}/view")


def open_drive_folder(folder_id):
    """Open a Google Drive folder in the browser.

    Args:
        folder_id (str): Drive folder ID.
    """
    open_url(f"https://drive.google.com/drive/folders/{folder_id}")


def show_snackbar(page, message, color=ft.Colors.BLUE):
    """Display a snackbar message on the page.

    Args:
        page (ft.Page): Flet page instance.
        message (str): Message to display.
        color (str, optional): Background color. Defaults to ft.Colors.BLUE.
    """
    page.snack_bar = ft.SnackBar(content=ft.Text(message), bgcolor=color)
    page.snack_bar.open = True
    page.update()


def create_icon_button(icon, tooltip, on_click, color=None):
    """Create a standard styled Flet IconButton.

    Args:
        icon (str): Icon name.
        tooltip (str): Tooltip text.
        on_click (Callable): Click handler.
        color (str, optional): Icon color.

    Returns:
        ft.IconButton: Configured button.
    """
    return ft.IconButton(
        icon=icon,
        tooltip=tooltip,
        on_click=on_click,
        icon_color=color
    )


def create_dialog(page, title, content, actions=None):
    """Create and show a modal dialog.

    Args:
        page (ft.Page): Flet page instance.
        title (str): Dialog title.
        content (ft.Control): content control.
        actions (list[ft.Control], optional): List of action buttons. Defaults to [OK].

    Returns:
        ft.AlertDialog: The created dialog instance (already opened).
    """
    def close_dialog_handler(e):
        dialog.open = False
        page.update()
    
    dialog = ft.AlertDialog(
        title=ft.Text(title),
        content=content,
        actions=actions or [ft.TextButton("OK", on_click=close_dialog_handler)]
    )
    page.dialog = dialog
    dialog.open = True
    page.update()
    return dialog