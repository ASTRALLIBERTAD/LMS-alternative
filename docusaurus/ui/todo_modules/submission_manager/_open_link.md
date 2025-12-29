---
id: "_open_link"
sidebar_position: 9
title: "_open_link"
---

# ⚙️ _open_link

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`submission_manager.py`](./submission_manager.py) | **Line:** 1440
:::

Open a web link in the system's default browser.

Launches the default web browser with the provided URL. Used to open
Google Drive file links from the submission grading interface.

## Parameters

- **`link`** (str): Full URL to open in browser. Should include protocol (e.g., '[https://drive.google.com/file/d/...'](https://drive.google.com/file/d/...')).

## Returns

**Type**: `None`


## Algorithm

- 1. **Module Import**:
    - a. Import webbrowser module from Python standard library
    - b. Module provides interface to system's web browser
    - c. Import occurs at runtime (not at module level)

  - 2. **Browser Invocation**:
    - a. Call webbrowser.open() function
    - b. Pass link parameter as URL string argument
    - c. Function signature: webbrowser.open(url, new=0, autoraise=True)
    - d. Uses default values: new=0 (same window if possible), autoraise=True

  - 3. **System Browser Interaction**:
    - a. webbrowser module queries system for default browser
    - b. Determines browser executable path from system settings
    - c. Launches browser process as subprocess
    - d. Passes URL as command-line argument to browser

  - 4. **Browser Window Display**:
    - a. Browser application opens (new window or new tab)
    - b. Browser navigates to provided URL
    - c. For Google Drive links: Drive viewer loads with file
    - d. User sees file content in familiar browser environment

  - 5. **Non-Blocking Return**:
    - a. webbrowser.open() returns immediately (non-blocking)
    - b. Browser runs as separate process (independent of application)
    - c. Python application continues execution normally
    - d. User can interact with both browser and application

  - 6. **Function Completion**:
    - a. Function returns None (no return value needed)
    - b. Control returns to event handler
    - c. Application remains responsive to user input

## Interactions

- **webbrowser**: Python standard library module for browser control

## Example

```python
# Open Google Drive file link
file_link = 'https://drive.google.com/file/d/1abc...xyz/view'
submission_mgr._open_link(file_link)
# Browser window opens with file

# Open any web URL
submission_mgr._open_link('https://example.com')
# Browser window opens with website
```

## See Also

- `view_submissions_dialog()`: Uses this for "Open in Browser" button
- `_open_drive_file()`: Constructs Drive URL from file_id
- `webbrowser`: Python webbrowser module documentation

## Notes

- Uses system default browser (respects user preference)
- Non-blocking operation (application continues running)
- No validation of link format or accessibility
- Handles both Drive links and general URLs
- May fail silently if no browser available (rare on desktop)
- Does not check if link is valid or accessible
