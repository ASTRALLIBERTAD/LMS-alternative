"""Data Manager Module.

This module helps persist the application state (assignments, students, submissions)
to both local storage (json files) and Google Drive (if enabled). It ensures synchronization
between the local cache and the cloud backend.

Classes:
    DataManager: Handles I/O operations for LMS data entities.
"""

from pathlib import Path
from utils.common import load_json_file, save_json_file
import datetime


class DataManager:
    """Manages data persistence for the LMS application.

    Purpose / Responsibility:
        Orchestrates storage and retrieval of application state (Assignments, Students, Submissions).
        It abstracts the backend implementation, seamlessly handling both local JSON files
        and cloud synchronization via Google Drive when available.

    Attributes:
        data_dir (Path): Local file system path for storing JSON data files.
        drive_service (DriveService): Instance of the Drive service for cloud operations.
        lms_root_id (str): The ID of the root LMS folder in Google Drive.
        assignments_file (Path): Path to the local assignments JSON file.
        students_file (Path): Path to the local students JSON file.
        submissions_file (Path): Path to the local submissions JSON file.

    Interactions / Calls:
        - Calls `src.services.drive_service.DriveService` for upload/download/find.
        - Uses `utils.common.load_json_file` and `save_json_file`.
        - Reads `lms_config.json`.

    Algorithm / Pseudocode:
        1. Initialize with local directory.
        2. Load config to get Drive folder ID.
        3. Define paths for data entities.
        4. `_load_from_drive_or_local`:
           a. If Drive connected: Check cloud file -> Download -> Parse.
           b. Else/Fallback: Read local JSON.
        5. `_save_to_local_and_drive`:
           a. Write to local JSON.
           b. If Drive connected: Update existing file or Upload new one.

    Examples:
        >>> dm = DataManager("data", drive_service)
        >>> assignments = dm.load_assignments()
        >>> dm.save_students(student_list)

    See Also:
        - :class:`~src.services.drive_service.DriveService`
        - :func:`~src.utils.common.load_json_file`
    """
    
    def __init__(self, data_dir, drive_service=None):
        """Initialize the DataManager.

        Purpose:
            Sets up file paths and initial configuration for data storage.

        Args:
            data_dir (str | Path): Directory path for local data storage.
            drive_service (DriveService, optional): Service instance for Drive syncing.

        Interactions:
            - Calls `_load_lms_root_id` to fetch configuration.
            - Sets public attributes for file paths.
        """
        self.data_dir = Path(data_dir) if isinstance(data_dir, str) else data_dir
        self.drive_service = drive_service
        self.lms_root_id = self._load_lms_root_id()
        
        self.assignments_file = self.data_dir / "assignments.json"
        self.students_file = self.data_dir / "students.json"
        self.submissions_file = self.data_dir / "submissions.json"
    
    def _load_lms_root_id(self):
        """Read the LMS root folder ID from local config.

        Purpose:
            Retrieves the Google Drive Folder ID used as the root for LMS data.

        Returns:
            str | None: The folder ID if configured, else None.

        Interactions:
            - Reads `lms_config.json` via `load_json_file`.
        """
        
        config = load_json_file("lms_config.json", {})
        return config.get("lms_root_id")
    
    def _load_from_drive_or_local(self, filepath, default=None):
        """Load data from Drive if available, falling back to local file.

        Purpose:
            Ensures the most up-to-date data is loaded, preferring the cloud version
            if connected to Google Drive to support cross-device usage.

        Args:
            filepath (Path): Local path where the file is expected to be.
            default (any, optional): Value to return if data cannot be loaded. Defaults to None.

        Returns:
            any: Parsed JSON data (list or dict), or default value.

        Interactions:
            - Calls `drive_service.find_file`.
            - Calls `drive_service.read_file_content`.
            - Calls `utils.common.load_json_file`.

        Algorithm:
            1. Check if Drive Service and Root ID are available.
            2. If yes:
               a. Search for file by name in LMS root folder.
               b. If found, download content string.
               c. Parse JSON and return.
            3. Fallback: Load directly from local file path.
        """
        if self.drive_service and self.lms_root_id:
            filename = filepath.name
            try:
                file = self.drive_service.find_file(filename, self.lms_root_id)
                if file:
                    content = self.drive_service.read_file_content(file['id'])
                    if content:
                        import json
                        return json.loads(content)
            except Exception as e:
                print(f"Error loading from Drive: {e}")
        
        return load_json_file(filepath, default)
    
    def _save_to_local_and_drive(self, filepath, data):
        """Save data locally and sync to Drive if connected.

        Purpose:
            Persists data to disk and synchronizes changes to the cloud backend.

        Args:
            filepath (Path): Target local file path.
            data (any): Python object (dict/list) to serialize and save.

        Interactions:
            - Calls `utils.common.save_json_file`.
            - Calls `drive_service.find_file`.
            - Calls `drive_service.update_file` or `drive_service.upload_file`.

        Algorithm:
            1. Save data to local JSON file immediately.
            2. Check if Drive Service is connected.
            3. If yes:
               a. Search for file by name in Drive root.
               b. If found -> Update file content.
               c. If not found -> Upload new file.
        """
        save_json_file(filepath, data)
        
        if self.drive_service and self.lms_root_id:
            filename = filepath.name
            try:
                existing = self.drive_service.find_file(filename, self.lms_root_id)
                if existing:
                    self.drive_service.update_file(existing['id'], str(filepath))
                else:
                    self.drive_service.upload_file(str(filepath), parent_id=self.lms_root_id)
            except Exception as e:
                print(f"Error saving to Drive: {e}")
    
    def load_assignments(self):
        """Load list of assignments.

        Purpose:
            Retrieves assignment data and ensures data integrity (assigning IDs if missing).

        Returns:
            list[dict]: List of assignment objects.

        Interactions:
            - Calls `_load_from_drive_or_local`.
            - Calls `save_assignments` (if integrity repair needed).

        Algorithm:
            1. Load data via `_load_from_drive_or_local`.
            2. Iterate through assignments.
            3. Check if 'id' exists; if not, generate one based on timestamp.
            4. If any IDs generated, save the repaired list.
            5. Return list.
        """
        assignments = self._load_from_drive_or_local(self.assignments_file, [])
        
        modified = False
        for i, assignment in enumerate(assignments):
            if 'id' not in assignment:
                assignment['id'] = str(datetime.datetime.now().timestamp()) + str(i)
                modified = True
        
        if modified:
            self.save_assignments(assignments)
        
        return assignments
    
    def load_students(self):
        """Load list of registered students.

        Purpose:
            Retrieves student registry data.

        Returns:
            list[dict]: List of student objects.

        Interactions:
            - Calls `_load_from_drive_or_local`.
        """
        return self._load_from_drive_or_local(self.students_file, [])
    
    def load_submissions(self):
        """Load list of submissions.

        Purpose:
            Retrieves all submission records.

        Returns:
            list[dict]: List of submission objects.

        Interactions:
            - Calls `_load_from_drive_or_local`.
        """
        return self._load_from_drive_or_local(self.submissions_file, [])
    
    def save_assignments(self, assignments):
        """Persist assignment list to storage.

        Purpose:
            Saves the current state of assignments.

        Args:
            assignments (list[dict]): The list of assignments to save.

        Interactions:
            - Calls `_save_to_local_and_drive`.
        """
        self._save_to_local_and_drive(self.assignments_file, assignments)
    
    def save_students(self, students):
        """Persist student list to storage.

        Purpose:
            Saves the current registry of students.

        Args:
            students (list[dict]): The list of students to save.

        Interactions:
            - Calls `_save_to_local_and_drive`.
        """
        self._save_to_local_and_drive(self.students_file, students)
    
    def save_submissions(self, submissions):
        """Persist submissions list to storage.

        Purpose:
            Saves the current state of all submissions.

        Args:
            submissions (list[dict]): The list of submissions to save.

        Interactions:
            - Calls `_save_to_local_and_drive`.
        """
        self._save_to_local_and_drive(self.submissions_file, submissions)