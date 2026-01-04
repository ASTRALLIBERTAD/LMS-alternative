---
id: "setup_paths"
sidebar_position: 2
title: "setup_paths"
---

# ⚙️ setup_paths

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`main.py`](./main.py) | **Line:** 39
:::

Configure Python module import paths for application execution.

Adds the application source directory and current working directory to
Python's sys.path to enable proper module imports regardless of how the
application is launched (direct execution, packaged, or from different
working directories). Ensures project modules can be imported consistently.

## Purpose

- Enable module imports from application directory
        - Support execution from different working directories
        - Ensure consistent import behavior across platforms
        - Prepare environment for application initialization

## Returns

**Type**: `tuple`

            - app_path (str): Absolute path to the application source directory
              where main.py is located. Used for locating resource files.
            - cwd (str): Current working directory at application startup.
              Used for locating user data and configuration files.

## Algorithm

- **Phase 1: Determine Application Path**
  - 1. Get absolute path of current file (__file__)
  - 2. Extract directory path using os.path.dirname()
  - 3. Store in app_path variable
  - 4. This is the src directory containing main.py

- **Phase 2: Get Current Working Directory**
  - 1. Call os.getcwd() to get current directory
  - 2. Store in cwd variable
  - 3. This is where user launched application

- **Phase 3: Update sys.path**
  - 1. Create list: [cwd, app_path]
  - 2. For each path in list:
    - a. Check if path already in sys.path
    - b. If not present:
    - - Call sys.path.insert(0, path)
    - - Adds to beginning of path (highest priority)
  - 3. Enables imports from both locations

- **Phase 4: Return Paths**
  - 1. Return tuple (app_path, cwd)
  - 2. Caller can use paths for resource loading

## Interactions

- **os.path.abspath()**: Gets absolute file path
- **os.path.dirname()**: Extracts directory from path
- **os.getcwd()**: Gets current working directory
- **sys.path.insert()**: Adds import paths to Python

## Example

```python
app_path, cwd = setup_paths()
print(f"Application directory: {app_path}")
# Application directory: /home/user/lms/src
print(f"Working directory: {cwd}")
# Working directory: /home/user/lms

# Now can import project modules
from services.auth_service import GoogleAuth
from ui.dashboard import Dashboard
```

## See Also

- `main()`: Calls this during initialization
- `sys`: Python system module for path manipulation

## Notes

- Paths inserted at position 0 (highest priority)
- Avoids duplicate entries in sys.path
- Safe to call multiple times (idempotent)
- app_path is where source code lives
- cwd is where user launched application
- Both paths may be same if launched from src directory
