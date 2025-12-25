"""Google Drive Service Module.

This module provides a high-level interface for Google Drive API operations
with built-in caching, retry logic, and error handling.

Classes:
    DriveService: Wrapper class for Google Drive API operations.

Example:
    >>> from services.auth_service import GoogleAuth
    >>> auth = GoogleAuth()
    >>> drive = DriveService(auth.get_service())
    >>> files = drive.list_files('root')

See Also:
    :class:`~src.services.auth_service.GoogleAuth`: Provides the API service.
"""

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from datetime import datetime, timedelta
from functools import lru_cache
import time
import io
from utils.common import extract_drive_id, format_file_size


class DriveService:
    """High-level wrapper for Google Drive API operations.

    Provides file and folder operations with caching, automatic retry,
    and optimized request handling for the Google Drive API.

    Attributes:
        service (googleapiclient.discovery.Resource): The Drive API service object.
        max_retries (int): Maximum retry attempts for failed requests.
        retry_delay (int): Base delay in seconds between retries.

    Algorithm (Pseudocode):
        1. Initialize with Drive API service and cache settings
        2. For read operations: check cache first, query API if miss
        3. For write operations: execute with retry, invalidate cache
        4. Use exponential backoff for transient failures

    See Also:
        :class:`~src.services.auth_service.GoogleAuth`: Creates the API service.
        :class:`~src.ui.dashboard.Dashboard`: Primary consumer of DriveService.
    """
    
    def __init__(self, service, cache_ttl=300, max_retries=3):
        """Initialize the DriveService wrapper.

        Args:
            service (googleapiclient.discovery.Resource): Google Drive API service.
            cache_ttl (int, optional): Cache time-to-live in seconds. Defaults to 300.
            max_retries (int, optional): Maximum retry attempts. Defaults to 3.

        Algorithm (Pseudocode):
            1. Store service reference
            2. Initialize cache dictionary
            3. Set retry parameters
            4. Setup LRU caches for file info
        """
        self.service = service
        self._cache = {}
        self._cache_ttl = cache_ttl
        self.max_retries = max_retries
        self.retry_delay = 1
        self._setup_lru_caches()
    
    def _setup_lru_caches(self):
        """Set up LRU caches for frequently accessed data.

        Creates cached wrapper for get_file_info to reduce API calls.
        """
        @lru_cache(maxsize=128)
        def cached_get_file_info(file_id):
            return self.get_file_info(file_id, use_cache=False)
        self._cached_get_file_info = cached_get_file_info
    
    def _get_cached(self, key):
        """Retrieve data from cache if not expired.

        Args:
            key (str): Cache key to look up.

        Returns:
            Any: Cached data if valid, None if expired or not found.
        """
        if key in self._cache:
            data, timestamp = self._cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self._cache_ttl):
                return data
            del self._cache[key]
        return None
    
    def _set_cache(self, key, data):
        """Store data in cache with timestamp.

        Args:
            key (str): Cache key for storage.
            data (Any): Data to cache.
        """
        self._cache[key] = (data, datetime.now())
    
    def _invalidate_cache(self, folder_id=None):
        """Clear cached data for a folder or entire cache.

        Args:
            folder_id (str, optional): Specific folder to invalidate.
                If None, clears entire cache.
        """
        if folder_id:
            keys_to_remove = [k for k in self._cache.keys() if folder_id in k]
            for key in keys_to_remove:
                del self._cache[key]
            if hasattr(self, '_cached_get_file_info'):
                try:
                    self._cached_get_file_info.cache_clear()
                except:
                    pass
        else:
            self._cache.clear()
            if hasattr(self, '_cached_get_file_info'):
                self._cached_get_file_info.cache_clear()
    
    def _retry_request(self, request_func, operation_name="operation"):
        """Execute request with exponential backoff retry.

        Args:
            request_func (Callable): Function to execute.
            operation_name (str): Name for logging.

        Returns:
            Any: Request result or None on failure.

        Algorithm (Pseudocode):
            1. Try request up to max_retries times
            2. On retryable error, wait with exponential backoff
            3. Return result or None if all retries fail
        """
        for attempt in range(self.max_retries):
            try:
                return request_func()
            except (TimeoutError, HttpError, Exception) as error:
                should_retry = (
                    isinstance(error, TimeoutError) or
                    (isinstance(error, HttpError) and error.resp.status in [429, 500, 503]) or
                    (not isinstance(error, HttpError) and attempt < self.max_retries - 1)
                )
                
                if should_retry and attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)
                    print(f"Error on {operation_name} (attempt {attempt + 1}/{self.max_retries}), retrying in {delay}s...")
                    time.sleep(delay)
                else:
                    print(f"Final error on {operation_name}: {error}")
                    return None
        return None
    
    def _execute_file_list_query(self, query, page_size=100, page_token=None, fields="nextPageToken, files(id, name, mimeType, modifiedTime, size, owners)", order_by="folder,name"):
        """Execute a files.list query with retry.

        Args:
            query (str): Drive API query string.
            page_size (int): Results per page.
            page_token (str, optional): Pagination token.
            fields (str): API fields to return.
            order_by (str): Sort order.

        Returns:
            dict: API response with files list.
        """
        def make_request():
            return self.service.files().list(
                q=query,
                pageSize=page_size,
                pageToken=page_token,
                fields=fields,
                orderBy=order_by
            ).execute()
        
        return self._retry_request(make_request, f"list_query({query[:50]})")
    
    def list_files(self, folder_id='root', page_size=100, page_token=None, use_cache=True):
        """List files in a folder.

        Args:
            folder_id (str): Folder ID to list. Defaults to 'root'.
            page_size (int): Results per page. Defaults to 100.
            page_token (str, optional): Pagination token.
            use_cache (bool): Whether to use cached results.

        Returns:
            dict: Contains 'files' list and 'nextPageToken'.
        """
        cache_key = f"files_{folder_id}_{page_size}_{page_token}"
        
        if use_cache:
            cached = self._get_cached(cache_key)
            if cached:
                print(f"Cache hit for {cache_key}")
                return cached
        
        query = f"'{folder_id}' in parents and trashed=false"
        result = self._execute_file_list_query(query, page_size, page_token)
        
        if result is not None:
            formatted_result = {
                'files': result.get('files', []),
                'nextPageToken': result.get('nextPageToken', None)
            }
            self._set_cache(cache_key, formatted_result)
            return formatted_result
        
        return None
    
    def search_files(self, query_text, folder_id=None, use_cache=False):
        """Search for files by name.

        Args:
            query_text (str): Text to search for in file names.
            folder_id (str, optional): Limit search to folder.
            use_cache (bool): Whether to cache results.

        Returns:
            list: Matching file objects.
        """
        cache_key = f"search_{query_text}_{folder_id}"
        
        if use_cache:
            cached = self._get_cached(cache_key)
            if cached:
                return cached
        
        query = f"name contains '{query_text}' and trashed=false"
        if folder_id:
            query += f" and '{folder_id}' in parents"
        
        result = self._execute_file_list_query(query, page_size=50, fields="files(id, name, mimeType, modifiedTime, parents)")
        files = result.get('files', []) if result else []
        
        if use_cache and files:
            self._set_cache(cache_key, files)
        
        return files
    
    def get_file_info(self, file_id, use_cache=True):
        """Get detailed information about a file.

        Args:
            file_id (str): The Drive file ID.
            use_cache (bool): Whether to use cached info.

        Returns:
            dict: File metadata including id, name, mimeType, size, etc.
        """
        if use_cache and hasattr(self, '_cached_get_file_info'):
            try:
                return self._cached_get_file_info(file_id)
            except:
                pass
        
        cache_key = f"fileinfo_{file_id}"
        
        if use_cache:
            cached = self._get_cached(cache_key)
            if cached:
                return cached
        
        def make_request():
            return self.service.files().get(
                fileId=file_id,
                fields="id, name, mimeType, size, createdTime, modifiedTime, owners, parents, webViewLink"
            ).execute()
        
        file = self._retry_request(make_request, f"get_file_info({file_id})")
        
        if file is not None:
            self._set_cache(cache_key, file)
        
        return file

    def resolve_drive_link(self, link):
        """Resolve a Drive URL to file ID and info.

        Args:
            link (str): Google Drive URL or file ID.

        Returns:
            tuple: (file_id, file_info) or (None, None) on failure.
        """
        file_id = extract_drive_id(link)
        
        if not file_id:
            print(f"Could not extract file ID from link: {link}")
            return None, None
        
        info = self.get_file_info(file_id)
        
        if not info:
            print(f"Could not retrieve file info for ID: {file_id}")
            return None, None
        
        return file_id, info
    
    def _execute_file_mutation(self, operation_name, request_func, parent_id=None):
        """Execute a mutation operation with cache invalidation.

        Args:
            operation_name (str): Name for logging.
            request_func (Callable): The mutation function.
            parent_id (str, optional): Parent folder to invalidate.

        Returns:
            Any: Operation result.
        """
        result = self._retry_request(request_func, operation_name)
        
        if result and parent_id:
            self._invalidate_cache(parent_id)
        
        return result
    
    def create_folder(self, folder_name, parent_id='root'):
        """Create a new folder.

        Args:
            folder_name (str): Name for the new folder.
            parent_id (str): Parent folder ID. Defaults to 'root'.

        Returns:
            dict: Created folder info with id and name.
        """
        def make_request():
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_id]
            }
            return self.service.files().create(
                body=file_metadata,
                fields='id, name'
            ).execute()
        
        return self._execute_file_mutation(f"create_folder({folder_name})", make_request, parent_id)
    
    def upload_file(self, file_path, parent_id='root', file_name=None, progress_callback=None):
        """Upload a file to Drive.

        Args:
            file_path (str): Local path to file.
            parent_id (str): Destination folder ID.
            file_name (str, optional): Name in Drive. Uses local name if None.
            progress_callback (Callable, optional): Progress handler(current, total).

        Returns:
            dict: Uploaded file info or None on failure.
        """
        try:
            if not file_name:
                import os
                file_name = os.path.basename(file_path)
                
            file_metadata = {
                'name': file_name,
                'parents': [parent_id]
            }
            
            media = MediaFileUpload(file_path, resumable=True)
            
            request = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, mimeType, size, webViewLink, parents'
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status and progress_callback:
                    progress_callback(status.resumable_progress, status.total_size)
            
            self._invalidate_cache(parent_id)
            
            return response
            
        except Exception as error:
            print(f"Error uploading file: {error}")
            return None
    
    def update_file(self, file_id, file_path, new_name=None):
        """Update an existing file's content.

        Args:
            file_id (str): File ID to update.
            file_path (str): Path to new content.
            new_name (str, optional): New filename.

        Returns:
            dict: Updated file info or None on failure.
        """
        try:
            file_metadata = {}
            if new_name:
                file_metadata['name'] = new_name
            
            media = MediaFileUpload(file_path, resumable=True)
            
            updated_file = self.service.files().update(
                fileId=file_id,
                body=file_metadata,
                media_body=media,
                fields='id, name, mimeType, modifiedTime'
            ).execute()
            
            self._invalidate_cache(file_id)
            return updated_file
        except Exception as error:
            print(f"Error updating file: {error}")
            return None

    def read_file_content(self, file_id):
        """Download and read file content as text.

        Args:
            file_id (str): File ID to read.

        Returns:
            str: File content as UTF-8 string, or None on failure.
        """
        try:
            request = self.service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            
            return file.getvalue().decode('utf-8')
        except Exception as error:
            print(f"Error reading file content: {error}")
            return None

    def find_file(self, name, parent_id):
        """Find a file by exact name in a folder.

        Args:
            name (str): Exact filename to find.
            parent_id (str): Folder to search in.

        Returns:
            dict: File info if found, None otherwise.
        """
        query = f"name = '{name}' and '{parent_id}' in parents and trashed=false"
        results = self.service.files().list(
            q=query,
            pageSize=1,
            fields="files(id, name, mimeType, modifiedTime)"
        ).execute()
        files = results.get('files', [])
        return files[0] if files else None

    def move_file(self, file_id, new_parent_id):
        """Move a file to a different folder.

        Args:
            file_id (str): File to move.
            new_parent_id (str): Destination folder ID.

        Returns:
            dict: Updated file info or None on failure.
        """
        def make_request():
            file = self.service.files().get(
                fileId=file_id,
                fields='parents'
            ).execute()
            
            previous_parents = ",".join(file.get('parents', []))
            
            return self.service.files().update(
                fileId=file_id,
                addParents=new_parent_id,
                removeParents=previous_parents,
                fields='id, parents'
            ).execute()
        
        updated_file = self._retry_request(make_request, f"move_file({file_id})")
        
        if updated_file:
            file = self.service.files().get(fileId=file_id, fields='parents').execute()
            for parent in file.get('parents', []):
                self._invalidate_cache(parent)
            self._invalidate_cache(new_parent_id)
        
        return updated_file
    
    def rename_file(self, file_id, new_name):
        """Rename a file.

        Args:
            file_id (str): File to rename.
            new_name (str): New filename.

        Returns:
            dict: Updated file info or None on failure.
        """
        def make_request():
            file_metadata = {'name': new_name}
            return self.service.files().update(
                fileId=file_id,
                body=file_metadata,
                fields='id, name, parents'
            ).execute()
        
        updated_file = self._retry_request(make_request, f"rename_file({file_id})")
        
        if updated_file:
            for parent in updated_file.get('parents', []):
                self._invalidate_cache(parent)
            self._invalidate_cache(file_id)
        
        return updated_file
    
    def delete_file(self, file_id):
        """Delete a file or folder.

        Args:
            file_id (str): File or folder to delete.

        Returns:
            bool: True if deleted successfully.
        """
        file_info = self.get_file_info(file_id, use_cache=False)
        
        def make_request():
            self.service.files().delete(fileId=file_id).execute()
            return True
        
        success = self._retry_request(make_request, f"delete_file({file_id})")
        
        if success:
            if file_info and 'parents' in file_info:
                for parent in file_info['parents']:
                    self._invalidate_cache(parent)
            self._invalidate_cache(file_id)
            return True
        
        return False
    
    def get_folder_tree(self, folder_id='root', max_depth=2, current_depth=0):
        """Get recursive folder structure.

        Args:
            folder_id (str): Root folder ID.
            max_depth (int): Maximum recursion depth.
            current_depth (int): Current depth (internal).

        Returns:
            list: Folder tree with nested 'children' lists.
        """
        if current_depth >= max_depth:
            return None
        
        query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
        result = self._execute_file_list_query(query, page_size=100, fields="files(id, name)", order_by="name")
        folders = result.get('files', []) if result else []
        
        for folder in folders:
            folder['children'] = self.get_folder_tree(
                folder['id'], 
                max_depth, 
                current_depth + 1
            )
        
        return folders