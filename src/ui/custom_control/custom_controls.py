"""Custom Controls Module.

This module provides custom Flet UI components for the LMS application.

Classes:
    ButtonWithMenu: A dropdown button styled like an elevated button.
"""

import flet as ft

class ButtonWithMenu(ft.PopupMenuButton):
    """Custom dropdown button styled as an elevated button with hover animations.

    ButtonWithMenu extends Flet's PopupMenuButton to create a visually enhanced
    dropdown control that resembles a standard ElevatedButton. It features smooth
    hover animations (shadow expansion and scale effects), consistent styling with
    primary theme colors, and simplified menu item handling through callbacks.
    
    This component bridges the gap between Flet's functional PopupMenuButton and
    the visual design language of ElevatedButton, providing a dropdown that feels
    cohesive with other button components while maintaining the menu functionality.
    It's particularly useful for action buttons that offer multiple related options
    (e.g., "Download as... → PDF/DOCX/TXT").

    Purpose:
        - Provide dropdown button with ElevatedButton appearance
        - Support hover animations (shadow and scale effects)
        - Simplify menu item selection with callback pattern
        - Maintain consistent button styling across application
        - Enable dynamic menu content through item list
        - Provide visual feedback for user interactions

    Attributes:
        page (ft.Page or None): Flet page instance for UI updates. Used for
            manual page updates if needed. May be None if updates handled
            elsewhere. Not currently used in implementation but available.
        on_menu_select (Callable or None): Callback function invoked when user
            selects menu item. Signature: (item_text: str) -> None. Receives
            the text of selected menu item. None if no callback registered.
        button_content (ft.Container): Styled container wrapping button visual.
            Contains Row with text label and dropdown arrow icon. Manages shadow,
            scale, and animation properties. Updated on hover events.

    Interactions:
        - **ft.PopupMenuButton**: Parent class providing menu functionality
        - **ft.Container**: Button visual container with styling
        - **ft.Row**: Layout for text and icon
        - **ft.Text**: Button label display
        - **ft.Icon**: Dropdown arrow indicator
        - **ft.PopupMenuItem**: Menu item controls
        - **ft.BoxShadow**: Shadow effects for depth
        - **ft.Animation**: Smooth transitions

    Algorithm (High-Level Workflow):
        **Phase 1: Initialization**
            1. Store page reference (optional)
            2. Convert menu_items strings to PopupMenuItem objects
            3. Create styled button_content Container:
               a. Build Row with label text and dropdown icon
               b. Apply PRIMARY bgcolor and padding
               c. Add initial BoxShadow for depth
               d. Configure animation for smooth transitions
               e. Register hover event handler
            4. Call parent PopupMenuButton constructor with button_content
            5. Store on_menu_select callback reference
        
        **Phase 2: Hover Animation** (_on_hover)
            1. Check hover state from event data
            2. If hovering (data == "true"):
               a. Increase shadow blur and spread
               b. Scale button to 1.02 (2% larger)
            3. If not hovering (data == "false"):
               a. Reset shadow to default
               b. Reset scale to 1.0
            4. Update button_content to render changes
        
        **Phase 3: Menu Selection** (_handle_menu_click)
            1. Extract selected item text from event
            2. Log selection for debugging
            3. Check if callback registered
            4. Invoke on_menu_select with item text

    Example:
        >>> # Create dropdown button for file export
        >>> def handle_export(format_type):
        ...     print(f"Exporting as {format_type}")
        ...     # Export logic here
        >>> 
        >>> export_button = ButtonWithMenu(
        ...     text="Export File",
        ...     menu_items=["PDF", "DOCX", "TXT", "CSV"],
        ...     on_menu_select=handle_export,
        ...     page=page
        ... )
        >>> page.add(export_button)
        >>> 
        >>> # User clicks button → menu appears
        >>> # User selects "PDF" → handle_export("PDF") called
        >>> 
        >>> # Without callback
        >>> simple_menu = ButtonWithMenu(
        ...     text="Options",
        ...     menu_items=["Option 1", "Option 2", "Option 3"]
        ... )
        >>> # Menu works but no action on selection
        >>> 
        >>> # With hover effects
        >>> # User hovers → shadow increases, button scales to 102%
        >>> # User moves away → shadow and scale reset

    See Also:
        - :class:`ft.PopupMenuButton`: Parent Flet class
        - :class:`ft.ElevatedButton`: Standard button for comparison
        - :class:`ft.Container`: Container styling reference
        - :class:`ft.PopupMenuItem`: Menu item class

    Notes:
        - Extends ft.PopupMenuButton (inherits menu behavior)
        - Styled to match ElevatedButton appearance
        - Hover animations enhance user feedback
        - Primary color from theme (adaptive)
        - Arrow icon indicates dropdown functionality
        - Callback receives string (item text)
        - Menu opens on click automatically (parent behavior)
        - Animation duration: 100ms with ease-in-out curve
        - Scale effect: 1.0 (normal) to 1.02 (hover)
        - Shadow increases on hover (visual depth)
        - Page reference optional (not used in current implementation)

    Design Considerations:
        - Visual consistency with ElevatedButton
        - Smooth animations for professional feel
        - Clear dropdown indicator (arrow icon)
        - Accessible interaction patterns
        - Theme-aware color scheme

    References:
        - Flet PopupMenuButton: https://flet.dev/docs/controls/popupmenubutton
        - Material Design Buttons: https://m3.material.io/components/buttons
        - Animation Curves: https://api.flutter.dev/flutter/animation/Curves-class.html
    """
    
    def __init__(self, text, menu_items, on_menu_select=None, page=None, **kwargs):
        """Initialize ButtonWithMenu with label, menu items, and callback.

        Creates a styled dropdown button with specified menu options. Builds
        visual appearance matching ElevatedButton and registers callback for
        menu selection handling.

        Args:
            text (str): Label text displayed on button. Shown alongside dropdown
                arrow. Should be concise action description. Example: "Export",
                "Download", "More Options".
            menu_items (list[str]): List of menu item labels. Each string becomes
                a selectable menu item. Order preserved in menu display. Example:
                ["Option 1", "Option 2", "Option 3"].
            on_menu_select (Callable, optional): Callback invoked when menu item
                selected. Signature: (item_text: str) -> None. Receives selected
                item text as parameter. None if no callback needed. Defaults to None.
            page (ft.Page, optional): Flet page instance for updates. Currently
                not used in implementation but stored for future enhancements.
                Defaults to None.
            **kwargs: Additional keyword arguments passed to parent PopupMenuButton
                constructor. Can include tooltip, disabled, etc.

        Algorithm:
            1. **Store Page Reference**:
               a. Assign page parameter to self.page
               b. Available for future update operations
            
            2. **Create Menu Items**:
               a. Initialize empty list: popup_items
               b. For each item in menu_items:
                  i. Create ft.PopupMenuItem with text
                  ii. Set on_click to self._handle_menu_click
                  iii. Append to popup_items list
               c. Menu items ready for popup display
            
            3. **Build Button Visual Container**:
               a. Create ft.Row with contents:
                  i. ft.Text(text):
                     - Size: 14px
                     - Weight: W_500 (medium)
                     - Color: ON_PRIMARY (theme-based)
                  ii. ft.Icon(ARROW_DROP_DOWN):
                      - Size: 18px
                      - Color: ON_PRIMARY
                  iii. Spacing: 8px between elements
                  iv. Alignment: CENTER
                  v. Tight: True (compact layout)
               
               b. Wrap Row in ft.Container (button_content):
                  i. Set bgcolor: PRIMARY (theme color)
                  ii. Set padding: horizontal=24px, vertical=10px
                  iii. Set border_radius: 20px (rounded)
                  iv. Add BoxShadow:
                      - spread_radius: 0
                      - blur_radius: 2px (subtle)
                      - color: BLACK with 30% opacity
                      - offset: (0, 1) - slight downward
                  v. Configure Animation:
                     - duration: 100ms
                     - curve: EASE_IN_OUT
                  vi. Register on_hover: self._on_hover
               
               c. Store container in self.button_content
            
            4. **Initialize Parent Class**:
               a. Call super().__init__() with:
                  i. content: button_content (styled container)
                  ii. items: popup_items (menu list)
                  iii. **kwargs: additional parameters
               b. Parent provides menu functionality
            
            5. **Store Callback**:
               a. Assign on_menu_select to self.on_menu_select
               b. Used when menu item clicked

        Interactions:
            - **ft.PopupMenuItem**: Creates menu items
            - **ft.Row**: Arranges text and icon
            - **ft.Text**: Button label
            - **ft.Icon**: Dropdown indicator
            - **ft.Container**: Button visual styling
            - **ft.PopupMenuButton.__init__()**: Parent initialization

        Example:
            >>> # Basic initialization
            >>> button = ButtonWithMenu(
            ...     text="Actions",
            ...     menu_items=["Edit", "Delete", "Share"]
            ... )
            >>> 
            >>> # With callback
            >>> def handle_action(action):
            ...     print(f"Action selected: {action}")
            >>> 
            >>> button = ButtonWithMenu(
            ...     text="File Operations",
            ...     menu_items=["Open", "Save", "Close"],
            ...     on_menu_select=handle_action,
            ...     page=page
            ... )
            >>> 
            >>> # With additional PopupMenuButton parameters
            >>> button = ButtonWithMenu(
            ...     text="Options",
            ...     menu_items=["A", "B", "C"],
            ...     tooltip="Select an option",
            ...     disabled=False
            ... )

        See Also:
            - :meth:`_handle_menu_click`: Callback handler
            - :meth:`_on_hover`: Hover animation handler
            - :class:`ft.PopupMenuButton`: Parent class

        Notes:
            - Menu items converted to PopupMenuItem objects
            - All items share same click handler
            - Button appearance matches ElevatedButton
            - Hover effects configured during initialization
            - Page parameter optional (may be None)
            - **kwargs passed to parent for extended functionality
            - Container stored as button_content for hover updates
            - Animation configured for smooth transitions
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
        """Handle hover events to animate button appearance with shadow and scale.

        Updates button visual state when user hovers or moves away. Increases
        shadow depth and scales button slightly larger on hover, then resets
        to default state on mouse leave. Provides visual feedback for interaction.

        Args:
            e (ft.ControlEvent): Hover event from Flet framework. Contains data
                property with string value: "true" when mouse enters hover area,
                "false" when mouse leaves. Event source is button_content container.

        Returns:
            None: Modifies button_content properties and updates as side effects.

        Algorithm:
            1. **Check Hover State**:
               a. Access e.data property (string: "true" or "false")
               b. Compare: if e.data == "true"
            
            2. **Apply Hover Effects** (if hovering):
               a. Update button_content.shadow:
                  i. spread_radius: 0 (no spread)
                  ii. blur_radius: 8px (increased from 2px)
                  iii. color: BLACK with 40% opacity (darker)
                  iv. offset: (0, 2) - more downward shadow
               b. Update button_content.scale:
                  i. Set to 1.02 (2% larger)
                  ii. Creates subtle growth effect
            
            3. **Reset to Default** (if not hovering):
               a. Update button_content.shadow:
                  i. spread_radius: 0
                  ii. blur_radius: 2px (original)
                  iii. color: BLACK with 30% opacity (lighter)
                  iv. offset: (0, 1) - subtle shadow
               b. Update button_content.scale:
                  i. Set to 1.0 (normal size)
            
            4. **Apply Changes**:
               a. Call button_content.update()
               b. Triggers re-render with new properties
               c. Animation makes transition smooth (100ms ease-in-out)

        Interactions:
            - **ft.ControlEvent**: Provides hover state data
            - **ft.BoxShadow**: Shadow effect modification
            - **button_content.update()**: Renders changes

        Example:
            >>> # User interaction flow:
            >>> # 1. Mouse enters button area
            >>> # → e.data = "true"
            >>> # → Shadow increases (blur: 2→8, opacity: 0.3→0.4)
            >>> # → Button scales to 102%
            >>> # → Smooth animation over 100ms
            >>> 
            >>> # 2. Mouse leaves button area
            >>> # → e.data = "false"
            >>> # → Shadow decreases (blur: 8→2, opacity: 0.4→0.3)
            >>> # → Button scales to 100%
            >>> # → Smooth animation over 100ms

        See Also:
            - :meth:`__init__`: Registers this as hover handler
            - :class:`ft.BoxShadow`: Shadow configuration
            - :class:`ft.Animation`: Smooth transition

        Notes:
            - Called automatically by Flet on hover events
            - e.data is string, not boolean
            - Animation configured in __init__ (100ms, ease-in-out)
            - Shadow changes create depth perception
            - Scale change subtle but noticeable (2%)
            - Update triggers smooth transition
            - Hover effects standard for modern UI
            - Shadow offset increases on hover (1→2)
            - Opacity increases on hover (0.3→0.4)
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
        """Handle menu item selection and invoke registered callback.

        Processes menu item click event by extracting selected text and
        calling the on_menu_select callback if registered. Logs selection
        for debugging purposes.

        Args:
            e (ft.ControlEvent): Click event from PopupMenuItem. Contains
                control property with reference to clicked menu item.
                e.control.text holds the menu item text (string).

        Returns:
            None: Invokes callback as side effect if registered.

        Algorithm:
            1. **Log Selection** (debugging):
               a. Print "MENU CLICKED:" with e.control.text
               b. Helps debug menu interaction
            
            2. **Log Callback State** (debugging):
               a. Print "CALLING on_menu_select:" with callback reference
               b. Shows if callback registered
            
            3. **Check Callback Registration**:
               a. If self.on_menu_select is not None:
                  i. Callback registered, proceed
               b. If None:
                  i. No callback, return early
            
            4. **Invoke Callback**:
               a. Extract menu item text: e.control.text
               b. Call self.on_menu_select(text)
               c. Pass selected item text as parameter
               d. Callback handles application logic

        Interactions:
            - **ft.ControlEvent**: Provides clicked control reference
            - **ft.PopupMenuItem**: Source of text property
            - **on_menu_select callback**: User-provided handler

        Example:
            >>> # Setup with callback
            >>> def handle_selection(item):
            ...     print(f"Selected: {item}")
            ...     if item == "Delete":
            ...         confirm_delete()
            ...     elif item == "Edit":
            ...         open_editor()
            >>> 
            >>> button = ButtonWithMenu(
            ...     text="Actions",
            ...     menu_items=["Edit", "Delete", "Share"],
            ...     on_menu_select=handle_selection
            ... )
            >>> 
            >>> # User clicks "Delete" menu item
            >>> # → _handle_menu_click called with event
            >>> # → Prints: "MENU CLICKED: Delete"
            >>> # → Prints: "CALLING on_menu_select: <function...>"
            >>> # → Calls: handle_selection("Delete")
            >>> # → Output: "Selected: Delete"
            >>> # → Executes: confirm_delete()

        See Also:
            - :meth:`__init__`: Registers this handler for all menu items
            - :class:`ft.PopupMenuItem`: Menu item control

        Notes:
            - Called automatically when menu item clicked
            - All menu items share this handler
            - Item identification by text property
            - Debug prints help troubleshoot menu issues
            - Callback receives item text as string
            - No action if callback not registered
            - Menu auto-closes after selection (parent behavior)
            - Event contains full control reference
        """
        print("MENU CLICKED:", e.control.text)
        print("CALLING on_menu_select:", self.on_menu_select)
        if self.on_menu_select:
            self.on_menu_select(e.control.text)
