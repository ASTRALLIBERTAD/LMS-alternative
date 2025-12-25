"""Notification Service Module.

This module manages system notices and user alerts. It supports both internal
logging of notifications (saved to JSON) and optional desktop notifications
using the `plyer` library if available.

Classes:
    NotificationService: Handles creation, storage, and retrieval of notifications.

See Also:
    `Plyer Documentation <https://pypi.org/project/plyer/>`_
"""

import json
import datetime
from pathlib import Path


try:
    from plyer import notification as os_notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False
    print("plyer not installed - using in-app notifications only")


class NotificationService:
    """Manages application notifications and alerts.

    Handles persistence of notification history to JSON and dispatches
    OS-level notifications when possible.

    Attributes:
        data_dir (Path): Directory for storing notification data.
        notifications_file (Path): Path to the JSON storage file.
        notifications (list): In-memory list of notification records.

    Algorithm (Pseudocode):
        1. Initialize storage directory.
        2. Load existing notifications from JSON.
        3. On send_notification: add to list, save to file.
        4. If plyer available, trigger OS notification.
        5. Provide methods to filter, count unread, and mark read.
    """
    def __init__(self, data_dir: Path = None):
        """Initialize the NotificationService.

        Args:
            data_dir (Path, optional): Custom directory for data storage.
        """
        self.data_dir = data_dir or Path("lms_data")
        self.data_dir.mkdir(exist_ok=True)
        self.notifications_file = self.data_dir / "notifications.json"
        self.notifications = self.load_notifications()
    
    def load_notifications(self):
        """Load notifications from the local JSON file.

        Returns:
            list: List of notification dictionaries.
        """
        if self.notifications_file.exists():
            try:
                with open(self.notifications_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("notifications", [])
            except:
                pass
        return []
    
    def save_notifications(self):
        """Save current notifications list to disk."""
        with open(self.notifications_file, 'w', encoding='utf-8') as f:
            json.dump({"notifications": self.notifications}, f, indent=2, ensure_ascii=False)
    
    def send_notification(self, title: str, message: str, student_email: str = None, assignment_id: str = None, notification_type: str = "info"):
        """Create and dispatch a notification.

        Args:
            title (str): Notification title.
            message (str): Notification body content.
            student_email (str, optional): Recipient email.
            assignment_id (str, optional): Related assignment ID.
            notification_type (str): Category (info, warning, etc.).

        Returns:
            bool: True if OS notification triggered, False otherwise.

        Algorithm:
            1. Construct notification record with timestamp.
            2. Append to internal list and save to disk.
            3. Attempt to show OS notification via plyer.
        """
        notification_record = {
            "id": str(datetime.datetime.now().timestamp()),
            "type": notification_type,
            "title": title,
            "message": message,
            "student_email": student_email,
            "assignment_id": assignment_id,
            "created_at": datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
            "read": False
        }
        self.notifications.append(notification_record)
        self.save_notifications()
        
        if PLYER_AVAILABLE:
            try:
                os_notification.notify(
                    title=title,
                    message=message,
                    app_name="LMS Assignment Manager",
                    timeout=10
                )
                return True
            except Exception as e:
                print(f"OS notification failed: {e}")
        
        return False
    
    def notify_new_assignment(self, assignment: dict, students: list):
        """Notify students of a newly created assignment.

        Args:
            assignment (dict): Assignment details.
            students (list): List of student records.

        Algorithm:
            1. Create notification message.
            2. Send individual notifications to each student.
            3. Send single OS summary notification to instructor.
        """
        title = f"New Assignment: {assignment.get('title', 'Untitled')}"
        message = f"Subject: {assignment.get('subject', 'N/A')}\nDeadline: {assignment.get('deadline', 'No deadline')}"
        
        os_notified = False
        
        for student in students:
            student_email = student.get('email')
            self.send_notification(
                title=title,
                message=message,
                student_email=student_email,
                assignment_id=assignment.get('id'),
                notification_type="new_assignment"
            )
            
            if not os_notified and PLYER_AVAILABLE:
                try:
                    os_notification.notify(
                        title=title,
                        message=f"{message}\nAssigned to {len(students)} students",
                        app_name="LMS Assignment Manager",
                        timeout=10
                    )
                    os_notified = True
                except:
                    pass
    
    def notify_deadline_reminder(self, assignment: dict, student_email: str, hours_remaining: int):
        """Send a deadline reminder to a student.

        Args:
            assignment (dict): Assignment details.
            student_email (str): Student's email.
            hours_remaining (int): Time left in hours.
        """
        title = f"Deadline Reminder: {assignment.get('title', 'Assignment')}"
        message = f"Only {hours_remaining} hours remaining to submit!"
        
        self.send_notification(
            title=title,
            message=message,
            student_email=student_email,
            assignment_id=assignment.get('id'),
            notification_type="deadline_reminder"
        )
    
    def notify_submission_received(self, assignment: dict, student_name: str):
        """Notify instructor that a submission has been made.

        Args:
            assignment (dict): Assignment details.
            student_name (str): Name of submitting student.
        """
        title = f"Submission Received"
        message = f"{student_name} submitted: {assignment.get('title', 'Assignment')}"
        
        self.send_notification(
            title=title,
            message=message,
            assignment_id=assignment.get('id'),
            notification_type="submission_received"
        )
    
    def notify_grade_posted(self, assignment: dict, student_email: str, grade: str):
        """Notify student of a posted grade.

        Args:
            assignment (dict): Assignment details.
            student_email (str): Student's email.
            grade (str): The assigned grade.
        """
        title = f"Grade Posted: {assignment.get('title', 'Assignment')}"
        message = f"Your grade: {grade}"
        
        self.send_notification(
            title=title,
            message=message,
            student_email=student_email,
            assignment_id=assignment.get('id'),
            notification_type="grade_posted"
        )
    
    def get_notifications_for_student(self, student_email: str):
        """Retrieve notifications relevant to a specific student.

        Args:
            student_email (str): The student's email filter.

        Returns:
            list: List of notification dictionaries.
        """
        return [n for n in self.notifications 
                if n.get('student_email') == student_email or n.get('student_email') is None]
    
    def get_unread_count(self, student_email: str = None):
        """Count unread notifications.

        Args:
            student_email (str, optional): Filter by student.

        Returns:
            int: Number of unread items.
        """
        if student_email:
            relevant = self.get_notifications_for_student(student_email)
        else:
            relevant = self.notifications
        return sum(1 for n in relevant if not n.get('read', False))
    
    def mark_as_read(self, notification_id: str):
        """Mark a single notification as read.

        Args:
            notification_id (str): Notification ID.

        Returns:
            bool: True if found and updated.
        """
        for n in self.notifications:
            if n.get('id') == notification_id:
                n['read'] = True
                self.save_notifications()
                return True
        return False
    
    def mark_all_as_read(self, student_email: str = None):
        """Mark all notifications (filtered by student) as read.

        Args:
            student_email (str, optional): Filter by student.
        """
        for n in self.notifications:
            if student_email is None or n.get('student_email') == student_email:
                n['read'] = True
        self.save_notifications()
    
    def clear_old_notifications(self, days: int = 30):
        """Delete notifications older than a specified duration.

        Args:
            days (int): Retention duration in days.
        """
        cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
        self.notifications = [
            n for n in self.notifications
            if datetime.datetime.strptime(n['created_at'], '%Y-%m-%d %H:%M') > cutoff
        ]
        self.save_notifications()
