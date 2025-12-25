"""Firebase Mobile Login Module.

This module provides a mobile-friendly OAuth authentication UI component
for the Learning Management System. It handles Google OAuth 2.0 authentication
on mobile platforms where native OAuth popups are unavailable.

Classes:
    FirebaseMobileLogin: A Flet Column component for mobile Google OAuth login.

Example:
    >>> login_view = FirebaseMobileLogin(
    ...     page=page,
    ...     auth_service=auth,
    ...     firebase_config=config,
    ...     oauth_client_id="client_id",
    ...     on_success=lambda: page.go("/dashboard")
    ... )
    >>> page.add(login_view)
"""

import flet as ft
import urllib.parse
import urllib.request
import json
import secrets
import threading


class FirebaseMobileLogin(ft.Column):
    """A Flet UI component for Firebase OAuth authentication on mobile platforms.

    This class provides a complete mobile login interface that handles Google OAuth 2.0
    authentication using Firebase. It launches an external browser for user sign-in,
    polls a callback server for token retrieval, and integrates with the application's
    authentication service.

    Attributes:
        page (ft.Page): The Flet page instance for UI updates and platform detection.
        auth (AuthService): The authentication service for token management and login.
        firebase_config (dict): Firebase project configuration dictionary.
        oauth_client_id (str): Google OAuth 2.0 client ID.
        on_success (Callable, optional): Callback function invoked upon successful login.
        session_id (str): Unique session identifier for OAuth state management.
        polling (bool): Flag indicating whether token polling is active.
        status_text (ft.Text): UI element displaying current authentication status.
        login_button (ft.ElevatedButton): Button to initiate the login flow.
        progress (ft.ProgressRing): Progress indicator shown during authentication.

    Algorithm (Pseudocode):
        1. Initialize UI components (status text, login button, progress indicator)
        2. On login button click:
           a. Generate unique session ID using secrets.token_urlsafe
           b. Build OAuth URL with session ID as state parameter
           c. Launch external browser with OAuth URL
           d. Start background polling thread
        3. Polling loop (max 60 attempts, 5-second intervals):
           a. Send GET request to callback server with session ID
           b. If token found, invoke _handle_tokens and stop polling
           c. If timeout reached, invoke _handle_timeout
        4. On token receipt:
           a. Call auth.login_with_token with token data
           b. Invoke on_success callback if authentication succeeds

    See Also:
        :class:`~src.services.auth_service.GoogleAuth`: Handles token storage and validation.
        :class:`~src.ui.login.LoginView`: Alternative desktop login implementation.
    """

    def __init__(self, page, auth_service, firebase_config, oauth_client_id, on_success=None):
        """Initialize the FirebaseMobileLogin component.

        Args:
            page (ft.Page): The Flet page instance for UI updates and navigation.
            auth_service (GoogleAuth): Authentication service instance for login operations.
            firebase_config (dict): Firebase configuration containing API keys and project details.
            oauth_client_id (str): Google OAuth 2.0 client ID for authentication.
            on_success (Callable, optional): Callback function to execute after successful
                authentication. Defaults to None.

        Algorithm (Pseudocode):
            1. Call parent ft.Column.__init__ with layout settings
            2. Store page, auth_service, firebase_config, and oauth_client_id
            3. Initialize session_id and polling flag to None/False
            4. Initialize UI control references to None
            5. Call _build_ui() to construct the user interface

        Example:
            >>> login = FirebaseMobileLogin(
            ...     page=page,
            ...     auth_service=auth,
            ...     firebase_config=config,
            ...     oauth_client_id="client_id",
            ...     on_success=on_login_success
            ... )
        """
        super().__init__(
            controls=[],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            spacing=20
        )
        self.page = page
        self.auth = auth_service
        self.firebase_config = firebase_config
        self.oauth_client_id = oauth_client_id
        self.on_success = on_success
        self.session_id = None
        self.polling = False
        
        self.status_text = None
        self.login_button = None
        self.progress = None
        
        self._build_ui()
        
    def _build_ui(self):
        """Construct the login user interface components.

        Builds and arranges all UI elements including the logo, title text,
        platform indicator, status message, login button, and progress indicator.

        Returns:
            None: Modifies ``self.controls`` in place.

        Algorithm (Pseudocode):
            1. Detect platform name via _get_platform_name()
            2. Add header elements (icon, title, subtitle, platform text)
            3. Create and store status_text with initial message
            4. Create and store login_button with styling
            5. Create and store progress ring (initially hidden)
            6. Append all elements to self.controls

        See Also:
            :meth:`_get_platform_name`: Platform detection helper.
        """
        platform_name = self._get_platform_name()
        
        self.controls.extend([
            ft.Container(height=50),
            ft.Icon(ft.Icons.CLOUD_CIRCLE, size=100, color=ft.Colors.BLUE_600),
            ft.Text("Learning Management System", size=32, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Text("Mobile Login", size=16, color=ft.Colors.GREY_700, text_align=ft.TextAlign.CENTER),
            ft.Container(height=10),
            ft.Text(f"Platform: {platform_name}", size=12, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
            ft.Container(height=20)
        ])
        
        self.status_text = ft.Text("Sign in with your Google account", color=ft.Colors.GREY_700, text_align=ft.TextAlign.CENTER)
        self.controls.append(self.status_text)
        
        self.login_button = ft.ElevatedButton(
            text="Sign in with Google",
            icon=ft.Icons.LOGIN,
            on_click=self.handle_login,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
                padding=ft.padding.symmetric(horizontal=30, vertical=15),
            ),
            height=50
        )
        
        self.controls.extend([
            ft.Container(height=10),
            self.login_button
        ])
        
        self.progress = ft.ProgressRing(visible=False)
        self.controls.append(self.progress)

    def _get_platform_name(self):
        """Get a human-readable name for the current platform.

        Maps Flet's platform enumeration to user-friendly platform names
        for display in the login UI.

        Returns:
            str: Human-readable platform name (e.g., 'Windows', 'Android', 'iOS').

        Algorithm (Pseudocode):
            1. Define mapping: ft.PagePlatform -> human-readable string
            2. Look up self.page.platform in mapping
            3. Return matched name or string representation of platform enum

        Example:
            >>> platform = self._get_platform_name()
            >>> print(platform)
            'Android'
        """
        platform_map = {
            ft.PagePlatform.WINDOWS: "Windows",
            ft.PagePlatform.LINUX: "Linux",
            ft.PagePlatform.MACOS: "macOS",
            ft.PagePlatform.ANDROID: "Android",
            ft.PagePlatform.IOS: "iOS"
        }
        return platform_map.get(self.page.platform, str(self.page.platform))

    def update_status(self, message, color=ft.Colors.BLUE_600):
        """Update the status message displayed to the user.

        Modifies the status text content and color, then triggers a UI refresh.

        Args:
            message (str): The status message to display.
            color (ft.Colors, optional): Text color. Defaults to ft.Colors.BLUE_600.

        Returns:
            None

        Algorithm (Pseudocode):
            1. Set status_text.value to the new message
            2. Set status_text.color to the specified color
            3. Call page.update() to render changes

        Example:
            >>> self.update_status('Authentication complete!', ft.Colors.GREEN_600)
        """
        self.status_text.value = message
        self.status_text.color = color
        self.page.update()

    def handle_login(self, e):
        """Handle the login button click event.

        Initiates the OAuth flow by generating a session ID, building the
        OAuth URL, launching the external browser, and starting token polling.

        Args:
            e (ft.ControlEvent): The click event from the login button.

        Returns:
            None

        Raises:
            Exception: Catches and displays any errors during OAuth initiation.

        Algorithm (Pseudocode):
            1. Generate unique session_id using secrets.token_urlsafe(16)
            2. Update status to 'Opening browser...'
            3. Disable login button and show progress indicator
            4. Try:
               a. Build OAuth URL via _build_oauth_url()
               b. Launch URL in browser via page.launch_url()
               c. Update status to 'Waiting for sign-in...'
               d. Start polling thread via _start_polling()
            5. Except: Display error, re-enable button, hide progress

        See Also:
            :meth:`_build_oauth_url`: Constructs the OAuth authorization URL.
            :meth:`_start_polling`: Initiates background token polling.
        """
        self.session_id = secrets.token_urlsafe(16)
        
        self.update_status("Opening browser...", ft.Colors.ORANGE)
        self.login_button.disabled = True
        self.progress.visible = True
        self.page.update()
        
        try:
            oauth_url = self._build_oauth_url()
            
            self.page.launch_url(oauth_url)
            
            self.update_status("Waiting for sign-in...", ft.Colors.BLUE_600)
            self.page.update()
            
            self._start_polling()
            
        except Exception as ex:
            import traceback
            self.update_status(f"Error: {str(ex)[:50]}...", ft.Colors.RED_600)
            self.login_button.disabled = False
            self.progress.visible = False
            print(f"Mobile login error: {ex}\n{traceback.format_exc()}")
    
    def _build_oauth_url(self):
        """Construct the Google OAuth 2.0 authorization URL.

        Builds a complete OAuth URL with all required parameters for
        implicit grant flow authentication.

        Returns:
            str: The fully-formed OAuth authorization URL.

        Algorithm (Pseudocode):
            1. Set base URL to Google OAuth endpoint
            2. Define parameters (client_id, redirect_uri, response_type, scope, state)
            3. URL-encode parameters and append to base URL
            4. Return complete URL string

        Note:
            Uses implicit grant flow (response_type=token) which returns
            the access token directly in the URL fragment.
        """
        auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
        params = {
            'client_id': self.oauth_client_id,
            'redirect_uri': 'https://lms-callback-git-main-astrallibertads-projects.vercel.app/callback.html',
            'response_type': 'token',
            'scope': 'openid email profile https://www.googleapis.com/auth/drive',
            'state': self.session_id
        }
        return f"{auth_url}?{urllib.parse.urlencode(params)}"
    
    def _start_polling(self):
        """Start background polling for OAuth token retrieval.

        Launches a daemon thread that periodically checks the callback
        server for token data matching the current session ID.

        Returns:
            None

        Algorithm (Pseudocode):
            1. Set self.polling = True
            2. Define inner poll() function:
               a. Set max_attempts = 60, attempt = 0
               b. While polling and attempt < max_attempts:
                  - Update waiting status animation
                  - Send GET request to callback server
                  - If token found, call _handle_tokens and return
                  - Sleep 5 seconds, increment attempt
               c. If max_attempts reached, call _handle_timeout
            3. Create daemon thread with poll as target
            4. Start thread

        Note:
            Polling runs for max 5 minutes (60 attempts x 5 seconds).

        See Also:
            :meth:`_handle_tokens`: Processes received OAuth tokens.
            :meth:`_handle_timeout`: Handles polling timeout.
        """
        self.polling = True
        
        def poll():
            max_attempts = 60
            attempt = 0
            
            while self.polling and attempt < max_attempts:
                self.page.run_task(self._update_waiting_status, attempt)
                
                try:
                    check_url = f"https://lms-callback.vercel.app/api/token/{self.session_id}"
                    
                    req = urllib.request.Request(check_url)
                    req.add_header('Accept', 'application/json')
                    
                    try:
                        with urllib.request.urlopen(req, timeout=10) as response:
                            response_text = response.read().decode('utf-8')
                            data = json.loads(response_text)
                            
                            if data.get('success') and data.get('token'):
                                token_info = data['token']
                                if token_info.get('access_token'):
                                    self.page.run_task(self._handle_tokens, token_info)
                                    return
                            
                    except urllib.error.HTTPError:
                        pass
                    except Exception:
                        pass
                    
                    import time
                    time.sleep(5)
                    attempt += 1
                    
                except Exception:
                    import time
                    time.sleep(5)
                    attempt += 1
            
            if attempt >= max_attempts:
                self.page.run_task(self._handle_timeout)
        
        thread = threading.Thread(target=poll, daemon=True)
        thread.start()
    
    async def _update_waiting_status(self, attempt):
        """Update the waiting status with animated dots.

        Async method that modifies the status text to show a cycling
        dot animation indicating ongoing polling activity.

        Args:
            attempt (int): Current polling attempt number, used to cycle dots.

        Returns:
            None

        Algorithm (Pseudocode):
            1. Calculate dot count: (attempt mod 3) + 1
            2. Build dots string ('.', '..', or '...')
            3. Set status_text.value to 'Waiting for sign-in' + dots
            4. Call page.update() to refresh UI
        """
        dots = "." * ((attempt % 3) + 1)
        self.status_text.value = f"Waiting for sign-in{dots}"
        self.page.update()
    
    async def _handle_tokens(self, tokens):
        """Process received OAuth tokens and complete authentication.

        Async method that stops polling, constructs token data, and
        authenticates with the auth service.

        Args:
            tokens (dict): Token data from callback server containing:
                - access_token (str): OAuth access token
                - token_type (str, optional): Token type, defaults to 'Bearer'
                - expires_in (int, optional): Token expiry in seconds
                - scope (str, optional): Granted OAuth scopes

        Returns:
            None

        Algorithm (Pseudocode):
            1. Set self.polling = False to stop polling thread
            2. Update status to 'Authenticating...'
            3. Construct token_data dict with access_token and metadata
            4. Call auth.login_with_token(token_data)
            5. If auth_result: update status, invoke on_success callback
            6. Else: show error, re-enable login button

        See Also:
            :meth:`~src.services.auth_service.GoogleAuth.login_with_token`
        """
        self.polling = False
        
        self.update_status("Authenticating...", ft.Colors.GREEN_600)
        self.page.update()
        
        token_data = {
            'access_token': tokens.get('access_token'),
            'token_type': tokens.get('token_type', 'Bearer'),
            'expires_in': tokens.get('expires_in'),
            'scope': tokens.get('scope'),
            'client_id': self.oauth_client_id,
            'client_secret': self.auth.client_secret
        }
        
        auth_result = self.auth.login_with_token(token_data)
        
        if auth_result:
            self.update_status("Authentication complete!", ft.Colors.GREEN_600)
            self.progress.visible = False
            self.page.update()
            
            if self.on_success:
                self.on_success()
        else:
            self.update_status("Authentication failed", ft.Colors.RED_600)
            self.login_button.disabled = False
            self.progress.visible = False
            self.page.update()
    
    async def _handle_timeout(self):
        """Handle polling timeout when sign-in takes too long.

        Async method that resets the UI state and displays a timeout
        message when the maximum polling attempts are exhausted.

        Returns:
            None

        Algorithm (Pseudocode):
            1. Set self.polling = False
            2. Update status to 'Timeout - Sign-in took too long' (orange)
            3. Re-enable login button
            4. Hide progress indicator
            5. Call page.update() to refresh UI

        Note:
            Timeout occurs after ~5 minutes (60 attempts x 5 seconds).
        """
        self.polling = False
        self.update_status("Timeout - Sign-in took too long", ft.Colors.ORANGE)
        self.login_button.disabled = False
        self.progress.visible = False
        self.page.update()