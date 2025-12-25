"""Google Authentication Service Module.

This module provides OAuth 2.0 authentication services for Google APIs,
specifically for Google Drive access. It handles credential storage,
token refresh, and service creation.

Classes:
    GoogleAuth: Manages Google OAuth authentication and Drive API access.

Attributes:
    SCOPES (list): OAuth 2.0 scopes required for Google Drive access.

Example:
    >>> auth = GoogleAuth(credentials_file='path/to/web.json')
    >>> if auth.is_authenticated():
    ...     service = auth.get_service()
    ...     # Use service to access Google Drive

See Also:
    :class:`~src.services.drive_service.DriveService`: Uses GoogleAuth for API access.
"""

import os
import pickle
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive"]


class GoogleAuth:
    """Manages Google OAuth 2.0 authentication and Google Drive API access.

    This class handles the complete OAuth lifecycle including credential loading,
    token storage, refresh token management, and Google Drive service creation.

    Attributes:
        creds (Credentials): Google OAuth credentials object.
        credentials_file (str): Path to the OAuth client secrets JSON file.
        token_file (str): Path to the pickled token storage file.
        client_id (str): OAuth client ID from credentials file.
        client_secret (str): OAuth client secret from credentials file.

    Algorithm (Pseudocode):
        1. On initialization:
           a. Load client info from credentials file
           b. Load existing token from pickle file if available
        2. On login (desktop or token):
           a. Acquire credentials via OAuth flow
           b. Save credentials to pickle file
        3. On authenticated requests:
           a. Check credential validity
           b. Refresh if expired and refresh token available
           c. Create and return Google Drive service

    See Also:
        :class:`~src.services.drive_service.DriveService`: Wraps the Drive API service.
        :class:`~src.ui.login.LoginView`: Uses GoogleAuth for desktop login.
    """

    def __init__(self, credentials_file=None):
        """Initialize the GoogleAuth service.

        Args:
            credentials_file (str, optional): Path to OAuth client secrets JSON file.
                Defaults to 'web.json' in the same directory as this module.

        Algorithm (Pseudocode):
            1. Initialize creds to None
            2. Set credentials_file path (use default if not provided)
            3. Set token_file path to 'token.pickle' in module directory
            4. Initialize client_id and client_secret to None
            5. Load client info from credentials file
            6. Load existing credentials from token file

        Example:
            >>> auth = GoogleAuth()  # Uses default web.json
            >>> auth = GoogleAuth('path/to/credentials.json')
        """
        self.creds = None
        self.credentials_file = credentials_file or os.path.join(
            os.path.dirname(__file__), 
            "web.json"
        )
        self.token_file = os.path.join(os.path.dirname(__file__), "token.pickle")
        
        self.client_id = None
        self.client_secret = None
        self._load_client_info()
        self._load_credentials()

    def _load_client_info(self):
        """Load OAuth client information from credentials file.

        Reads the client_id and client_secret from the OAuth credentials
        JSON file and stores them as instance attributes.

        Returns:
            None: Sets self.client_id and self.client_secret.

        Algorithm (Pseudocode):
            1. If credentials file doesn't exist, return early
            2. Open and parse JSON file
            3. Extract 'web' or 'installed' config section
            4. Store client_id and client_secret if found
        """
        if not os.path.exists(self.credentials_file):
            return
            
        try:
            with open(self.credentials_file, 'r') as f:
                data = json.load(f)
                config = data.get('web') or data.get('installed')
                if config:
                    self.client_id = config.get('client_id')
                    self.client_secret = config.get('client_secret')
                    print(f"✓ Loaded client info from {os.path.basename(self.credentials_file)}")
        except Exception as e:
            print(f"Error loading client info: {e}")

    def _load_credentials(self):
        """Load saved credentials from token pickle file.

        Attempts to load previously saved OAuth credentials from the
        token.pickle file for session persistence.

        Returns:
            None: Sets self.creds if token file exists and is valid.

        Algorithm (Pseudocode):
            1. If token file doesn't exist, return early
            2. Open token file in binary read mode
            3. Unpickle and store credentials object
            4. Handle errors by setting creds to None
        """
        if not os.path.exists(self.token_file):
            return
            
        try:
            with open(self.token_file, 'rb') as token:
                self.creds = pickle.load(token)
            print("✓ Loaded existing credentials from token.pickle")
        except Exception as e:
            print(f"⚠ Error loading token: {e}")
            self.creds = None

    def _save_credentials(self):
        """Save current credentials to token pickle file.

        Persists the OAuth credentials to disk for session persistence
        across application restarts.

        Returns:
            None

        Algorithm (Pseudocode):
            1. Open token file in binary write mode
            2. Pickle and write credentials object
            3. Log success or handle errors
        """
        try:
            with open(self.token_file, 'wb') as token:
                pickle.dump(self.creds, token)
            print("Credentials saved to token.pickle")
        except Exception as e:
            print(f"Error saving token: {e}")

    def login_desktop(self):
        """Perform desktop OAuth login flow.

        Launches a local server and opens the browser for user authentication
        using Google's installed app OAuth flow.

        Returns:
            None: Sets self.creds on successful authentication.

        Raises:
            FileNotFoundError: If credentials file doesn't exist.

        Algorithm (Pseudocode):
            1. Verify credentials file exists
            2. Create InstalledAppFlow from client secrets
            3. Run local server on port 8550 for OAuth callback
            4. Store returned credentials
            5. Save credentials to pickle file

        See Also:
            :meth:`login_with_token`: Alternative token-based login.
        """
        if not os.path.exists(self.credentials_file):
            raise FileNotFoundError(f"Credentials file not found at {self.credentials_file}")
            
        from google_auth_oauthlib.flow import InstalledAppFlow
        
        print("Starting desktop OAuth flow...")
        flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
        self.creds = flow.run_local_server(port=8550)
        self._save_credentials()
        print("✓ Desktop login successful")

    def login_with_token(self, token_data):
        """Authenticate using OAuth token data from external source.

        Creates Google credentials from token data received from Flet's
        OAuth provider or mobile authentication flow.

        Args:
            token_data (dict): OAuth token dictionary containing:
                - access_token (str): Required. The OAuth access token.
                - refresh_token (str, optional): Token for refreshing access.
                - client_id (str, optional): OAuth client ID.
                - client_secret (str, optional): OAuth client secret.
                - scope (str or list, optional): Granted OAuth scopes.

        Returns:
            bool: True if authentication successful, False otherwise.

        Algorithm (Pseudocode):
            1. Validate token_data is a dictionary with access_token
            2. Extract tokens, client credentials, and scopes
            3. Create Credentials object with extracted data
            4. Validate and refresh credentials if needed
            5. Save credentials and return success status

        See Also:
            :meth:`login_desktop`: Alternative desktop OAuth flow.
        """
        try:
            print("Bridging OAuth token to Google credentials")
            print(f"Token data type: {type(token_data)}")
            
            if not isinstance(token_data, dict):
                print("Token data is not a dictionary")
                return False
            
            access_token = token_data.get("access_token")
            if not access_token:
                print("No access_token in token_data")
                return False
            
            refresh_token = token_data.get("refresh_token")
            client_id = token_data.get("client_id") or self.client_id
            client_secret = token_data.get("client_secret") or self.client_secret
            
            scope = token_data.get("scope", SCOPES)
            if isinstance(scope, str):
                scope = scope.split() if scope else SCOPES
            
            self._log_token_status(access_token, refresh_token, client_id, client_secret, scope)
            
            self.creds = Credentials(
                token=access_token,
                refresh_token=refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=client_id,
                client_secret=client_secret,
                scopes=scope
            )
            
            if not self._validate_and_refresh_credentials():
                return False
            
            self._save_credentials()
            return True
            
        except Exception as e:
            import traceback
            print(f"Error bridging token: {e}")
            print(f"Traceback:\n{traceback.format_exc()}")
            return False

    def _log_token_status(self, access_token, refresh_token, client_id, client_secret, scope):
        """Log the status of token components for debugging.

        Args:
            access_token (str): The OAuth access token.
            refresh_token (str): The refresh token (may be None).
            client_id (str): OAuth client ID.
            client_secret (str): OAuth client secret.
            scope (list or str): Granted OAuth scopes.

        Returns:
            None: Outputs to console.
        """
        print(f"Access token: present")
        print(f"Refresh token: {'present' if refresh_token else 'missing'}")
        print(f"Client ID: {'present' if client_id else 'missing'}")
        print(f"Client secret: {'present' if client_secret else 'missing'}")
        print(f"Scopes: {', '.join(scope) if isinstance(scope, list) else scope}")
    def _validate_and_refresh_credentials(self):
        """Validate credentials and refresh if expired.

        Checks if current credentials are valid and attempts to refresh
        them using the refresh token if they have expired.

        Returns:
            bool: True if credentials are valid or successfully refreshed.

        Algorithm (Pseudocode):
            1. If credentials are valid, return True
            2. If expired but no refresh token, return False
            3. Attempt to refresh using Google's token endpoint
            4. Return True on success, False on failure
        """
        if self.creds.valid:
            print("Credentials are valid")
            return True
            
        if not self.creds.expired or not self.creds.refresh_token:
            print("Credentials not valid and cannot be refreshed")
            return False
            
        print("Attempting to refresh expired token...")
        try:
            self.creds.refresh(Request())
            print("Token refreshed successfully")
            return True
        except Exception as refresh_error:
            print(f"Failed to refresh token: {refresh_error}")
            return False

    def is_authenticated(self):
        """Check if the user is currently authenticated.

        Validates credentials and attempts refresh if expired.

        Returns:
            bool: True if authenticated with valid credentials.

        Algorithm (Pseudocode):
            1. If no credentials, return False
            2. If credentials not expired, return validity status
            3. If expired without refresh token, return False
            4. Attempt to refresh credentials
            5. Save refreshed credentials and return result
        """
        if self.creds is None:
            return False
        
        if not self.creds.expired:
            return self.creds.valid
            
        if not self.creds.refresh_token:
            print("Credentials expired and no refresh token available")
            return False
            
        try:
            print("→ Refreshing expired credentials...")
            self.creds.refresh(Request())
            self._save_credentials()
            print("✓ Credentials refreshed")
            return True
        except Exception as e:
            print(f"Error refreshing token: {e}")
            return False

    def logout(self):
        """Log out the current user and clear stored credentials.

        Clears the credentials object and removes the token pickle file.

        Returns:
            None

        Algorithm (Pseudocode):
            1. Set credentials to None
            2. If token file exists, delete it
            3. Handle any deletion errors
        """
        print("Logging out...")
        self.creds = None
        if os.path.exists(self.token_file):
            try:
                os.remove(self.token_file)
                print("Token file removed")
            except Exception as e:
                print(f"Error removing token file: {e}")

    def get_service(self):
        """Get an authenticated Google Drive API service.

        Creates and returns a Google Drive API service object for making
        API requests.

        Returns:
            googleapiclient.discovery.Resource or None: The Drive API service
                object, or None if not authenticated.

        Algorithm (Pseudocode):
            1. Check if authenticated; return None if not
            2. Build Drive API v3 service with credentials
            3. Return service object or None on error

        See Also:
            :class:`~src.services.drive_service.DriveService`: Wraps this service.
        """
        if not self.is_authenticated():
            print("Cannot get service - not authenticated")
            return None
        
        try:
            service = build('drive', 'v3', credentials=self.creds)
            print("Google Drive service created")
            return service
        except Exception as e:
            print(f"Error creating service: {e}")
            return None

    def get_user_info(self):
        """Get information about the authenticated user.

        Retrieves user details from the Google Drive API.

        Returns:
            dict: User information containing emailAddress, displayName, etc.
                Returns empty dict if not authenticated or on error.

        Algorithm (Pseudocode):
            1. Get Drive service; return empty dict if None
            2. Call about().get() API endpoint
            3. Extract and return user info from response
        """
        try:
            service = self.get_service()
            if not service:
                return {}
            about = service.about().get(fields="user").execute()
            user = about.get('user', {})
            email = user.get('emailAddress', 'unknown')
            print(f"✓ User info retrieved: {email}")
            return user
        except Exception as e:
            print(f"Error getting user info: {e}")
            return {}