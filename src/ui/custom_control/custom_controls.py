"""Custom Controls Module.

This module provides custom Flet UI components for the LMS application.

Classes:
    ButtonWithMenu: A dropdown button styled like an elevated button.
"""

import flet as ft

class ButtonWithMenu(ft.PopupMenuButton):
    """Custom PopupMenuButton styled to look like an ElevatedButton.

    Provides a button with dropdown menu functionality and hover effects.
    It extends Flet's PopupMenuButton but applies custom container styling
    to resemble a standard ElevatedButton with an arrow icon.

    Attributes:
        page (ft.Page): The Flet page for updates.
        on_menu_select (Callable): Callback when menu item is selected.
        button_content (ft.Container): The styled button container.

    Algorithm (Pseudocode):
        1. Initialize with text, menu items, and callback
        2. Create PopupMenuitems from the provided list
        3. Create a styled Container (button_content) with Row(Text, Icon)
        4. Apply BoxShadow and Animation to the container
        5. Bind _on_hover event to modify shadow/scale
        6. Initialize parent PopupMenuButton with the custom content
    """
    
    def __init__(self, text, menu_items, on_menu_select=None, page=None, **kwargs):
        """Initialize the ButtonWithMenu control.

        Args:
            text (str): The label text for the button.
            menu_items (list): List of string items for the dropdown menu.
            on_menu_select (Callable, optional): Function called with selected item text.
            page (ft.Page, optional): Reference to Flet page.
            **kwargs: Additional arguments passed to PopupMenuButton.
        """
        self.page = page  

        popup_items = [
            ft.PopupMenuItem(text=item, on_click=self._handle_menu_click)
            for item in menu_items
        ]
        
        self.button_content = ft.Container(
            content=ft.Row(
                [
                    ft.Text(text, size=14, weight=ft.FontWeight.W_500, color=ft.Colors.ON_PRIMARY),
                    ft.Icon(ft.Icons.ARROW_DROP_DOWN, size=18, color=ft.Colors.ON_PRIMARY),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER,
                tight=True,
            ),
            bgcolor=ft.Colors.PRIMARY,
            padding=ft.padding.symmetric(horizontal=24, vertical=10),
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=2,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(0, 1),
            ),
            animate=ft.Animation(100, ft.AnimationCurve.EASE_IN_OUT),
            on_hover=self._on_hover,
        )
        
        super().__init__(
            content=self.button_content,
            items=popup_items,
            **kwargs
        )
        
        self.on_menu_select = on_menu_select
    
    def _on_hover(self, e):
        """Handle hover events to animate button appearance.

        Updates the button's shadow and scale when hovered.

        Args:
            e (ft.ControlEvent): Hover event containing data (true/false).
        """
        if e.data == "true":
            self.button_content.shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            )
            self.button_content.scale = 1.02
        else:
            self.button_content.shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=2,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(0, 1),
            )
            self.button_content.scale = 1.0
        
        self.button_content.update()
    
    def _handle_menu_click(self, e):
        """Handle menu item selection.

        Invokes the on_menu_select callback with the selected item text.

        Args:
            e (ft.ControlEvent): Click event from the menu item.
        """
        print("MENU CLICKED:", e.control.text)
        print("CALLING on_menu_select:", self.on_menu_select)
        if self.on_menu_select:
            self.on_menu_select(e.control.text)
