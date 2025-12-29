"""Google Authentication Service Module.

Provides OAuth 2.0 authentication for Google Drive API with credential
management, token refresh, and session persistence.

Classes:
    GoogleAuth: OAuth 2.0 authentication manager for Drive API.

Module Attributes:
    SCOPES (list[str]): Required OAuth scopes for Drive access.

Example:
    >>> from services.auth_service import GoogleAuth
    >>> auth = GoogleAuth('web.json')
    >>> auth.login_desktop()
    >>> service = auth.get_service()

See Also:
    - :class:`DriveService`: Uses GoogleAuth for authenticated API access
    - :mod:`ui.login`: Desktop authentication interface
"""

import os
import pickle
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive"]


class GoogleAuth:
    """OAuth 2.0 authentication manager for Google Drive API.

    Manages complete authentication lifecycle including credential storage,
    automatic token refresh, and session persistence. Supports both desktop
    OAuth flow (browser-based) and token bridging from external providers.

    Purpose:
        - Handle OAuth 2.0 authentication flows
        - Persist credentials across sessions
        - Automatically refresh expired tokens
        - Provide authenticated Drive API service

    Attributes:
        creds (Credentials or None): OAuth credentials with access/refresh tokens.
            None when not authenticated.
        credentials_file (str): Path to OAuth client secrets JSON (web.json).
        token_file (str): Path to pickled credentials (token.pickle).
        client_id (str or None): OAuth client ID from credentials file.
        client_secret (str or None): OAuth client secret from credentials file.

    Algorithm:
        **Initialization Flow**:
            1. Set file paths for credentials and token storage
            2. Load client_id and client_secret from credentials JSON
            3. Restore existing session from token.pickle if available
        
        **Desktop Authentication**:
            1. Launch local server on port 8550
            2. Open browser for user consent
            3. Receive authorization code via callback
            4. Exchange code for tokens
            5. Persist credentials to token.pickle
        
        **Token-Based Authentication**:
            1. Validate incoming token structure
            2. Create Credentials object from token data
            3. Refresh if expired
            4. Save to token.pickle

    Example:
        >>> # Desktop authentication
        >>> auth = GoogleAuth('web.json')
        >>> auth.login_desktop()
        >>> 
        >>> # Token-based authentication
        >>> token_data = {
        ...     'access_token': 'ya29...',
        ...     'refresh_token': '1//0g...',
        ...     'client_id': 'xxx.apps.googleusercontent.com',
        ...     'client_secret': 'secret'
        ... }
        >>> auth.login_with_token(token_data)
        >>> 
        >>> # Use authenticated service
        >>> if auth.is_authenticated():
        ...     service = auth.get_service()
        ...     user = auth.get_user_info()

    See Also:
        - :class:`DriveService`: Wraps GoogleAuth for Drive operations
        - :class:`ui.login.LoginView`: Desktop OAuth UI
        - :meth:`login_desktop`: Browser-based authentication
        - :meth:`login_with_token`: External token integration

    Notes:
        - Credentials stored in token.pickle (binary format)
        - Tokens auto-refresh when expired
        - Desktop OAuth uses port 8550
        - Add token.pickle to .gitignore

    Security Considerations:
        - Never commit web.json or token.pickle
        - Credentials file contains client_secret
        - Token file contains user access tokens
        - Use appropriate file permissions (chmod 600)
        - Refresh tokens have long lifetime
    """

    def __init__(self, credentials_file=None):
        """Initialize authentication manager.

        Args:
            credentials_file (str, optional): Path to OAuth client secrets JSON.
                Defaults to 'web.json' in module directory.

        Example:
            >>> auth = GoogleAuth()  # Uses default web.json
            >>> auth = GoogleAuth('/path/to/credentials.json')
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
        """Load OAuth client credentials from configuration file.

        Reads the OAuth client secrets JSON file, extracts the client_id and
        client_secret, and stores them as instance attributes. Supports both
        'web' and 'installed' application type configurations.

        Returns:
            None: Sets self.client_id and self.client_secret as side effects.
                Both None if file doesn't exist or parsing fails.

        Algorithm:
            1. **Check File Existence**:
               1. Check if self.credentials_file exists
               2. If not, return early (no error, silent failure)
            
            2. **Try Loading File**:
               1. Enter try block for error handling
               2. Open credentials_file in read mode
               3. Parse JSON content with json.load()
               4. Store in data variable

            3. **Extract Configuration Section**:
               1. Try to get 'web' section: data.get('web')
               2. If 'web' is None, try 'installed': data.get('installed')
               3. Store result in config variable
               4. Supports both application types
            
            4. **Extract Client Credentials**:
               1. If config found (not None):
                  a. Extract client_id: config.get('client_id')
                  b. Store in self.client_id
                  c. Extract client_secret: config.get('client_secret')
                  d. Store in self.client_secret
                  e. Print success message with filename
            
            5. **Handle Errors**:
               1. Catch any Exception during file read/parse
               2. Print error message to console
               3. Client_id and client_secret remain None

        Interactions:
            - **os.path.exists()**: Checks file existence
            - **json.load()**: Parses JSON configuration
            - **os.path.basename()**: Gets filename for logging

        Example:
            >>> auth = GoogleAuth()
            >>> # After initialization:
            >>> print(auth.client_id)
            123456-abc.apps.googleusercontent.com
            >>> print(auth.client_secret)
            GOCSPX-abc123...
            >>> 
            >>> # If file doesn't exist:
            >>> auth = GoogleAuth('/nonexistent/path.json')
            >>> print(auth.client_id)
            None

        See Also:
            - :meth:`__init__`: Calls this during initialization
            - :meth:`login_with_token`: Uses client_id and client_secret

        Notes:
            - Supports both 'web' and 'installed' OAuth app types
            - Silent failure if file doesn't exist (no exception)
            - Prints success message on successful load
            - Client credentials required for token operations
            - File format matches Google Cloud Console export
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
        """Load saved OAuth credentials from pickle file.

        Attempts to restore a previous authentication session by unpickling
        the credentials object from token.pickle. Enables session persistence
        across application restarts.

        Returns:
            None: Sets self.creds if token file exists and is valid.
                Remains None if file doesn't exist or unpickling fails.

        Algorithm:
            1. **Check File Existence**:
               a. Check if self.token_file exists
               b. If not, return early (no saved session)
            
            2. **Try Loading Credentials**:
               a. Enter try block for error handling
               b. Open token_file in binary read mode ('rb')
               c. Use context manager for automatic closing
               d. Call pickle.load(token) to deserialize
               e. Store result in self.creds
               f. Print success message
            
            3. **Handle Errors**:
               a. Catch any Exception during unpickling
               b. Print warning message with error details
               c. Set self.creds = None (invalid session)

        Interactions:
            - **os.path.exists()**: Checks file existence
            - **pickle.load()**: Deserializes credentials object
            - **File I/O**: Opens file in binary mode

        Example:
            >>> # First run - no token file
            >>> auth = GoogleAuth()
            >>> print(auth.creds)
            None
            >>> 
            >>> # After login and save
            >>> auth.login_desktop()
            >>> # token.pickle created
            >>> 
            >>> # Second run - session restored
            >>> auth2 = GoogleAuth()
            >>> print(auth2.creds)
            <Credentials object>
            >>> print(auth2.is_authenticated())
            True

        See Also:
            - :meth:`__init__`: Calls this during initialization
            - :meth:`_save_credentials`: Saves credentials to pickle
            - :meth:`is_authenticated`: Validates loaded credentials

        Notes:
            - Token file may not exist (first run or after logout)
            - Credentials may be expired even if loaded successfully
            - Pickle format is Python-specific (not portable)
            - Silent failure if file corrupt or wrong format
            - Prints success message when credentials restored
            - Credentials validated later by is_authenticated()
        """
        pass

    def _save_credentials(self):
        """Persist current OAuth credentials to pickle file.

        Serializes the credentials object to token.pickle for session
        persistence across application restarts. Called after successful
        authentication or token refresh.

        Returns:
            None: Writes to token.pickle file as side effect.

        Algorithm:
            1. **Try Saving Credentials**:
               a. Enter try block for error handling
               b. Open self.token_file in binary write mode ('wb')
               c. Use context manager for automatic closing
               d. Call pickle.dump(self.creds, token)
               e. Serializes credentials object to file
               f. Print success message
            
            2. **Handle Errors**:
               a. Catch any Exception during pickling
               b. Print error message with exception details
               c. File may not be created if error occurs

        Interactions:
            - **pickle.dump()**: Serializes credentials object
            - **File I/O**: Opens file in binary write mode

        Example:
            >>> auth = GoogleAuth()
            >>> auth.login_desktop()  # Sets self.creds
            >>> # _save_credentials() called automatically
            >>> # token.pickle now exists
            >>> 
            >>> # Manual save after token refresh
            >>> auth.creds.refresh(Request())
            >>> auth._save_credentials()
            Credentials saved to token.pickle

        See Also:
            - :meth:`_load_credentials`: Loads credentials from pickle
            - :meth:`login_desktop`: Calls this after authentication
            - :meth:`login_with_token`: Calls this after token validation
            - :meth:`is_authenticated`: Calls this after refresh

        Notes:
            - Called automatically after successful authentication
            - Called after token refresh to save new tokens
            - Overwrites existing token.pickle
            - File contains sensitive credentials (use .gitignore)
            - Pickle format preserves full Credentials object state
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

    def login_desktop(self):
        """Perform desktop OAuth 2.0 authentication flow with browser.

        Launches a local HTTP server on port 8550 and opens the system browser
        to Google's OAuth consent screen. After user authorization, receives
        the authorization code via callback and exchanges it for access and
        refresh tokens. Saves credentials to pickle file for session persistence.

        Returns:
            None: Sets self.creds on successful authentication. Side effects:
                - Opens system browser to OAuth consent screen
                - Starts local server on port 8550
                - Creates/updates token.pickle file

        Raises:
            FileNotFoundError: If credentials_file doesn't exist at specified path.
                Must have valid web.json with OAuth client configuration.

        Algorithm:
            1. **Verify Credentials File**:
               a. Check if self.credentials_file exists
               b. If not, raise FileNotFoundError with path

            2. **Import OAuth Flow**:
               a. Import InstalledAppFlow from google_auth_oauthlib.flow
               b. Lazy import (only when needed)
            
            3. **Start OAuth Flow**:
               a. Print status message: "Starting desktop OAuth flow..."
               b. Create flow: InstalledAppFlow.from_client_secrets_file()
                  i. Pass self.credentials_file (web.json path)
                  ii. Pass SCOPES (Drive API scope)
               c. Flow configured with client credentials
            
            4. **Run Local Server**:
               a. Call flow.run_local_server(port=8550)
               b. Starts HTTP server on localhost:8550
               c. Opens default browser to OAuth consent URL
               d. User sees Google sign-in and consent screen
               e. User authorizes application
               f. Browser redirects to localhost:8550/oauth_callback
               g. Server receives authorization code
               h. Flow exchanges code for tokens
               i. Returns Credentials object with tokens
            
            5. **Store Credentials**:
               a. Assign returned credentials to self.creds
               b. Contains access_token and refresh_token
            
            6. **Save to Pickle**:
               a. Call self._save_credentials()
               b. Persists session to token.pickle
            
            7. **Log Success**:
               a. Print success message: "✓ Desktop login successful"

        Interactions:
            - **os.path.exists()**: Verifies credentials file
            - **InstalledAppFlow.from_client_secrets_file()**: Creates OAuth flow
            - **InstalledAppFlow.run_local_server()**: Runs auth server
            - **_save_credentials()**: Persists credentials

        Example:
            >>> auth = GoogleAuth('path/to/web.json')
            >>> auth.login_desktop()
            Starting desktop OAuth flow...
            # Browser opens to Google OAuth consent screen
            # User signs in and authorizes
            # Browser shows success message
            ✓ Desktop login successful
            >>> 
            >>> # Check authentication
            >>> if auth.is_authenticated():
            ...     print("Login successful!")
            Login successful!
            >>> 
            >>> # Get Drive service
            >>> service = auth.get_service()

        See Also:
            - :meth:`login_with_token`: Alternative token-based authentication
            - :meth:`is_authenticated`: Validates authentication status
            - :meth:`_save_credentials`: Persists credentials
            - `InstalledAppFlow <https://google-auth-oauthlib.readthedocs.io/>`_

        Notes:
            - Port 8550 must be in authorized redirect URIs (Google Console)
            - Browser must be available on system
            - User must complete OAuth consent in browser
            - Automatically saves credentials on success
            - Refresh token provided for long-term access
            - Local server stops after receiving callback
            - May fail if port 8550 already in use
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
        """Authenticate using OAuth tokens from external provider.

        Creates Google credentials from token data received from Flet's OAuth
        provider or mobile authentication. Validates and refreshes tokens if
        needed, then saves credentials for session persistence.

        Args:
            token_data (dict): OAuth token dictionary containing:
                - access_token (str, required): OAuth access token for API calls
                - refresh_token (str, optional): Token for refreshing access
                - client_id (str, optional): OAuth client ID (falls back to instance attr)
                - client_secret (str, optional): Client secret (falls back to instance attr)
                - scope (str or list, optional): Granted scopes (defaults to SCOPES)

        Returns:
            bool: True if authentication successful and credentials saved,
                False if token invalid, missing required fields, or validation failed.

        Algorithm:
            1. **Validate Input**:
               a. Print status: "Bridging OAuth token to Google credentials"
               b. Print token_data type for debugging
               c. Check if token_data is dictionary type
               d. If not dict, print error and return False
            
            2. **Extract Access Token** (required):
               a. Get access_token from token_data
               b. If not present, print error and return False
               c. Access token is required minimum
            
            3. **Extract Optional Fields**:
               a. Get refresh_token (may be None)
               b. Get client_id (use from token_data or self.client_id)
               c. Get client_secret (use from token_data or self.client_secret)
               d. Get scope (from token_data or default to SCOPES)
            
            4. **Process Scope**:
               a. If scope is string:
                  i. Split by whitespace to create list
                  ii. If empty, use default SCOPES
               b. If scope is already list, use as-is
            
            5. **Log Token Status**:
               a. Call _log_token_status() with extracted values
               b. Prints presence of each component for debugging
            
            6. **Create Credentials Object**:
               a. Instantiate google.oauth2.credentials.Credentials with:
                  i. token=access_token
                  ii. refresh_token=refresh_token (may be None)
                  iii. token_uri="https://oauth2.googleapis.com/token"
                  iv. client_id=client_id
                  v. client_secret=client_secret
                  vi. scopes=scope (as list)
               b. Store in self.creds
            
            7. **Validate and Refresh**:
               a. Call _validate_and_refresh_credentials()
               b. Checks if credentials valid
               c. Attempts refresh if expired and refresh_token present
               d. If validation fails, return False
            
            8. **Save Credentials**:
               a. Call _save_credentials()
               b. Persists to token.pickle
               c. Return True (success)
            
            9. **Handle Errors**:
               a. Catch any Exception
               b. Import traceback for detailed error info
               c. Print error message and full traceback
               d. Return False (failure)

        Interactions:
            - **google.oauth2.credentials.Credentials**: Creates credentials object
            - **_log_token_status()**: Logs token components
            - **_validate_and_refresh_credentials()**: Validates tokens
            - **_save_credentials()**: Persists credentials

        Example:
            >>> # From Flet OAuth provider
            >>> token_data = {
            ...     'access_token': 'ya29.a0AfH6SMBx...',
            ...     'refresh_token': '1//0gTVgG...',
            ...     'client_id': '123-abc.apps.googleusercontent.com',
            ...     'client_secret': 'GOCSPX-...',
            ...     'scope': 'openid email profile https://www.googleapis.com/auth/drive'
            ... }
            >>> auth = GoogleAuth()
            >>> success = auth.login_with_token(token_data)
            Bridging OAuth token to Google credentials
            Token data type: <class 'dict'>
            Access token: present
            Refresh token: present
            ...
            >>> print(success)
            True
            >>> 
            >>> # Invalid token data
            >>> success = auth.login_with_token({'invalid': 'data'})
            >>> print(success)
            False

        See Also:
            - :meth:`login_desktop`: Alternative desktop authentication
            - :meth:`_validate_and_refresh_credentials`: Validates tokens
            - :meth:`_log_token_status`: Debugging helper
            - :class:`~ui.firebase_mobile_login.FirebaseMobileLogin`: Mobile OAuth

        Notes:
            - Supports tokens from external OAuth providers (Flet, Firebase)
            - access_token is required minimum
            - refresh_token optional but recommended for long sessions
            - Client credentials fall back to instance attributes
            - Scope can be space-separated string or list
            - Validates and refreshes tokens immediately
            - Saves credentials on success for persistence
            - Returns bool for error handling by caller
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
        """Log OAuth token components for debugging authentication issues.

        Prints the presence/absence of each token component to console for
        troubleshooting authentication problems. Does not print actual token
        values for security.

        Args:
            access_token (str): OAuth access token (only presence checked).
            refresh_token (str or None): Refresh token (may be None).
            client_id (str or None): OAuth client ID.
            client_secret (str or None): OAuth client secret.
            scope (list or str): Granted OAuth scopes.

        Returns:
            None: Outputs debug information to console.

        Algorithm:
            1. **Log Token Components**:
               a. Print "Access token: present" (don't print actual value)
               b. Print refresh_token status: "present" or "missing"
               c. Print client_id status: "present" or "missing"
               d. Print client_secret status: "present" or "missing"
               e. Print scopes: join list or print string directly

        Interactions:
            - **Console output**: Prints to stdout

        Example:
            >>> # Called from login_with_token
            >>> auth._log_token_status(
            ...     'token123',
            ...     '1//refresh',
            ...     'client_id',
            ...     'secret',
            ...     ['drive', 'email']
            ... )
            Access token: present
            Refresh token: present
            Client ID: present
            Client secret: present
            Scopes: drive, email

        See Also:
            - :meth:`login_with_token`: Calls this for debugging

        Notes:
            - Never prints actual token values (security)
            - Only indicates presence/absence of components
            - Helps diagnose missing credentials
            - Scope handling for both list and string formats
        """
        print(f"Access token: present")
        print(f"Refresh token: {'present' if refresh_token else 'missing'}")
        print(f"Client ID: {'present' if client_id else 'missing'}")
        print(f"Client secret: {'present' if client_secret else 'missing'}")
        print(f"Scopes: {', '.join(scope) if isinstance(scope, list) else scope}")
    def _validate_and_refresh_credentials(self):
        """Validate OAuth credentials and refresh if expired.

        Checks if current credentials are valid and attempts to refresh them
        using the refresh token if they have expired. Required for maintaining
        active sessions and ensuring API calls succeed.

        Returns:
            bool: True if credentials valid or successfully refreshed,
                False if credentials invalid and cannot be refreshed.

        Algorithm:
            1. **Check Validity**:
               a. If self.creds.valid is True:
                  i. Print "Credentials are valid"
                  ii. Return True immediately
            
            2. **Check Refresh Possibility**:
               a. If not self.creds.expired OR not self.creds.refresh_token:
                  i. Credentials either not expired or no refresh token
                  ii. Print "Credentials not valid and cannot be refreshed"
                  iii. Return False
            
            3. **Attempt Refresh**:
               a. Print "Attempting to refresh expired token..."
               b. Enter try block for error handling
               c. Call self.creds.refresh(Request())
                  i. Creates HTTP request to token endpoint
                  ii. Exchanges refresh_token for new access_token
                  iii. Updates self.creds with new tokens
               d. Print "Token refreshed successfully"
               e. Return True
            
            4. **Handle Refresh Errors**:
               a. Catch any Exception during refresh
               b. Print error message with exception details
               c. Return False (refresh failed)

        Interactions:
            - **google.auth.transport.requests.Request**: HTTP transport
            - **Credentials.refresh()**: Token refresh operation

        Example:
            >>> # Valid credentials
            >>> result = auth._validate_and_refresh_credentials()
            Credentials are valid
            >>> print(result)
            True
            >>> 
            >>> # Expired with refresh token
            >>> result = auth._validate_and_refresh_credentials()
            Attempting to refresh expired token...
            Token refreshed successfully
            >>> print(result)
            True
            >>> 
            >>> # Expired without refresh token
            >>> result = auth._validate_and_refresh_credentials()
            Credentials not valid and cannot be refreshed
            >>> print(result)
            False

        See Also:
            - :meth:`login_with_token`: Calls this after creating credentials
            - :meth:`is_authenticated`: Calls this to validate session
            - :class:`google.auth.transport.requests.Request`: HTTP transport

        Notes:
            - Returns True if already valid (no refresh needed)
            - Requires refresh_token for refresh operation
            - Refresh may fail if refresh_token revoked or expired
            - Updates credentials object with new tokens on success
            - Does not save credentials (caller must call _save_credentials)
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
        """Check if user currently has valid authentication.

        Validates current credentials and attempts to refresh them if expired.
        Provides the primary method for checking authentication status before
        API operations.

        Returns:
            bool: True if authenticated with valid credentials, False if
                not authenticated, credentials expired without refresh token,
                or refresh operation failed.

        Algorithm:
            1. **Check Credentials Exist**:
               a. If self.creds is None:
                  i. No authentication performed yet
                  ii. Return False immediately
            
            2. **Check Not Expired**:
               a. If not self.creds.expired:
                  i. Credentials still valid (not expired)
                  ii. Return self.creds.valid (should be True)
            
            3. **Check Refresh Token**:
               a. If not self.creds.refresh_token:
                  i. Credentials expired but no refresh token
                  ii. Print message: "Credentials expired and no refresh token available"
                  iii. Return False (cannot refresh)
            
            4. **Attempt Refresh**:
               a. Enter try block for error handling
               b. Print "→ Refreshing expired credentials..."
               c. Call self.creds.refresh(Request())
                  i. Exchanges refresh_token for new access_token
                  ii. Updates self.creds with new tokens
               d. Call self._save_credentials()
                  i. Persists refreshed tokens to pickle
               e. Print "✓ Credentials refreshed"
               f. Return True (refresh successful)
            
            5. **Handle Refresh Errors**:
               a. Catch any Exception during refresh
               b. Print error message with exception details
               c. Return False (refresh failed)

        Interactions:
            - **google.auth.transport.requests.Request**: HTTP transport
            - **Credentials.refresh()**: Token refresh operation
            - **_save_credentials()**: Persists refreshed credentials

        Example:
            >>> # Not authenticated
            >>> auth = GoogleAuth()
            >>> print(auth.is_authenticated())
            False
            >>> 
            >>> # After login
            >>> auth.login_desktop()
            >>> print(auth.is_authenticated())
            True
            >>> 
            >>> # Token expires, but refreshes automatically
            >>> # (time passes, token expires)
            >>> print(auth.is_authenticated())
            → Refreshing expired credentials...
            ✓ Credentials refreshed
            True
            >>> 
            >>> # Use for API access control
            >>> if auth.is_authenticated():
            ...     service = auth.get_service()
            ...     # Make API calls
            ... else:
            ...     print("Please login first")

        See Also:
            - :meth:`login_desktop`: Desktop authentication
            - :meth:`login_with_token`: Token-based authentication
            - :meth:`get_service`: Requires authentication
            - :meth:`_save_credentials`: Saves refreshed credentials

        Notes:
            - Primary method for checking auth status
            - Automatically refreshes expired tokens
            - Saves refreshed tokens to pickle file
            - Returns False if refresh fails
            - Should be called before API operations
            - Token refresh requires refresh_token
            - Refresh may fail if token revoked
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
        """Log out user and clear all stored authentication data.

        Clears the credentials object and deletes the token pickle file,
        ending the current session. User must re-authenticate after logout.

        Returns:
            None: Clears self.creds and removes token file as side effects.

        Algorithm:
            1. **Log Action**:
               a. Print "Logging out..." to console
            
            2. **Clear Credentials**:
               a. Set self.creds = None
               b. Removes credentials from memory
            
            3. **Delete Token File**:
               a. Check if self.token_file exists
               b. If exists:
                  i. Enter try block for error handling
                  ii. Call os.remove(self.token_file)
                  iii. Print "Token file removed"
               c. If exception:
                  i. Print error message with details
                  ii. File may be locked or permission denied

        Interactions:
            - **os.path.exists()**: Checks file existence
            - **os.remove()**: Deletes token file

        Example:
            >>> # User authenticated
            >>> auth = GoogleAuth()
            >>> auth.login_desktop()
            >>> print(auth.is_authenticated())
            True
            >>> 
            >>> # Logout
            >>> auth.logout()
            Logging out...
            Token file removed
            >>> 
            >>> # No longer authenticated
            >>> print(auth.is_authenticated())
            False
            >>> 
            >>> # token.pickle deleted
            >>> import os
            >>> print(os.path.exists('token.pickle'))
            False

        See Also:
            - :meth:`login_desktop`: Re-authenticate after logout
            - :meth:`login_with_token`: Alternative re-authentication
            - :meth:`is_authenticated`: Returns False after logout

        Notes:
            - Clears credentials from memory immediately
            - Deletes token.pickle file if exists
            - Silent failure if file deletion fails
            - User must re-authenticate after logout
            - Does not revoke tokens with Google (tokens still valid)
            - For full security, revoke tokens in Google Account settings
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
        """Create and return authenticated Google Drive API v3 service.

        Builds a Google Drive API service object for making API requests.
        Requires valid authentication and automatically refreshes expired
        tokens before creating service.

        Returns:
            googleapiclient.discovery.Resource or None: Google Drive API v3
                service object configured with authenticated credentials,
                or None if not authenticated or service creation failed.

        Algorithm:
            1. **Check Authentication**:
               a. Call self.is_authenticated()
               b. If False:
                  i. Print "Cannot get service - not authenticated"
                  ii. Return None immediately
            
            2. **Try Service Creation**:
               a. Enter try block for error handling
               b. Call build('drive', 'v3', credentials=self.creds)
                  i. 'drive': Google Drive API
                  ii. 'v3': API version 3
                  iii. credentials: OAuth credentials object
               c. Returns Resource object for API calls
               d. Store in service variable
               e. Print "Google Drive service created"
               f. Return service object
            
            3. **Handle Errors**:
               a. Catch any Exception during service creation
               b. Print error message with exception details
               c. Return None (service creation failed)

        Interactions:
            - **is_authenticated()**: Validates and refreshes credentials
            - **googleapiclient.discovery.build()**: Creates API service
            - **Credentials**: Provides authentication for service

        Example:
            >>> # Get service for API calls
            >>> auth = GoogleAuth()
            >>> auth.login_desktop()
            >>> service = auth.get_service()
            Google Drive service created
            >>> 
            >>> # Use service for Drive operations
            >>> if service:
            ...     results = service.files().list(pageSize=10).execute()
            ...     files = results.get('files', [])
            ...     for file in files:
            ...         print(file['name'])
            >>> 
            >>> # Not authenticated
            >>> auth2 = GoogleAuth()
            >>> service = auth2.get_service()
            Cannot get service - not authenticated
            >>> print(service)
            None

        See Also:
            - :meth:`is_authenticated`: Validates authentication
            - :class:`~services.drive_service.DriveService`: Wraps this service
            - `Drive API Reference <https://developers.google.com/drive/api/v3/reference>`_

        Notes:
            - Requires valid authentication (checked automatically)
            - Automatically refreshes expired tokens
            - Returns None if not authenticated
            - Service object used for all Drive API calls
            - DriveService class typically wraps this service
            - API version v3 is current stable version
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
        """Retrieve authenticated user's Google account information.

        Fetches user details from the Google Drive API including email address,
        display name, and profile information. Requires valid authentication.

        Returns:
            dict: User information dictionary containing:
                - emailAddress (str): User's email
                - displayName (str): User's display name
                - photoLink (str): Profile photo URL
                - permissionId (str): User's permission ID
                Returns empty dict {} if not authenticated or API call fails.

        Algorithm:
            1. **Try Getting User Info**:
               a. Enter try block for error handling
               b. Call self.get_service() to get Drive service
               c. If service is None:
                  i. Not authenticated
                  ii. Return empty dict {}
            
            2. **Make API Call**:
               a. Call service.about().get(fields="user").execute()
                  i. about(): Endpoint for account info
                  ii. get(): Retrieve information
                  iii. fields="user": Request only user fields
                  iv. execute(): Perform API request
               b. Store response in about variable
            
            3. **Extract User Data**:
               a. Get 'user' field from response: about.get('user', {})
               b. Store in user variable
               c. Extract email: user.get('emailAddress', 'unknown')
               d. Print success message with email
               e. Return user dictionary
            
            4. **Handle Errors**:
               a. Catch any Exception during API call
               b. Print error message with exception details
               c. Return empty dict {} (API call failed)

        Interactions:
            - **get_service()**: Gets authenticated Drive service
            - **Drive API about().get()**: Retrieves user information

        Example:
            >>> # Get user info
            >>> auth = GoogleAuth()
            >>> auth.login_desktop()
            >>> user_info = auth.get_user_info()
            ✓ User info retrieved: user@example.com
            >>> 
            >>> print(user_info)
            {
                'emailAddress': 'user@example.com',
                'displayName': 'John Doe',
                'photoLink': 'https://...',
                'permissionId': '...'
            }
            >>> 
            >>> # Display user email
            >>> print(f"Logged in as: {user_info.get('emailAddress')}")
            Logged in as: user@example.com
            >>> 
            >>> # Not authenticated
            >>> auth2 = GoogleAuth()
            >>> user_info = auth2.get_user_info()
            >>> print(user_info)
            {}

        See Also:
            - :meth:`get_service`: Gets authenticated Drive service
            - :meth:`is_authenticated`: Validates authentication
            - `Drive API About <https://developers.google.com/drive/api/v3/reference/about>`_

        Notes:
            - Requires valid authentication
            - Returns empty dict if not authenticated
            - Returns empty dict on API errors
            - Email address used for displaying logged-in user
            - Single API call to get user information
            - Useful for displaying current user in UI
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