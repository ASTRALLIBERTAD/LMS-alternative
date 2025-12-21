import os
import sys
import json
import time
import flet as ft


def setup_paths():
    app_path = os.path.dirname(os.path.abspath(__file__))
    cwd = os.getcwd()
    
    for path in [cwd, app_path]:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    return app_path, cwd


def repair_filesystem(cwd):
    try:
        files = os.listdir(cwd)
        fixed_any = False
        for filename in files:
            if "\\" in filename:
                new_path = filename.replace("\\", os.sep)
                dir_name = os.path.dirname(new_path)
                if dir_name and not os.path.exists(dir_name):
                    os.makedirs(dir_name, exist_ok=True)
                try:
                    os.rename(filename, new_path)
                    fixed_any = True
                except OSError:
                    pass
        return fixed_any
    except Exception:
        return False


def load_credentials(app_path, cwd):
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


def get_redirect_url(platform):
    is_mobile = platform in [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]
    
    if is_mobile:
        return "https://lms-callback.vercel.app/firebase_callback_v2.html"
    else:
        return "http://localhost:8550/oauth_callback"


def create_system_check_ui(page):
    log_column = ft.Column(scroll=ft.ScrollMode.AUTO)
    page.add(ft.Container(content=log_column, expand=True))
    
    def log(msg, color=ft.Colors.GREEN):
        log_column.controls.append(ft.Text(msg, color=color, size=14, font_family="monospace"))
        page.update()
        print(msg)
    
    return log


def main(page: ft.Page):
    page.title = "System Check"
    page.bgcolor = ft.Colors.BLACK
    page.padding = 20
    
    log = create_system_check_ui(page)
    
    log("1. Application Started", ft.Colors.CYAN)
    
    try:
        log("2. Setting up paths...")
        app_path, cwd = setup_paths()
        log(f"Paths configured")
        
        log("3. Running Filesystem Repair...", ft.Colors.CYAN)
        fixed = repair_filesystem(cwd)
        if fixed:
            log("Filesystem repairs completed", ft.Colors.GREEN)
        else:
            log("No repairs needed", ft.Colors.GREEN)
        
        log("4. Importing Modules...", ft.Colors.CYAN)
        from services.auth_service import GoogleAuth
        from ui.dashboard import Dashboard
        from ui.login import LoginView
        
        try:
            from ui.firebase_mobile_login import FirebaseMobileLogin
            log("Firebase mobile login available")
        except ImportError:
            FirebaseMobileLogin = None
            log("Firebase mobile login not found (optional)", ft.Colors.YELLOW)
        
        log("All modules imported")
        
        log("5. Loading Credentials...", ft.Colors.CYAN)
        creds = load_credentials(app_path, cwd)
        
        if not creds:
            log("ERROR: web.json not found!", ft.Colors.RED)
            return

        log(f"Credentials loaded")

        redirect_url = get_redirect_url(page.platform)
        log(f"Platform: {page.platform.value if hasattr(page.platform, 'value') else page.platform}")
        log(f"Redirect URL: {redirect_url}", ft.Colors.GREEN)
        
        log("6. Initializing Auth Service...", ft.Colors.CYAN)
        auth_service = GoogleAuth(credentials_file=creds['path'])
        log("Auth Service initialized", ft.Colors.GREEN)
        
        log("7. All checks passed! Launching app...", ft.Colors.CYAN)
        time.sleep(2)
        
        page.controls.clear()
        page.title = "LMS Alternative"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.bgcolor = ft.Colors.WHITE
        page.padding = 0
        
        from flet.auth.providers import GoogleOAuthProvider
        
        provider = GoogleOAuthProvider(
            client_id=creds['client_id'],
            client_secret=creds['client_secret'],
            redirect_url=redirect_url
        )
        provider.scopes = ["openid", "email", "profile"]
        
        def handle_on_login(e):
            print("=" * 60)
            print("OAuth Callback Received")
            print("=" * 60)
            
            if e.error:
                print(f"Login error: {e.error}")
                show_snackbar(f"Login Error: {e.error}")
                return
            
            if not hasattr(page.auth, 'token') or not page.auth.token:
                print("No auth token received")
                show_snackbar("Authentication failed: No token received")
                return
            
            token_data = page.auth.token
            print(f"Token received - Type: {type(token_data)}")
            
            if isinstance(token_data, dict):
                print(f"Token keys: {list(token_data.keys())}")
                token_data['client_id'] = creds['client_id']
                token_data['client_secret'] = creds['client_secret']
            
            print("Bridging token to auth service...")
            if auth_service.login_with_token(token_data):
                print("Authentication successful!")
                show_dashboard()
            else:
                print("Failed to bridge token")
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
            print("Logging out...")
            auth_service.logout()
            if hasattr(page.auth, 'logout'):
                page.auth.logout()
            show_login()
        
        def show_login():
            page.controls.clear()
            
            is_mobile = page.platform in [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]
            
            if is_mobile and FirebaseMobileLogin:
                print("Using Firebase mobile login")
                
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
                print("Using standard OAuth login")
                page.add(LoginView(page, provider, auth_service, on_success=show_dashboard))
            
            page.update()
        
        print("\n" + "=" * 60)
        print("LMS Alternative Starting")
        print("=" * 60)
        print(f"Platform: {page.platform}")
        
        if auth_service.is_authenticated():
            print("✓ User already authenticated")
            show_dashboard()
        else:
            print("→ Showing login screen")
            show_login()
            
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        log(f"CRITICAL ERROR: {e}", ft.Colors.RED)
        log(f"Traceback:\n{error_msg}", ft.Colors.RED)
        print(f"CRITICAL ERROR:\n{error_msg}")
        time.sleep(10)


if __name__ == "__main__":
    ft.app(target=main)