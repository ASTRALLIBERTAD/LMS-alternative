"""LMS Alternative - Main Application Module.

This module serves as the entry point for the Learning Management System (LMS)
Alternative application built with Flet. It handles application initialization,
OAuth configuration, authentication flow routing, and view management.

Functions:
    setup_paths: Configure Python path for module imports.
    repair_filesystem: Fix malformed filenames from Android file system.
    load_credentials: Load OAuth credentials from JSON file.
    get_redirect_url: Get the OAuth redirect URL for desktop authentication.
    main: Main application entry point and Flet page handler.

Example:
    Run the application directly::

        $ python main.py

    Or use Flet's app runner::

        >>> import flet as ft
        >>> ft.app(target=main)

See Also:
    :class:`~src.services.auth_service.GoogleAuth`: Authentication service.
    :class:`~src.ui.dashboard.Dashboard`: Main dashboard view.
    :class:`~src.ui.login.LoginView`: Desktop login view.
"""

import os
import sys
import json
import flet as ft


def setup_paths():
    """Configure Python path for module imports.

    Adds the application directory and current working directory to sys.path
    to enable imports of project modules regardless of execution context.

    Returns:
        tuple: A tuple containing (app_path, cwd) where:
            - app_path (str): Absolute path to the application directory.
            - cwd (str): Current working directory.

    Algorithm (Pseudocode):
        1. Get absolute path of this file's directory (app_path)
        2. Get current working directory (cwd)
        3. For each path in [cwd, app_path]:
           - If not already in sys.path, insert at position 0
        4. Return (app_path, cwd)

    Example:
        >>> app_path, cwd = setup_paths()
        >>> print(app_path)
        '/path/to/src'
    """
    app_path = os.path.dirname(os.path.abspath(__file__))
    cwd = os.getcwd()
    
    for path in [cwd, app_path]:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    return app_path, cwd


def repair_filesystem(cwd):
    """Repair malformed filenames from Android file system.

    Fixes filenames containing backslashes that may occur when files are
    created on Android and synced to other platforms.

    Args:
        cwd (str): Current working directory to scan for malformed filenames.

    Returns:
        None

    Algorithm (Pseudocode):
        1. Try to list files in cwd
        2. For each filename containing backslashes:
           a. Replace backslashes with OS-appropriate separator
           b. Create parent directories if needed
           c. Rename file to corrected path
        3. Silently ignore any errors

    Note:
        This function fails silently to avoid interrupting app startup.
    """
    try:
        files = os.listdir(cwd)
        for filename in files:
            if "\\" in filename:
                new_path = filename.replace("\\", os.sep)
                dir_name = os.path.dirname(new_path)
                if dir_name and not os.path.exists(dir_name):
                    os.makedirs(dir_name, exist_ok=True)
                try:
                    os.rename(filename, new_path)
                except OSError:
                    pass
    except Exception:
        pass


def load_credentials(app_path, cwd):
    """Load OAuth credentials from JSON configuration file.

    Searches for web.json in multiple locations and extracts OAuth
    client credentials for Google authentication.

    Args:
        app_path (str): Application source directory path.
        cwd (str): Current working directory.

    Returns:
        dict or None: Dictionary containing credentials if found:
            - path (str): Path to the credentials file
            - client_id (str): OAuth client ID
            - client_secret (str): OAuth client secret
            - redirect_uris (list): List of authorized redirect URIs
        Returns None if no valid credentials file is found.

    Algorithm (Pseudocode):
        1. Define search paths: [app_path/services/web.json, cwd/services/web.json,
           app_path/web.json, cwd/web.json]
        2. For each path that exists:
           a. Load JSON data
           b. Extract 'web' or 'installed' config section
           c. If config found, return credentials dict
        3. Return None if no valid credentials found

    See Also:
        :class:`~src.services.auth_service.GoogleAuth`: Uses these credentials.
    """
    possible_paths = [
        os.path.join(app_path, "services", "web.json"),
        os.path.join(cwd, "services", "web.json"),
        os.path.join(app_path, "web.json"),
        os.path.join(cwd, "web.json")
    ]
    
    for creds_path in possible_paths:
        if os.path.exists(creds_path):
            try:
                with open(creds_path, 'r') as f:
                    data = json.load(f)
                    config = data.get('web') or data.get('installed')
                    
                    if not config:
                        continue
                    
                    return {
                        'path': creds_path,
                        'client_id': config.get('client_id'),
                        'client_secret': config.get('client_secret'),
                        'redirect_uris': config.get('redirect_uris', [])
                    }
            except Exception:
                continue
    
    return None


def get_redirect_url():
    """Get the OAuth redirect URL for desktop authentication.

    Returns:
        str: The localhost redirect URL with port 8550.

    Example:
        >>> url = get_redirect_url()
        >>> print(url)
        'http://localhost:8550/oauth_callback'
    """
    return "http://localhost:8550/oauth_callback"


