"""Submission Manager Module.

This module handles the student submission flow and the teacher grading interface.
It manages file uploads for submissions, calculation of submission timing (early/late),
and the grading/feedback loop.

Classes:
    SubmissionManager: Manages assignment submissions and grading.
"""

import flet as ft
import datetime


class SubmissionManager:
    """Manages the submission and grading process for student assignments.

    The SubmissionManager class orchestrates the complete lifecycle of assignment
    submissions in an educational application. It provides a dual-interface system:
    a student-facing submission portal for uploading work with notes, and a 
    teacher-facing grading interface for evaluating submissions and providing feedback.
    
    This class integrates with Google Drive for file storage, calculates submission
    timing metrics (early/late relative to deadlines), and manages the persistent
    storage of submission records and grades through the DataManager.

    Purpose:
        - Enable students to submit assignment files with optional notes
        - Provide teachers with a comprehensive grading interface
        - Calculate and display submission timing (early/late) relative to deadlines
        - Manage file uploads to Google Drive with organized folder structures
        - Persist submission data and grades across application sessions
        - Support file preview functionality for submitted work

    Attributes:
        todo (TodoView): Reference to the parent TodoView instance, providing access
            to shared services, data stores, and UI components.
        temp_file_path (str or None): Temporary storage for file path during upload
            operations. Reset after each submission.
        temp_file_name (str or None): Temporary storage for file name during upload
            operations. Reset after each submission.
        file_preview (FilePreviewService or None): Service instance for rendering
            file previews in overlays. None if import fails or service unavailable.

    Interactions:
        - **TodoView**: Parent class providing access to page, data_manager, 
          drive_service, storage_manager, student_manager, and UI utilities
        - **DataManager**: Persists submission records via save_submissions()
        - **DriveService**: Handles Google Drive file operations and folder queries
        - **StorageManager**: Uploads files to Drive with organized naming conventions
        - **StudentManager**: Retrieves filtered student lists (bridging/regular/all)
        - **FilePreviewService**: Renders file previews in modal overlays

    Algorithm (High-Level Workflow):
        **Phase 1: Initialization**
            1. Receive TodoView instance reference containing all shared services
            2. Initialize temporary file storage attributes (temp_file_path, temp_file_name)
            3. Attempt to import FilePreviewService from services module
            4. If import successful, instantiate service with page and drive_service
            5. If import fails, set file_preview to None (graceful degradation)
        
        **Phase 2: Student Submission Process** (submit_assignment_dialog)
            1. Validate that Google Drive service is connected and available
            2. Verify that assignment has a linked Drive folder ID
            3. Display submission dialog with assignment details and subject
            4. Initialize folder display showing the target upload location
            5. Provide optional folder browser for subfolder selection
            6. Present file picker for student to select assignment file
            7. When file selected, extract file path, name, and student identifier
            8. Upload file to Drive using StorageManager with student name prefix
            9. Retrieve existing submission record or create new submission object
            10. Populate submission with file metadata (id, name, link) and timestamp
            11. Update or append submission to submissions list
            12. Persist changes through DataManager.save_submissions()
            13. Refresh UI to display updated submission status
            14. Show success notification and auto-close dialog after 1 second
        
        **Phase 3: Teacher Grading Process** (view_submissions_dialog)
            1. Create scrollable dialog container for submission cards
            2. Retrieve assignment's target_for filter (all/bridging/regular students)
            3. Call StudentManager to get filtered list of target students
            4. Initialize submission counter for tracking submitted vs total
            5. For each student in target list:
               a. Search submissions list for matching assignment_id and student_email
               b. If submission exists:
                  - Increment submitted counter
                  - Calculate submission timing using calculate_submission_timing()
                  - Determine if already graded (has grade or feedback)
                  - If graded and not force_edit: display read-only grade view
                  - If not graded or force_edit matches: display editable grade fields
                  - Add file preview and browser links if file available
                  - Create green-themed card with all submission details
               c. If submission missing:
                  - Create red-themed card with "Missing" status
               d. Append card to submissions list container
            6. Insert submission count summary at top of dialog
            7. When "Save Grade" clicked:
               a. Disable save button to prevent double-submission
               b. Update submission record with grade and feedback
               c. Add graded_at timestamp
               d. Persist via DataManager.save_submissions()
               e. Close dialog and reopen to show read-only view
            8. When "Edit Grade" clicked:
               a. Close current dialog
               b. Reopen with force_edit_email parameter set
               c. This switches from read-only to edit mode
        
        **Phase 4: Timing Calculation** (calculate_submission_timing)
            1. Validate that both submitted_at and deadline strings are provided
            2. Return (None, "No timing data") if either parameter is missing
            3. Parse submitted_at timestamp:
               - If contains 'T', parse as ISO 8601 format
               - Otherwise, parse as '%Y-%m-%d %H:%M' format
            4. Parse deadline timestamp as ISO 8601 format
            5. Calculate time difference: time_diff = deadline - submitted_at
            6. Check if time_diff is positive (early) or negative (late)
            7. If early (positive difference):
               a. Extract days, hours, minutes from time_diff
               b. Format message prioritizing largest non-zero unit
               c. Return ("early", "✅ {days}d {hours}h early") or similar
            8. If late (negative difference):
               a. Take absolute value of time_diff
               b. Extract days, hours, minutes from absolute time_diff
               c. Format message prioritizing largest non-zero unit
               d. Return ("late", "⚠️ {days}d {hours}h late") or similar
            9. If any parsing or calculation error occurs:
               - Catch exception and return (None, "Invalid timing data")

    Example:
        >>> # Initialize with TodoView instance
        >>> submission_mgr = SubmissionManager(todo_view)
        >>> 
        >>> # Student submits an assignment
        >>> assignment = {
        ...     'id': 'assign_123',
        ...     'title': 'Python Project',
        ...     'subject': 'Computer Science',
        ...     'drive_folder_id': 'folder_xyz',
        ...     'deadline': '2025-12-31T23:59:00'
        ... }
        >>> submission_mgr.submit_assignment_dialog(assignment)
        >>> 
        >>> # Teacher views submissions and grades
        >>> submission_mgr.view_submissions_dialog(assignment)
        >>> 
        >>> # Calculate timing for a submission
        >>> status, msg = submission_mgr.calculate_submission_timing(
        ...     '2025-12-30T10:00:00',
        ...     '2025-12-31T23:59:00'
        ... )
        >>> print(f"Status: {status}, Message: {msg}")
        Status: early, Message: ✅ 1d 13h early

    See Also:
        - :class:`~src.ui.views.todo_view.TodoView`: Parent view class
        - :class:`~services.file_preview_service.FilePreviewService`: File preview service
        - :class:`~services.data_manager.DataManager`: Data persistence layer
        - :class:`~services.drive_service.DriveService`: Google Drive integration
        - :class:`~src.ui.todo_modules.storage_manager.StorageManager`: File upload manager
        - :class:`~src.ui.todo_modules.student_manager.StudentManager`: Student data manager

    Notes:
        - All file uploads include student identifier for organization
        - Submission timing uses ISO 8601 datetime format
        - Grade editing requires force_edit_email parameter to reopen editor
        - File preview requires FilePreviewService to be available
        - Missing submissions are clearly marked in teacher interface

    References:
        - Google Drive API: https://developers.google.com/drive
        - Flet UI Framework: https://flet.dev
        - ISO 8601 Datetime Standard: https://en.wikipedia.org/wiki/ISO_8601
    """

    def __init__(self, todo_view):
        """Initialize the SubmissionManager with parent view reference.

        Sets up the submission manager by storing a reference to the parent TodoView
        and attempting to initialize the FilePreviewService. If the service cannot
        be imported or initialized, file preview functionality will be disabled but
        other features remain functional.

        Args:
            todo_view (TodoView): Parent TodoView instance that provides access to:
                - page: Flet page object for UI updates
                - drive_service: Google Drive integration service
                - data_manager: Persistent data storage manager
                - storage_manager: File upload and Drive operations
                - student_manager: Student data and filtering
                - submissions: List of all submission records
                - students: List of all student records
                - current_student_email: Currently logged-in student

        Algorithm:
            1. Receive and store reference to parent TodoView instance
            2. Initialize temp_file_path attribute to None (used during upload operations)
            3. Initialize temp_file_name attribute to None (used during upload operations)
            4. Enter try-except block for FilePreviewService initialization
            5. Attempt to import FilePreviewService from services.file_preview_service module
            6. If import successful:
               a. Instantiate FilePreviewService with todo_view.page parameter
               b. Pass todo_view.drive_service as second parameter
               c. Store instance in self.file_preview attribute
            7. If ImportError occurs (service not available):
               a. Catch the exception silently
               b. Set self.file_preview to None
               c. File preview functionality will be disabled but other features work
            8. Initialization complete, instance ready for use

        Interactions:
            - **TodoView**: Stores reference for accessing shared services
            - **FilePreviewService**: Conditionally imported and initialized

        Example:
            >>> from src.ui.views.todo_view import TodoView
            >>> todo_view = TodoView(page, user_data)
            >>> submission_mgr = SubmissionManager(todo_view)
            >>> print(f"Preview available: {submission_mgr.file_preview is not None}")
            Preview available: True

        See Also:
            - :class:`~src.ui.views.todo_view.TodoView`: Parent view class
            - :class:`~services.file_preview_service.FilePreviewService`: File preview service

        Notes:
            - File preview is optional; other features work without it
            - Temporary file attributes are reset after each submission
        """
        self.todo = todo_view
        self.temp_file_path = None
        self.temp_file_name = None
        
        try:
            from services.file_preview_service import FilePreviewService
            self.file_preview = FilePreviewService(todo_view.page, todo_view.drive_service)
        except ImportError:
            self.file_preview = None
    
    def calculate_submission_timing(self, submitted_at_str, deadline_str):
        """Calculate whether a submission was early or late relative to deadline.

        Parses submission and deadline timestamps, computes the time difference,
        and returns a human-readable status message indicating whether the
        submission was early or late. Supports both ISO 8601 and custom datetime
        formats for backward compatibility.

        Args:
            submitted_at_str (str): Timestamp of when assignment was submitted.
                Accepts ISO 8601 format (with 'T' separator) or custom format
                'YYYY-MM-DD HH:MM'. Example: '2025-12-30T10:00:00' or
                '2025-12-30 10:00'.
            deadline_str (str): Deadline timestamp in ISO 8601 format.
                Example: '2025-12-31T23:59:00'.

        Returns:
            tuple: A 2-tuple containing:
                - status_code (str or None): 'early' if submitted before deadline,
                  'late' if submitted after deadline, None if data invalid.
                - message (str): Formatted human-readable timing message with emoji
                  and time breakdown. Examples: '✅ 1d 13h early', '⚠️ 2h 30m late',
                  'No timing data', 'Invalid timing data'.

        Algorithm:
            1. **Input Validation Phase**:
               a. Check if submitted_at_str parameter is provided and not empty
               b. Check if deadline_str parameter is provided and not empty
               c. If either is missing, return tuple (None, "No timing data")
               d. Proceed to parsing phase if both parameters valid
            
            2. **Submission Timestamp Parsing**:
               a. Check if submitted_at_str contains 'T' character (ISO 8601 indicator)
               b. If 'T' present:
                  - Parse using datetime.fromisoformat() for ISO 8601 format
                  - Example: '2025-12-30T10:00:00' → datetime object
               c. If 'T' not present:
                  - Parse using strptime() with format '%Y-%m-%d %H:%M'
                  - Example: '2025-12-30 10:00' → datetime object
               d. Store result in submitted_at variable
            
            3. **Deadline Timestamp Parsing**:
               a. Parse deadline_str using datetime.fromisoformat() (always ISO 8601)
               b. Example: '2025-12-31T23:59:00' → datetime object
               c. Store result in deadline variable
            
            4. **Time Difference Calculation**:
               a. Compute: time_diff = deadline - submitted_at
               b. Result is timedelta object (can be positive or negative)
               c. Extract total_seconds() to determine early vs late
            
            5. **Early Submission Processing** (time_diff > 0):
               a. Check if time_diff.total_seconds() is positive
               b. Extract components from time_diff:
                  - days = time_diff.days
                  - hours = time_diff.seconds // 3600
                  - minutes = (time_diff.seconds % 3600) // 60
               c. Format message based on priority (days > hours > minutes):
                  - If days > 0: return ("early", "✅ {days}d {hours}h early")
                  - Elif hours > 0: return ("early", "✅ {hours}h {minutes}m early")
                  - Else: return ("early", "✅ {minutes}m early")
            
            6. **Late Submission Processing** (time_diff <= 0):
               a. Calculate absolute value: time_diff = abs(time_diff)
               b. Extract components from absolute time_diff:
                  - days = time_diff.days
                  - hours = time_diff.seconds // 3600
                  - minutes = (time_diff.seconds % 3600) // 60
               c. Format message based on priority (days > hours > minutes):
                  - If days > 0: return ("late", "⚠️ {days}d {hours}h late")
                  - Elif hours > 0: return ("late", "⚠️ {hours}h {minutes}m late")
                  - Else: return ("late", "⚠️ {minutes}m late")
            
            7. **Error Handling**:
               a. Wrap entire process in try-except block
               b. If any exception occurs (parsing error, calculation error):
                  - Catch exception silently
                  - Return tuple (None, "Invalid timing data")
               c. This ensures function never crashes, always returns valid tuple

        Interactions:
            - **datetime.datetime**: Used for timestamp parsing and arithmetic
            - **datetime.timedelta**: Represents time difference between dates

        Example:
            >>> # Early submission (1 day 13 hours early)
            >>> status, msg = calculate_submission_timing(
            ...     '2025-12-30T10:00:00',
            ...     '2025-12-31T23:59:00'
            ... )
            >>> print(f"{status}: {msg}")
            early: ✅ 1d 13h early
            >>> 
            >>> # Late submission (2 hours 30 minutes late)
            >>> status, msg = calculate_submission_timing(
            ...     '2026-01-01T02:30:00',
            ...     '2025-12-31T23:59:00'
            ... )
            >>> print(f"{status}: {msg}")
            late: ⚠️ 2h 30m late
            >>> 
            >>> # Custom format submission (30 minutes early)
            >>> status, msg = calculate_submission_timing(
            ...     '2025-12-31 23:29',
            ...     '2025-12-31T23:59:00'
            ... )
            >>> print(f"{status}: {msg}")
            early: ✅ 30m early
            >>> 
            >>> # Invalid data
            >>> status, msg = calculate_submission_timing(
            ...     'invalid-date',
            ...     '2025-12-31T23:59:00'
            ... )
            >>> print(f"{status}: {msg}")
            None: Invalid timing data

        See Also:
            - :meth:`submit_assignment_dialog`: Uses timing for submission records
            - :meth:`view_submissions_dialog`: Displays timing in teacher interface
            - :mod:`datetime`: Python datetime module documentation

        Notes:
            - Time breakdowns prioritize largest unit (days > hours > minutes)
            - Displays only non-zero units in formatted message
            - Handles both ISO 8601 and legacy datetime formats
            - Returns None status for invalid or missing data
            - Uses Unicode emoji for visual status indicators (✅/⚠️)
        """
        if not submitted_at_str or not deadline_str:
            return None, "No timing data"
        
        try:
            if 'T' in submitted_at_str:
                submitted_at = datetime.datetime.fromisoformat(submitted_at_str)
            else:
                submitted_at = datetime.datetime.strptime(submitted_at_str, '%Y-%m-%d %H:%M')

            deadline = datetime.datetime.fromisoformat(deadline_str)
            
            time_diff = deadline - submitted_at
            
            if time_diff.total_seconds() > 0:
                days = time_diff.days
                hours = time_diff.seconds // 3600
                minutes = (time_diff.seconds % 3600) // 60
                
                if days > 0:
                    return "early", f"✅ {days}d {hours}h early"
                elif hours > 0:
                    return "early", f"✅ {hours}h {minutes}m early"
                else:
                    return "early", f"✅ {minutes}m early"
            else:
                time_diff = abs(time_diff)
                days = time_diff.days
                hours = time_diff.seconds // 3600
                minutes = (time_diff.seconds % 3600) // 60
                
                if days > 0:
                    return "late", f"⚠️ {days}d {hours}h late"
                elif hours > 0:
                    return "late", f"⚠️ {hours}h {minutes}m late"
                else:
                    return "late", f"⚠️ {minutes}m late"
        except:
            return None, "Invalid timing data"
    
    def submit_assignment_dialog(self, assignment):
        """Display student submission dialog for uploading assignment work.

        Creates an interactive modal dialog allowing students to submit their
        assignment by uploading a file to Google Drive, optionally adding
        submission notes, and selecting a target folder. Handles the complete
        submission workflow including validation, file upload, record creation,
        and user feedback.

        Args:
            assignment (dict): Assignment dictionary containing:
                - id (str): Unique assignment identifier
                - title (str): Assignment title/name
                - subject (str): Subject/category (e.g., 'Math', 'Science')
                - drive_folder_id (str): Target Google Drive folder ID for uploads
                - deadline (str): ISO 8601 deadline timestamp

        Returns:
            None: Displays modal dialog and handles interaction asynchronously.
                Updates UI and data stores as side effects.

        Algorithm:
            1. **Prerequisites Validation**:
               a. Extract subject from assignment dictionary (default to 'Other')
               b. Extract drive_folder_id from assignment dictionary
               c. Check if self.todo.drive_service is available and authenticated
               d. If drive_service is None:
                  - Show error snackbar "No Drive service available"
                  - Return immediately (abort dialog creation)
               e. Check if drive_folder_id exists and is not empty
               f. If drive_folder_id missing:
                  - Show error snackbar "No submission folder linked"
                  - Return immediately (abort dialog creation)
            
            2. **UI Component Initialization**:
               a. Create selected_folder_id list with drive_folder_id as default
               b. Retrieve folder name using get_folder_name_by_id()
               c. Create folder_display text showing "Upload to: {folder_name}"
               d. Create submission_text TextField for student notes (multiline, 3+ lines)
               e. Create upload_status Text element (initially empty string)
               f. Set up folder browser button with "Browse Folders" label
            
            3. **Folder Browser Setup**:
               a. Define update_selected_folder(fid) callback function
               b. Callback updates selected_folder_id[0] with new folder ID
               c. Callback retrieves new folder name using get_folder_name_by_id()
               d. If folder name is "Linked Folder", query Drive service for actual name
               e. Update folder_display.value with new folder name
               f. Call page.update() to refresh UI
               g. Connect callback to change_folder_btn click event
               h. Callback invokes storage_manager.create_browse_dialog()
            
            4. **File Picker Handler Definition** (on_file_picked):
               a. Check if files were selected in picker (e.files not empty)
               b. If no files, return immediately (user cancelled)
               c. Extract file_path from e.files[0].path
               d. Extract file_name from e.files[0].name
               e. Get student identifier from current_student_email (split by '@')
               f. Update upload_status to "Uploading {file_name}..."
               g. Call page.update() to show upload status
               h. Enter try-except block for upload operation
            
            5. **File Upload Process** (within on_file_picked):
               a. Call storage_manager.upload_submission_to_link_drive() with:
                  - file_path: full path to local file
                  - file_name: original file name
                  - subject: assignment subject for folder organization
                  - student_name: student identifier from email
                  - folder_id: selected_folder_id[0]
               b. Store upload result (file metadata from Drive API)
               c. If result is truthy (upload succeeded):
                  - Update upload_status to "✓ Uploaded to link drive"
                  - Show success snackbar "File uploaded to link drive folder!"
               d. If result is falsy (upload failed):
                  - Update upload_status to "✗ Upload failed"
                  - Show error snackbar "Upload failed"
                  - Skip submission record creation
            
            6. **Submission Record Management**:
               a. Call _get_submission_status() to check for existing submission
               b. Generate current timestamp using datetime.now().strftime()
               c. Extract submission notes from submission_text.value (strip whitespace)
               d. If notes empty, use default "Uploaded to link drive"
               e. If existing submission found:
                  - Update existing['submitted_at'] with new timestamp
                  - Update existing['file_id'] from upload result
                  - Update existing['file_name'] from upload result
                  - Update existing['file_link'] from upload result
                  - Set existing['uploaded_to_drive'] to True
                  - Update existing['submission_text'] with notes
                  - Update existing['subject_folder'] with subject
               f. If no existing submission:
                  - Create new submission dictionary with:
                    * id: timestamp-based unique identifier
                    * assignment_id: from assignment parameter
                    * student_email: from current_student_email
                    * submission_text: student notes
                    * submitted_at: current timestamp
                    * grade: None (not graded yet)
                    * feedback: None (no feedback yet)
                    * file_id, file_name, file_link: from upload result
                    * uploaded_to_drive: True
                    * subject_folder: assignment subject
                  - Append new submission to self.todo.submissions list
            
            7. **Persistence and UI Update**:
               a. Call data_manager.save_submissions() with updated submissions list
               b. Call display_assignments() to refresh main UI with new status
               c. Sleep for 1 second to allow user to see success message
               d. Call close_overlay(None) to automatically close dialog
               e. Update page to reflect all changes
            
            8. **Error Handling**:
               a. Catch any exceptions during upload or record creation
               b. Update upload_status to "✗ Error: {exception_message}"
               c. Show error snackbar with exception details
               d. Update page to display error message
            
            9. **File Picker Registration**:
               a. Create ft.FilePicker instance with on_result=on_file_picked
               b. Append file_picker to page.overlay list
               c. Update page to register picker in overlay system
            
            10. **Dialog Content Assembly**:
                a. Create Column container with spacing=10 and scroll="auto"
                b. Add assignment title text (bold, word-wrapped)
                c. Add subject text (size 13, blue color)
                d. Add divider for visual separation
                e. Add submission_text field for student notes
                f. Add 10px spacing container
                g. Add responsive row with folder_display and change_folder_btn
                h. Add help text "You can browse and select a subfolder if needed"
                i. Add 5px spacing container
                j. Add "Choose File" button with upload icon
                k. Add upload_status text for progress feedback
                l. Add 10px spacing container
                m. Add "Close" button row aligned to right
            
            11. **Dialog Display**:
                a. Call todo.show_overlay() with:
                   - content: assembled Column
                   - title: "Submit: {assignment_title}"
                   - width: 450px
                b. Store returned overlay and close_overlay function
                c. Dialog now visible to user, awaiting interaction

        Interactions:
            - **DriveService**: Validates availability and retrieves folder info
            - **StorageManager**: Handles file upload to Drive via 
              upload_submission_to_link_drive()
            - **DataManager**: Persists submission records via save_submissions()
            - **TodoView**: Accesses page, services, shows snackbars, overlays
            - **FilePicker**: System file selection dialog
            - **FilePreviewService**: Optional file preview (not in this method)

        Example:
            >>> # Student submits assignment
            >>> assignment = {
            ...     'id': 'assign_123',
            ...     'title': 'Python Project',
            ...     'subject': 'Computer Science',
            ...     'drive_folder_id': 'folder_abc123',
            ...     'deadline': '2025-12-31T23:59:00'
            ... }
            >>> submission_mgr.submit_assignment_dialog(assignment)
            >>> # User interacts with dialog:
            >>> # 1. Optionally browses to select subfolder
            >>> # 2. Clicks "Choose File" and selects file
            >>> # 3. File uploads to Drive
            >>> # 4. Submission record created/updated
            >>> # 5. Dialog auto-closes on success

        See Also:
            - :meth:`view_submissions_dialog`: Teacher grading interface
            - :meth:`_get_submission_status`: Retrieve existing submission
            - :class:`~src.ui.todo_modules.storage_manager.StorageManager`: File uploads
            - :class:`~services.drive_service.DriveService`: Drive operations
            - :class:`~services.data_manager.DataManager`: Data persistence

        Notes:
            - Requires Google Drive service to be configured and authenticated
            - Assignment must have valid drive_folder_id linked
            - Student email is extracted from current_student_email attribute
            - File upload uses student name prefix for organization
            - Submission timestamp captured at upload completion
            - Dialog auto-closes 1 second after successful upload
            - Previous submissions are updated rather than duplicated
            - Upload errors display in-dialog status and snackbar notification

        Raises:
            No direct exceptions raised. All errors handled gracefully with:
            - Snackbar notifications for user feedback
            - Status text updates within dialog
            - Early return for validation failures
        """
        subject = assignment.get('subject', 'Other')
        drive_folder_id = assignment.get('drive_folder_id')
        
        if not self.todo.drive_service:
            self.todo.show_snackbar("No Drive service available", ft.Colors.RED)
            return
        
        if not drive_folder_id:
            self.todo.show_snackbar("No submission folder linked to this assignment", ft.Colors.RED)
            return
        
        selected_folder_id = [drive_folder_id]
        
        drive_folder_name = self.todo.get_folder_name_by_id(drive_folder_id)
        folder_display = ft.Text(f"Upload to: {drive_folder_name}", size=13, color=ft.Colors.BLUE, overflow=ft.TextOverflow.VISIBLE, no_wrap=False)
        
        submission_text = ft.TextField(
            hint_text="Submission notes/comments",
            multiline=True,
            min_lines=3,
            expand=True
        )
        
        upload_status = ft.Text("", overflow=ft.TextOverflow.VISIBLE, no_wrap=False)
        
        def update_selected_folder(fid):
            selected_folder_id[0] = fid
            folder_name = self.todo.get_folder_name_by_id(fid)
            
            if folder_name == "Linked Folder" and self.todo.drive_service:
                try:
                    info = self.todo.drive_service.get_file_info(fid)
                    if info:
                        folder_name = info.get('name', 'Selected Folder')
                except:
                    folder_name = "Selected Folder"
            
            folder_display.value = f"Upload to: {folder_name}"
            self.todo.page.update()
        
        change_folder_btn = ft.TextButton(
            "Browse Folders",
            icon=ft.Icons.FOLDER_OPEN,
            on_click=lambda e: self.todo.storage_manager.create_browse_dialog(
                selected_folder_id[0],
                update_selected_folder
            )
        )
        
        def on_file_picked(e: ft.FilePickerResultEvent):
            if not e.files:
                return
            
            file_path = e.files[0].path
            file_name = e.files[0].name
            
            student_name = self.todo.current_student_email.split('@')[0] if self.todo.current_student_email else "unknown"
            
            upload_status.value = f"Uploading {file_name}..."
            self.todo.page.update()
            
            try:
                result = self.todo.storage_manager.upload_submission_to_link_drive(
                    file_path,
                    file_name,
                    subject,
                    student_name,
                    selected_folder_id[0]
                )
                
                if result:
                    upload_status.value = f"✓ Uploaded to link drive"
                    self.todo.show_snackbar(f"File uploaded to link drive folder!", ft.Colors.GREEN)
                    
                    existing = self._get_submission_status(assignment['id'], self.todo.current_student_email)
                    submitted_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                    
                    notes = submission_text.value.strip() if submission_text.value else "Uploaded to link drive"
                    
                    if existing:
                        existing['submitted_at'] = submitted_at
                        existing['file_id'] = result.get('id')
                        existing['file_name'] = result.get('name')
                        existing['file_link'] = result.get('webViewLink')
                        existing['uploaded_to_drive'] = True
                        existing['submission_text'] = notes
                        existing['subject_folder'] = subject
                    else:
                        self.todo.submissions.append({
                            'id': str(datetime.datetime.now().timestamp()),
                            'assignment_id': assignment['id'],
                            'student_email': self.todo.current_student_email,
                            'submission_text': notes,
                            'submitted_at': submitted_at,
                            'grade': None,
                            'feedback': None,
                            'file_id': result.get('id'),
                            'file_name': result.get('name'),
                            'file_link': result.get('webViewLink'),
                            'uploaded_to_drive': True,
                            'subject_folder': subject
                        })
                    
                    self.todo.data_manager.save_submissions(self.todo.submissions)
                    self.todo.display_assignments()
                    
                    import time
                    time.sleep(1)
                    close_overlay(None)
                else:
                    upload_status.value = "✗ Upload failed"
                    self.todo.show_snackbar("Upload failed", ft.Colors.RED)
            except Exception as ex:
                upload_status.value = f"✗ Error: {str(ex)}"
                self.todo.show_snackbar(f"Error: {str(ex)}", ft.Colors.RED)
            
            self.todo.page.update()
        
        file_picker = ft.FilePicker(on_result=on_file_picked)
        self.todo.page.overlay.append(file_picker)
        self.todo.page.update()
        
        content = ft.Column([
            ft.Text(f"Assignment: {assignment.get('title')}", weight=ft.FontWeight.BOLD, overflow=ft.TextOverflow.VISIBLE, no_wrap=False),
            ft.Text(f"Subject: {subject}", size=13, color=ft.Colors.BLUE, overflow=ft.TextOverflow.VISIBLE, no_wrap=False),
            ft.Divider(),
            submission_text,
            ft.Container(height=10),
            ft.ResponsiveRow([
                ft.Column(col={"sm": 12, "md": 8}, controls=[folder_display]),
                ft.Column(col={"sm": 12, "md": 4}, controls=[change_folder_btn])
            ]),
            ft.Text("You can browse and select a subfolder if needed", size=11, italic=True, color=ft.Colors.GREY_600, overflow=ft.TextOverflow.VISIBLE, no_wrap=False),
            ft.Container(height=5),
            ft.ElevatedButton(
                "Choose File",
                icon=ft.Icons.FILE_UPLOAD,
                on_click=lambda e: file_picker.pick_files()
            ),
            upload_status,
            ft.Container(height=10),
            ft.Row([
                ft.TextButton("Close", on_click=lambda e: close_overlay(e))
            ], alignment=ft.MainAxisAlignment.END)
        ], spacing=10, scroll="auto")
        
        overlay, close_overlay = self.todo.show_overlay(
            content,
            f"Submit: {assignment['title']}",
            width=450
        )
    
    def view_submissions_dialog(self, assignment, force_edit_email=None):
        """Display teacher grading interface for viewing and grading submissions.

        Creates a comprehensive modal dialog showing all students enrolled for an
        assignment (filtered by target type), their submission status, timing
        information, and grading controls. Supports inline grading, feedback entry,
        file preview, and edit mode for existing grades.

        Args:
            assignment (dict): Assignment dictionary containing:
                - id (str): Unique assignment identifier
                - title (str): Assignment title displayed in dialog header
                - target_for (str): Student filter - 'all', 'bridging', or 'regular'
                - deadline (str): ISO 8601 deadline for timing calculations
            force_edit_email (str, optional): If provided, automatically opens the
                grade editor for this specific student email, even if already graded.
                Defaults to None (show read-only view for graded submissions).

        Returns:
            None: Displays modal dialog and handles interaction asynchronously.
                Updates UI and data stores as side effects.

        Algorithm:
            1. **Dialog Container Initialization**:
               a. Create submissions_list Column with scroll="auto" and spacing=10
               b. Initialize submitted_count counter to 0
               c. Extract deadline from assignment dictionary
               d. Create overlay and close_overlay using todo.show_overlay()
               e. Set dialog title to "Submissions for: {title} (0/{total})" initially
               f. Set dialog dimensions: width=600px, height=500px
            
            2. **Student Filtering**:
               a. Extract target_for value from assignment ('all', 'bridging', 'regular')
               b. If target == 'bridging':
                  - Call student_manager.get_bridging_students()
                  - Store filtered list in target_students
               c. If target == 'regular':
                  - Call student_manager.get_regular_students()
                  - Store filtered list in target_students
               d. If target == 'all' or any other value:
                  - Use complete self.todo.students list as target_students
               e. If target_students is empty:
                  - Append "No students enrolled" message to submissions_list
                  - Skip to step 10 (early completion)
            
            3. **Student Loop - Submission Status Retrieval**:
               a. Begin for loop iterating through each student in target_students
               b. Extract student_name from student['name']
               c. Search self.todo.submissions for matching record:
                  - Match on: assignment_id == assignment['id']
                  - AND: student_email == student['email']
               d. Store result in 'sub' variable (None if not found)
            
            4. **Submitted Assignment Processing**:
               a. If sub is not None (submission exists):
                  i. Increment submitted_count by 1
                  ii. Create status_icon as green checkmark (ft.Icons.CHECK_CIRCLE)
                  iii. Set status_text to "Submitted: {submitted_at}"
                  
            5. **Timing Calculation for Submissions**:
               a. Call calculate_submission_timing() with:
                  - submitted_at: sub['submitted_at']
                  - deadline: assignment deadline
               b. Receive timing_status ('early' or 'late' or None)
               c. Receive timing_text (formatted message like "✅ 1d 13h early")
               d. Set timing_color to GREEN if early, ORANGE if late
               e. Create timing badge container with background color and text
            
            6. **Grading Mode Determination**:
               a. Check if submission is already graded:
                  - is_graded = True if (grade exists OR feedback exists) AND not force_edit
               b. If is_graded == True (Read-Only Mode):
                  i. Create grade_display Container with:
                     - Blue-tinted background (opacity 0.05)
                     - Border: 1px solid BLUE_200
                     - Padding: 10px, border_radius: 8px
                  ii. Display grade as "Grade: {value}" (bold, blue text)
                  iii. Display feedback as "Feedback: {text}" (bold label + text)
                  iv. Create "Edit Grade" button with edit icon
                  v. Define make_toggle_edit_handler() closure:
                      - Captures student_email and close_fn
                      - When clicked: closes dialog, reopens with force_edit_email
                  vi. Connect handler to "Edit Grade" button
                  vii. Display "Last updated: {graded_at}" if timestamp exists
                  viii. Assemble grade_section with display and edit button
               c. If is_graded == False (Edit Mode):
                  i. Create grade_field TextField:
                     - Pre-filled with existing grade if available
                     - Label: "Grade", hint: "e.g., 95/100"
                     - Width: 150px
                  ii. Create feedback_field TextField:
                     - Pre-filled with existing feedback if available
                     - Label: "Feedback", multiline: True
                     - Min lines: 3, max lines: 5
                  iii. Create save_status Text (initially empty)
                  iv. Define make_save_handler() closure:
                      - Captures sub, student_name, close_fn
                      - Returns save_grade(e) function
                  v. Save handler implementation:
                      - Disable save button, set text to "Saving..."
                      - Update page to show disabled state
                      - Update sub['grade'] from grade_field.value
                      - Update sub['feedback'] from feedback_field.value
                      - Set sub['graded_at'] to current timestamp
                      - Call data_manager.save_submissions()
                      - Show success snackbar
                      - Close dialog and reopen (refreshes to read-only)
                      - On error: update save_status, re-enable button
                  vi. Create "Save Grade" button with save icon
                  vii. Connect save_handler to button click
                  viii. Assemble grade_section with fields and save button
            
            7. **File Access Controls**:
               a. Initialize file_link_btn as empty Container
               b. If sub.get('file_link') exists (has direct Drive link):
                  i. Create Row with two buttons:
                     - "Preview File" button (if file_preview service available)
                     - Click calls _preview_file() with file_id and file_name
                     - "Open in Browser" button
                     - Click calls _open_link() with file_link URL
                  ii. Set spacing to 10px between buttons
                  iii. Store in file_link_btn
               c. Elif sub.get('file_id') exists (has Drive ID but no link):
                  i. Create Row with two buttons:
                     - "Preview File" button (if file_preview available)
                     - Click calls _preview_file() with file_id and file_name
                     - "Open in Browser" button
                     - Click calls _open_drive_file() with file_id
                  ii. Set spacing to 10px between buttons
                  iii. Store in file_link_btn
            
            8. **Submission Card Assembly**:
               a. Create Column with card_content containing:
                  i. Row with status_icon and student name/email (bold, word-wrap)
                  ii. Status text (size 12, green, "Submitted: {time}")
                  iii. Timing badge container (if timing_status exists)
                  iv. Submission notes text (size 12, word-wrap)
                  v. File name text (size 12, blue color, word-wrap)
                  vi. File link buttons row
                  vii. Divider
                  viii. Grade section (read-only or edit mode)
               b. Set card_border_color to GREEN_200
               c. Set card_bg to GREEN_50
               d. Wrap card_content in Container with:
                  - padding: 10px
                  - border: 1px solid card_border_color
                  - border_radius: 8px
                  - bgcolor: card_bg
               e. Store wrapped container in 'card' variable
            
            9. **Missing Submission Processing**:
               a. If sub is None (no submission found):
                  i. Create status_icon as red cancel icon (ft.Icons.CANCEL)
                  ii. Set status_text to "Missing"
                  iii. Create card_content as Row containing:
                      - status_icon (red cancel)
                      - Student name/email Container (bold, word-wrap, expand=True)
                      - status_text ("Missing" in red, bold)
                  iv. Set card_border_color to RED_200
                  v. Set card_bg to RED_50
                  vi. Wrap in Container with red theme styling
                  vii. Store wrapped container in 'card' variable
            
            10. **Card Addition and Counter Update**:
                a. Append 'card' to submissions_list.controls
                b. After all students processed, insert at position 0:
                   - Text showing "Submissions: {submitted_count}/{total}"
                   - Size: 16, bold, color: BLUE_700
                c. Update dialog title to reflect accurate count
                d. Call self.todo.page.update() to render all changes
            
            11. **Event Handler Persistence**:
                a. All event handlers (save, edit, preview, open) remain active
                b. Handlers use closures to capture submission references
                c. Handlers persist until dialog is closed
                d. Dialog can be reopened multiple times with different parameters
            
            12. **Force Edit Mode Handling**:
                a. If force_edit_email parameter provided on dialog open:
                   i. When processing matching student, bypass is_graded check
                   ii. Force edit mode to display for that specific student
                   iii. All other students display normal read-only if graded
                b. After "Edit Grade" button clicked:
                   i. Close current dialog instance
                   ii. Reopen view_submissions_dialog() with force_edit_email set
                   iii. This creates fresh dialog with edit mode active

        Interactions:
            - **StudentManager**: Retrieves filtered student lists via 
              get_bridging_students(), get_regular_students()
            - **DataManager**: Persists grade updates via save_submissions()
            - **FilePreviewService**: Displays file previews via _preview_file()
            - **DriveService**: Retrieves file info for drive links
            - **TodoView**: Accesses submissions, students, shows snackbars/overlays
            - **calculate_submission_timing()**: Computes early/late timing

        Example:
            >>> # Teacher views all submissions
            >>> assignment = {
            ...     'id': 'assign_123',
            ...     'title': 'Python Project',
            ...     'target_for': 'all',
            ...     'deadline': '2025-12-31T23:59:00'
            ... }
            >>> submission_mgr.view_submissions_dialog(assignment)
            >>> # Dialog shows:
            >>> # - 15/20 students submitted
            >>> # - 5 green cards (submitted, graded)
            >>> # - 10 green cards (submitted, needs grading)
            >>> # - 5 red cards (missing submission)
            >>> 
            >>> # Teacher edits existing grade
            >>> submission_mgr.view_submissions_dialog(
            ...     assignment,
            ...     force_edit_email='student@example.com'
            ... )
            >>> # Dialog opens with edit mode active for that student

        See Also:
            - :meth:`submit_assignment_dialog`: Student submission interface
            - :meth:`calculate_submission_timing`: Timing calculation
            - :meth:`_get_submission_status`: Retrieve submission record
            - :meth:`_preview_file`: Launch file preview
            - :class:`~src.ui.todo_modules.student_manager.StudentManager`: Student filtering
            - :class:`~services.data_manager.DataManager`: Grade persistence

        Notes:
            - Dialog is 600px wide, 500px tall with scrollable content
            - Students filtered by assignment target_for (all/bridging/regular)
            - Submission timing shows days, hours, minutes with emoji indicators
            - Grade editing updates 'graded_at' timestamp automatically
            - Edit mode accessible via "Edit Grade" button or force_edit_email
            - Missing submissions clearly marked with red styling
            - File preview requires FilePreviewService availability
            - Browser links open in new tab via webbrowser module
            - Save button disabled during save operation to prevent double-submit
            - Dialog auto-refreshes after grade save to show read-only view

        Raises:
            No direct exceptions raised. All errors handled gracefully with:
            - Try-catch blocks around grade save operations
            - Snackbar notifications for save success/failure
            - Status text updates within dialog
        """
        submissions_list = ft.Column(scroll="auto", spacing=10)
        
        target = assignment.get('target_for', 'all')
        if target == 'bridging':
            target_students = self.todo.student_manager.get_bridging_students()
        elif target == 'regular':
            target_students = self.todo.student_manager.get_regular_students()
        else:
            target_students = self.todo.students
        
        if not target_students:
            submissions_list.controls.append(
                ft.Text("No students enrolled for this assignment type", color=ft.Colors.GREY)
            )
        
        submitted_count = 0
        deadline = assignment.get('deadline')
        
        overlay, close_overlay = self.todo.show_overlay(
            submissions_list,
            f"Submissions for: {assignment['title']} ({submitted_count}/{len(target_students)})",
            width=600,
            height=500
        )
        
        for student in target_students:
            sub = next((s for s in self.todo.submissions
                       if s['assignment_id'] == assignment['id'] and s['student_email'] == student['email']), None)
            
            student_name = student['name']
            
            if sub:
                submitted_count += 1
                status_icon = ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN)
                status_text = f"Submitted: {sub['submitted_at']}"
                
                timing_status, timing_text = self.calculate_submission_timing(
                    sub['submitted_at'], 
                    deadline
                )
                timing_color = ft.Colors.GREEN if timing_status == "early" else ft.Colors.ORANGE

                is_graded = (sub.get('grade') or sub.get('feedback')) and (force_edit_email != student['email'])
                
                if is_graded:
                    grade_display = ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text("Grade:", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.GREY_700),
                                ft.Text(sub.get('grade', 'Not graded'), size=14, color=ft.Colors.BLUE_700, weight=ft.FontWeight.W_500),
                            ], spacing=8),
                            ft.Row([
                                ft.Text("Feedback:", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.GREY_700),
                            ], spacing=8),
                            ft.Text(
                                sub.get('feedback', 'No feedback'), 
                                size=13, 
                                color=ft.Colors.GREY_800,
                                overflow=ft.TextOverflow.VISIBLE,
                                no_wrap=False
                            ),
                        ], spacing=5),
                        padding=10,
                        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLUE),
                        border_radius=8,
                        border=ft.border.all(1, ft.Colors.BLUE_200)
                    )
                    
                    def make_toggle_edit_handler(student_email, close_fn):
                        def toggle_edit_mode(e):
                            close_fn(None)
                            self.view_submissions_dialog(assignment, force_edit_email=student_email)
                        return toggle_edit_mode
                    
                    grade_section = ft.Column([
                        grade_display,
                        ft.Row([
                            ft.TextButton(
                                "Edit Grade",
                                icon=ft.Icons.EDIT,
                                on_click=make_toggle_edit_handler(student['email'], close_overlay)
                            ),
                            ft.Text(
                                f"Last updated: {sub.get('graded_at', '')}",
                                size=11,
                                color=ft.Colors.GREY_600,
                                italic=True
                            ) if sub.get('graded_at') else ft.Container()
                        ], spacing=10)
                    ], spacing=8)
                    
                else:
                    grade_field = ft.TextField(
                        value=sub.get('grade', ''),
                        label="Grade",
                        width=150,
                        hint_text="e.g., 95/100"
                    )
                    
                    feedback_field = ft.TextField(
                        value=sub.get('feedback', ''),
                        label="Feedback",
                        multiline=True,
                        min_lines=3,
                        max_lines=5,
                        hint_text="Enter feedback for student"
                    )
                    
                    save_status = ft.Text("", size=12, color=ft.Colors.GREEN)
                    
                    def make_save_handler(submission_ref, student_name_ref, close_fn):
                        def save_grade(e):
                            e.control.disabled = True
                            e.control.text = "Saving..."
                            self.todo.page.update()
                            
                            try:
                                submission_ref['grade'] = grade_field.value
                                submission_ref['feedback'] = feedback_field.value
                                submission_ref['graded_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                                
                                self.todo.data_manager.save_submissions(self.todo.submissions)
                                
                                self.todo.show_snackbar(f"✓ Grade saved for {student_name_ref}", ft.Colors.GREEN)
                                
                                close_fn(None)
                                self.view_submissions_dialog(assignment)
                                
                            except Exception as ex:
                                save_status.value = f"Error: {str(ex)}"
                                save_status.color = ft.Colors.RED
                                e.control.text = "Save Grade"
                                e.control.disabled = False
                                self.todo.show_snackbar(f"✗ Failed to save: {str(ex)}", ft.Colors.RED)
                            
                            self.todo.page.update()
                        
                        return save_grade
                    
                    save_handler = make_save_handler(sub, student_name, close_overlay)
                    
                    grade_section = ft.Column([
                        grade_field,
                        feedback_field,
                        ft.Row([
                            ft.ElevatedButton(
                                "Save Grade",
                                on_click=save_handler,
                                icon=ft.Icons.SAVE,
                                bgcolor=ft.Colors.BLUE,
                                color=ft.Colors.WHITE
                            ),
                            save_status
                        ], spacing=10)
                    ], spacing=10)
                
                file_link_btn = ft.Container()
                if sub.get('file_link'):
                    file_link_btn = ft.Row([
                        ft.TextButton(
                            "Preview File",
                            icon=ft.Icons.VISIBILITY,
                            on_click=lambda e, fid=sub.get('file_id'), fname=sub.get('file_name', 'File'): 
                                self._preview_file(fid, fname) if self.file_preview and fid else None
                        ) if self.file_preview else ft.Container(),
                        ft.TextButton(
                            "Open in Browser",
                            icon=ft.Icons.OPEN_IN_NEW,
                            on_click=lambda e, link=sub['file_link']: self._open_link(link)
                        )
                    ], spacing=10)
                elif sub.get('file_id') and self.todo.drive_service:
                    file_link_btn = ft.Row([
                        ft.TextButton(
                            "Preview File",
                            icon=ft.Icons.VISIBILITY,
                            on_click=lambda e, fid=sub['file_id'], fname=sub.get('file_name', 'File'): 
                                self._preview_file(fid, fname) if self.file_preview else None
                        ) if self.file_preview else ft.Container(),
                        ft.TextButton(
                            "Open in Browser",
                            icon=ft.Icons.OPEN_IN_NEW,
                            on_click=lambda e, fid=sub['file_id']: self._open_drive_file(fid)
                        )
                    ], spacing=10)
                
                card_content = ft.Column([
                    ft.Row([
                        status_icon,
                        ft.Container(
                            content=ft.Text(
                                f"{student_name} ({student['email']})", 
                                weight=ft.FontWeight.BOLD, 
                                overflow=ft.TextOverflow.VISIBLE, 
                                no_wrap=False
                            ),
                            expand=True
                        ),
                    ]),
                    ft.Text(status_text, size=12, color=ft.Colors.GREEN, overflow=ft.TextOverflow.VISIBLE, no_wrap=False),
                    ft.Container(
                        content=ft.Text(timing_text, size=13, weight=ft.FontWeight.BOLD, overflow=ft.TextOverflow.VISIBLE, no_wrap=False),
                        bgcolor=ft.Colors.with_opacity(0.1, timing_color),
                        padding=5,
                        border_radius=5
                    ) if timing_status else ft.Container(),
                    ft.Text(f"Notes: {sub.get('submission_text', 'No notes')}", size=12, overflow=ft.TextOverflow.VISIBLE, no_wrap=False),
                    ft.Text(
                        f"File: {sub.get('file_name', 'No file')}",
                        size=12,
                        color=ft.Colors.BLUE,
                        overflow=ft.TextOverflow.VISIBLE,
                        no_wrap=False
                    ),
                    file_link_btn,
                    ft.Divider(),
                    grade_section
                ])
                card_border_color = ft.Colors.GREEN_200
                card_bg = ft.Colors.GREEN_50
            else:
                status_icon = ft.Icon(ft.Icons.CANCEL, color=ft.Colors.RED)
                status_text = "Missing"
                card_content = ft.Row([
                    status_icon,
                    ft.Container(
                        content=ft.Text(
                            f"{student_name} ({student['email']})", 
                            weight=ft.FontWeight.BOLD, 
                            overflow=ft.TextOverflow.VISIBLE, 
                            no_wrap=False
                        ),
                        expand=True
                    ),
                    ft.Text(status_text, color=ft.Colors.RED, weight=ft.FontWeight.BOLD)
                ])
                card_border_color = ft.Colors.RED_200
                card_bg = ft.Colors.RED_50
            
            card = ft.Container(
                content=card_content,
                padding=10,
                border=ft.border.all(1, card_border_color),
                border_radius=8,
                bgcolor=card_bg
            )
            submissions_list.controls.append(card)
        
        submissions_list.controls.insert(0, ft.Text(
            f"Submissions: {submitted_count}/{len(target_students)}",
            size=16,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_700
        ))
        
        self.todo.page.update()
    
    def _get_submission_status(self, assignment_id, student_email):
        """Retrieve submission record for specific assignment and student.

        Searches the submissions list for a matching record based on assignment
        ID and student email. Used to determine submission status when displaying
        assignment lists or grading interfaces.

        Args:
            assignment_id (str): Unique identifier of the assignment to search for.
            student_email (str): Email address of the student to search for.

        Returns:
            dict or None: Submission record dictionary if found, containing:
                - id (str): Unique submission identifier
                - assignment_id (str): Associated assignment ID
                - student_email (str): Student's email address
                - submission_text (str): Student's notes/comments
                - submitted_at (str): Submission timestamp
                - grade (str or None): Assigned grade value
                - feedback (str or None): Teacher's feedback
                - file_id (str or None): Google Drive file ID
                - file_name (str or None): Name of uploaded file
                - file_link (str or None): Direct link to file
                - uploaded_to_drive (bool): Whether file uploaded successfully
                - graded_at (str or None): Grading timestamp
                Returns None if no matching submission found.

        Algorithm:
            1. **Initialize Search**:
               a. Begin iteration through self.todo.submissions list
               b. Each element 'sub' represents a submission dictionary
            
            2. **Match Criteria Check**:
               a. For current submission 'sub' in iteration:
                  i. Extract sub['assignment_id'] value
                  ii. Compare with provided assignment_id parameter
                  iii. Store boolean result of comparison
               b. Extract sub['student_email'] value
               c. Compare with provided student_email parameter
               d. Store boolean result of comparison
            
            3. **Match Evaluation**:
               a. If both conditions are True (AND logic):
                  i. Assignment ID matches provided ID
                  ii. Student email matches provided email
               b. Return the complete submission dictionary immediately
               c. Exit function with found submission
            
            4. **Continue Search**:
               a. If either condition is False:
                  i. Continue to next iteration of loop
                  ii. Check next submission in list
            
            5. **No Match Found**:
               a. If loop completes without finding match:
                  i. All submissions have been checked
                  ii. No matching record exists
               b. Return None to indicate submission not found
            
            6. **Return Value Interpretation**:
               a. If return is dict: submission exists for this student+assignment
               b. If return is None: student has not submitted this assignment
               c. Caller can use truthiness check or explicit None comparison

        Interactions:
            - **TodoView**: Accesses submissions list via self.todo.submissions

        Example:
            >>> # Check if student has submitted assignment
            >>> sub = submission_mgr._get_submission_status(
            ...     'assign_123',
            ...     'student@example.com'
            ... )
            >>> if sub:
            ...     print(f"Submitted at: {sub['submitted_at']}")
            ...     print(f"Grade: {sub.get('grade', 'Not graded')}")
            ... else:
            ...     print("No submission found")
            Submitted at: 2025-12-30 10:00
            Grade: 95/100

        See Also:
            - :meth:`submit_assignment_dialog`: Creates submission records
            - :meth:`view_submissions_dialog`: Uses this to check submission status
            - :class:`~services.data_manager.DataManager`: Persists submission data

        Notes:
            - Linear search through submissions list (O(n) complexity)
            - Returns first match found (submissions should be unique per student+assignment)
            - Used internally by other methods to avoid duplicate submissions
            - Does not modify the submission record
        """
        pass

    def _preview_file(self, file_id, file_name):
        """Launch file preview overlay for submitted assignment file.

        Opens a modal overlay displaying the contents of a Google Drive file
        using the FilePreviewService. Supports various file types including
        documents, spreadsheets, presentations, images, and PDFs.

        Args:
            file_id (str): Google Drive file ID to preview.
            file_name (str): Display name of the file (shown in preview header).

        Returns:
            None: Displays preview overlay as side effect. No return value.

        Algorithm:
            1. **Service Availability Check**:
               a. Check if self.file_preview attribute is not None
               b. If file_preview is None:
                  i. FilePreviewService failed to import or initialize
                  ii. Preview functionality unavailable
                  iii. Proceed to step 5 (silent return)
            
            2. **File ID Validation**:
               a. Check if file_id parameter is provided
               b. Check if file_id is not None and not empty string
               c. If file_id invalid:
                  i. No file to preview
                  ii. Proceed to step 5 (silent return)
            
            3. **Preview Service Invocation**:
               a. Both conditions met (service available, file_id valid)
               b. Call self.file_preview.show_preview() method
               c. Pass file_id parameter (Google Drive file identifier)
               d. Pass file_name parameter (display name for preview header)
            
            4. **Preview Display**:
               a. FilePreviewService handles:
                  i. Fetching file content from Google Drive
                  ii. Determining file type (doc, pdf, image, etc.)
                  iii. Rendering appropriate preview interface
                  iv. Creating modal overlay with preview content
                  v. Adding close button for user to dismiss
               b. Preview overlay appears on screen
               c. User can view file content without leaving application
            
            5. **Silent Failure**:
               a. If any condition failed (service unavailable or invalid file_id):
                  i. Function returns immediately with no action
                  ii. No error message displayed to user
                  iii. No exception raised
                  iv. Graceful degradation (button simply has no effect)
            
            6. **Return to Caller**:
               a. Function completes (no return value needed)
               b. Control returns to event handler
               c. Application continues normal operation

        Interactions:
            - **FilePreviewService**: Calls show_preview() method to display file
            - **DriveService**: Service uses Drive API to fetch file content

        Example:
            >>> # Preview student's submitted document
            >>> submission_mgr._preview_file(
            ...     '1abc...xyz',
            ...     'Project_Report.docx'
            ... )
            >>> # Modal overlay appears with document preview
            >>> 
            >>> # Handle missing file_id gracefully
            >>> submission_mgr._preview_file(None, 'file.txt')
            >>> # No action taken, no error raised

        See Also:
            - :meth:`view_submissions_dialog`: Calls this from "Preview File" button
            - :class:`~services.file_preview_service.FilePreviewService`: Preview service
            - :meth:`_open_drive_file`: Alternative to open file in browser

        Notes:
            - Requires FilePreviewService to be initialized (checked in __init__)
            - Silently fails if file_preview is None (service unavailable)
            - Silently fails if file_id is None or empty
            - Preview overlay provides close button for user
            - Supports multiple file formats depending on service implementation
            - Does not handle file download (use browser link for that)
        """
        for sub in self.todo.submissions:
            if sub['assignment_id'] == assignment_id and sub['student_email'] == student_email:
                return sub
        return None
    
    def _preview_file(self, file_id, file_name):
        """Launch file preview overlay for submitted assignment file.

        Opens a modal overlay displaying the contents of a Google Drive file
        using the FilePreviewService. Supports various file types including
        documents, spreadsheets, presentations, images, and PDFs.

        Args:
            file_id (str): Google Drive file ID to preview.
            file_name (str): Display name of the file (shown in preview header).

        Returns:
            None: Displays preview overlay as side effect. No return value.

        Algorithm:
            1. **Service Availability Check**:
               a. Check if self.file_preview attribute is not None
               b. If file_preview is None:
                  i. FilePreviewService failed to import or initialize
                  ii. Preview functionality unavailable
                  iii. Proceed to step 5 (silent return)
            
            2. **File ID Validation**:
               a. Check if file_id parameter is provided
               b. Check if file_id is not None and not empty string
               c. If file_id invalid:
                  i. No file to preview
                  ii. Proceed to step 5 (silent return)
            
            3. **Preview Service Invocation**:
               a. Both conditions met (service available, file_id valid)
               b. Call self.file_preview.show_preview() method
               c. Pass file_id parameter (Google Drive file identifier)
               d. Pass file_name parameter (display name for preview header)
            
            4. **Preview Display**:
               a. FilePreviewService handles:
                  i. Fetching file content from Google Drive
                  ii. Determining file type (doc, pdf, image, etc.)
                  iii. Rendering appropriate preview interface
                  iv. Creating modal overlay with preview content
                  v. Adding close button for user to dismiss
               b. Preview overlay appears on screen
               c. User can view file content without leaving application
            
            5. **Silent Failure**:
               a. If any condition failed (service unavailable or invalid file_id):
                  i. Function returns immediately with no action
                  ii. No error message displayed to user
                  iii. No exception raised
                  iv. Graceful degradation (button simply has no effect)
            
            6. **Return to Caller**:
               a. Function completes (no return value needed)
               b. Control returns to event handler
               c. Application continues normal operation

        Interactions:
            - **FilePreviewService**: Calls show_preview() method to display file
            - **DriveService**: Service uses Drive API to fetch file content

        Example:
            >>> # Preview student's submitted document
            >>> submission_mgr._preview_file(
            ...     '1abc...xyz',
            ...     'Project_Report.docx'
            ... )
            >>> # Modal overlay appears with document preview
            >>> 
            >>> # Handle missing file_id gracefully
            >>> submission_mgr._preview_file(None, 'file.txt')
            >>> # No action taken, no error raised

        See Also:
            - :meth:`view_submissions_dialog`: Calls this from "Preview File" button
            - :class:`~services.file_preview_service.FilePreviewService`: Preview service
            - :meth:`_open_drive_file`: Alternative to open file in browser

        Notes:
            - Requires FilePreviewService to be initialized (checked in __init__)
            - Silently fails if file_preview is None (service unavailable)
            - Silently fails if file_id is None or empty
            - Preview overlay provides close button for user
            - Supports multiple file formats depending on service implementation
            - Does not handle file download (use browser link for that)
        """
        if self.file_preview and file_id:
            self.file_preview.show_preview(file_id=file_id, file_name=file_name)
    
    def _open_link(self, link):
        """Open a web link in the system's default browser.

        Launches the default web browser with the provided URL. Used to open
        Google Drive file links from the submission grading interface.

        Args:
            link (str): Full URL to open in browser. Should include protocol
                (e.g., 'https://drive.google.com/file/d/...'). 

        Returns:
            None: Opens browser as side effect. No return value.

        Algorithm:
            1. **Module Import**:
               a. Import webbrowser module from Python standard library
               b. Module provides interface to system's web browser
               c. Import occurs at runtime (not at module level)
            
            2. **Browser Invocation**:
               a. Call webbrowser.open() function
               b. Pass link parameter as URL string argument
               c. Function signature: webbrowser.open(url, new=0, autoraise=True)
               d. Uses default values: new=0 (same window if possible), autoraise=True
            
            3. **System Browser Interaction**:
               a. webbrowser module queries system for default browser
               b. Determines browser executable path from system settings
               c. Launches browser process as subprocess
               d. Passes URL as command-line argument to browser
            
            4. **Browser Window Display**:
               a. Browser application opens (new window or new tab)
               b. Browser navigates to provided URL
               c. For Google Drive links: Drive viewer loads with file
               d. User sees file content in familiar browser environment
            
            5. **Non-Blocking Return**:
               a. webbrowser.open() returns immediately (non-blocking)
               b. Browser runs as separate process (independent of application)
               c. Python application continues execution normally
               d. User can interact with both browser and application
            
            6. **Function Completion**:
               a. Function returns None (no return value needed)
               b. Control returns to event handler
               c. Application remains responsive to user input

        Interactions:
            - **webbrowser**: Python standard library module for browser control

        Example:
            >>> # Open Google Drive file link
            >>> file_link = 'https://drive.google.com/file/d/1abc...xyz/view'
            >>> submission_mgr._open_link(file_link)
            >>> # Browser window opens with file
            >>> 
            >>> # Open any web URL
            >>> submission_mgr._open_link('https://example.com')
            >>> # Browser window opens with website

        See Also:
            - :meth:`view_submissions_dialog`: Uses this for "Open in Browser" button
            - :meth:`_open_drive_file`: Constructs Drive URL from file_id
            - :mod:`webbrowser`: Python webbrowser module documentation

        Notes:
            - Uses system default browser (respects user preference)
            - Non-blocking operation (application continues running)
            - No validation of link format or accessibility
            - Handles both Drive links and general URLs
            - May fail silently if no browser available (rare on desktop)
            - Does not check if link is valid or accessible
        """
        import webbrowser
        webbrowser.open(link)
    
    def _open_drive_file(self, file_id):
        """Open a Google Drive file in the system's default browser.

        Constructs a Google Drive file URL from a file ID and opens it in the
        default web browser. Used when file_link is not stored but file_id is
        available in the submission record.

        Args:
            file_id (str): Google Drive file ID (typically 33-character string
                like '1abc...xyz'). Retrieved from submission record.

        Returns:
            None: Opens browser as side effect. No return value.

        Algorithm:
            1. **URL Construction**:
               a. Define Google Drive file view URL template
               b. Template format: 'https://drive.google.com/file/d/{FILE_ID}/view'
               c. Substitute {FILE_ID} placeholder with file_id parameter
               d. Example result: 'https://drive.google.com/file/d/1abc...xyz/view'
               e. Store complete URL in local variable
            
            2. **Module Import**:
               a. Import webbrowser module from Python standard library
               b. Module provides cross-platform browser control interface
               c. Import occurs at runtime within function scope
            
            3. **Browser Open Command**:
               a. Call webbrowser.open() with constructed URL
               b. Function signature: webbrowser.open(url, new=0, autoraise=True)
               c. Default parameters used:
                  - new=0: reuse existing window if possible
                  - autoraise=True: bring browser window to foreground
            
            4. **System Browser Detection**:
               a. webbrowser module queries operating system
               b. Retrieves user's default web browser setting
               c. Examples: Chrome, Firefox, Safari, Edge
               d. Determines browser executable path
            
            5. **Browser Process Launch**:
               a. Create new subprocess for browser application
               b. Pass constructed Drive URL as argument
               c. Browser process independent from Python application
               d. Non-blocking operation (function returns immediately)
            
            6. **Drive File Display**:
               a. Browser navigates to Google Drive URL
               b. Drive authentication checked (uses existing session if available)
               c. Drive loads file viewer interface
               d. File rendered in appropriate viewer:
                  - Documents: Google Docs viewer
                  - Spreadsheets: Google Sheets viewer
                  - PDFs: Built-in PDF viewer
                  - Images: Image viewer with zoom controls
                  - etc.
            
            7. **Function Return**:
               a. Function completes immediately after browser launch
               b. Returns None (no return value needed)
               c. Control returns to calling event handler
               d. Python application continues execution
               e. User can interact with both browser and application simultaneously

        Interactions:
            - **webbrowser**: Python standard library module for browser control

        Example:
            >>> # Open Drive file by ID
            >>> file_id = '1abc...xyz'
            >>> submission_mgr._open_drive_file(file_id)
            >>> # Browser opens: https://drive.google.com/file/d/1abc...xyz/view
            >>> 
            >>> # Typical usage from submission record
            >>> submission = {
            ...     'file_id': '1abc...xyz',
            ...     'file_name': 'Project.pdf'
            ... }
            >>> submission_mgr._open_drive_file(submission['file_id'])

        See Also:
            - :meth:`view_submissions_dialog`: Uses this for "Open in Browser" button
            - :meth:`_open_link`: Opens pre-constructed URL
            - :class:`~services.drive_service.DriveService`: Drive integration

        Notes:
            - URL format uses Drive's file view endpoint
            - Assumes file_id is valid Google Drive ID (no validation)
            - Non-blocking operation (application continues running)
            - User must have access permissions to view file in browser
            - File opens in browser's Drive viewer (not downloaded)
            - Alternative to storing full webViewLink in submission record
            - Uses standard Drive URL structure (stable API endpoint)
        """
        import webbrowser
        webbrowser.open(f"https://drive.google.com/file/d/{file_id}/view")