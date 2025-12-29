---
id: "_get_submission_status"
sidebar_position: 7
title: "_get_submission_status"
---

# ⚙️ _get_submission_status

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`submission_manager.py`](./submission_manager.py) | **Line:** 1256
:::

Retrieve submission record for specific assignment and student.

Searches the submissions list for a matching record based on assignment
ID and student email. Used to determine submission status when displaying
assignment lists or grading interfaces.

## Parameters

- **`assignment_id`** (str): Unique identifier of the assignment to search for.
- **`student_email`** (str): Email address of the student to search for.

## Returns

**Type**: `dict or None`

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

## Algorithm

- 1. **Initialize Search**:
    - a. Begin iteration through self.todo.submissions list
    - b. Each element 'sub' represents a submission dictionary

  - 2. **Match Criteria Check**:
    - a. For current submission 'sub' in iteration:
    - i. Extract sub['assignment_id'] value
    - ii. Compare with provided assignment_id parameter
    - iii. Store boolean result of comparison
    - b. Extract sub['student_email'] value
    - c. Compare with provided student_email parameter
    - d. Store boolean result of comparison

  - 3. **Match Evaluation**:
    - a. If both conditions are True (AND logic):
    - i. Assignment ID matches provided ID
    - ii. Student email matches provided email
    - b. Return the complete submission dictionary immediately
    - c. Exit function with found submission

  - 4. **Continue Search**:
    - a. If either condition is False:
    - i. Continue to next iteration of loop
    - ii. Check next submission in list

  - 5. **No Match Found**:
    - a. If loop completes without finding match:
    - i. All submissions have been checked
    - ii. No matching record exists
    - b. Return None to indicate submission not found

  - 6. **Return Value Interpretation**:
    - a. If return is dict: submission exists for this student+assignment
    - b. If return is None: student has not submitted this assignment
    - c. Caller can use truthiness check or explicit None comparison

## Interactions

- **TodoView**: Accesses submissions list via self.todo.submissions

## Example

```python
# Check if student has submitted assignment
sub = submission_mgr._get_submission_status(
    'assign_123',
    'student@example.com'
    )
if sub:
    print(f"Submitted at: {sub['submitted_at']}")
    print(f"Grade: {sub.get('grade', 'Not graded')}")
    else:
    print("No submission found")
# Submitted at: 2025-12-30 10:00
# Grade: 95/100
```

## See Also

- `submit_assignment_dialog()`: Creates submission records
- `view_submissions_dialog()`: Uses this to check submission status
- `DataManager`: Persists submission data

## Notes

- Linear search through submissions list (O(n) complexity)
- Returns first match found (submissions should be unique per student+assignment)
- Used internally by other methods to avoid duplicate submissions
- Does not modify the submission record