def main(page: ft.Page):
    """Main application entry point and Flet page handler.

    Initializes the LMS application, configures authentication, and manages
    the routing between login and dashboard views based on auth state.

    Args:
        page (ft.Page): The Flet page instance provided by the Flet runtime.

    Returns:
        None

    Raises:
        Exception: Displays critical errors on the page if initialization fails.

    Algorithm (Pseudocode):
        1. Configure page properties (title, theme, bgcolor, padding)
        2. Setup paths and repair filesystem
        3. Import required modules (GoogleAuth, Dashboard, LoginView)
        4. Load OAuth credentials; show error if not found
        5. Create GoogleAuth service and GoogleOAuthProvider
        6. Define nested handler functions:
           - handle_on_login: Process OAuth login callback
           - show_snackbar: Display notification messages
           - show_dashboard: Navigate to dashboard view
           - handle_logout: Clear auth and return to login
           - show_login: Display appropriate login view for platform
        7. Check authentication state:
           - If authenticated: show_dashboard()
           - Else: show_login()
        8. Catch and display any critical errors

    See Also:
        :class:`~src.services.auth_service.GoogleAuth`: Authentication service.
        :class:`~src.ui.dashboard.Dashboard`: Main application dashboard.
        :class:`~src.ui.login.LoginView`: Desktop OAuth login view.
        :class:`~src.ui.firebase_mobile_login.FirebaseMobileLogin`: Mobile login.
    """
    page.title = "LMS Alternative"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    page.padding = 0
    
    try:
        app_path, cwd = setup_paths()
        repair_filesystem(cwd)
        
        from services.auth_service import GoogleAuth
        from ui.dashboard import Dashboard
        from ui.login import LoginView
        
        try:
            from ui.firebase_mobile_login import FirebaseMobileLogin
        except ImportError:
            FirebaseMobileLogin = None
        
        creds = load_credentials(app_path, cwd)
        if not creds:
            page.add(ft.Text("ERROR: web.json not found!", color=ft.Colors.RED))
            page.update()
            return

        redirect_url = get_redirect_url()
        auth_service = GoogleAuth(credentials_file=creds['path'])
        
        from flet.auth.providers import GoogleOAuthProvider
        
        provider = GoogleOAuthProvider(
            client_id=creds['client_id'],
            client_secret=creds['client_secret'],
            redirect_url=redirect_url
        )
        provider.scopes = ["openid", "email", "profile"]
        
        def handle_on_login(e):
            if e.error:
                show_snackbar(f"Login Error: {e.error}")
                return
            
            if not hasattr(page.auth, 'token') or not page.auth.token:
                show_snackbar("Authentication failed: No token received")
                return
            
            token_data = page.auth.token
            
            if isinstance(token_data, dict):
                token_data['client_id'] = creds['client_id']
                token_data['client_secret'] = creds['client_secret']
            
            if auth_service.login_with_token(token_data):
                show_dashboard()
            else:
                show_snackbar("Authentication failed: Could not complete login")
        
        page.on_login = handle_on_login
        
        def show_snackbar(message):
            page.snack_bar = ft.SnackBar(content=ft.Text(message), action="Dismiss")
            page.snack_bar.open = True
            page.update()
        
        def show_dashboard():
            page.controls.clear()
            dashboard = Dashboard(page, auth_service, handle_logout)
            page.add(dashboard.get_view() if hasattr(dashboard, 'get_view') else dashboard)
            page.update()
        
        def handle_logout():
            auth_service.logout()
            if hasattr(page.auth, 'logout'):
                page.auth.logout()
            show_login()
        
        def show_login():
            page.controls.clear()
            
            is_mobile = page.platform in [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]
            
            if is_mobile and FirebaseMobileLogin:
                firebase_config_path = os.path.join(app_path, "services", "firebase_config.json")
                if not os.path.exists(firebase_config_path):
                    firebase_config_path = os.path.join(cwd, "services", "firebase_config.json")
                
                firebase_config = {}
                if os.path.exists(firebase_config_path):
                    with open(firebase_config_path, 'r') as f:
                        firebase_config = json.load(f)
                
                page.add(FirebaseMobileLogin(
                    page, 
                    auth_service, 
                    firebase_config,
                    creds['client_id'],
                    on_success=show_dashboard
                ))
            else:
                page.add(LoginView(page, provider, auth_service, on_success=show_dashboard))
            
            page.update()
        
        if auth_service.is_authenticated():
            show_dashboard()
        else:
            show_login()
            
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        page.add(ft.Text(f"CRITICAL ERROR: {e}", color=ft.Colors.RED))
        page.update()
        print(f"CRITICAL ERROR:\n{error_msg}")


if __name__ == "__main__":
    ft.app(target=main)