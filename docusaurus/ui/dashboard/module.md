---
id: "module"
sidebar_position: 1
title: "Module"
---

# 📁 Module

![Completeness](https://img.shields.io/badge/Docs-0%25-red)

:::info Source
**File:** [`dashboard.py`](./dashboard.py) | **Line:** 1
:::

Dashboard UI Module - Main application interface for LMS.

This module provides the primary dashboard interface for the Learning Management
System, integrating Google Drive file management, folder navigation, assignment
tracking, and multi-account support. It serves as the central hub coordinating
all major UI components and backend services.

## Purpose

- Provide unified interface for Google Drive file operations
    - Coordinate file management, navigation, and assignment modules  
    - Handle responsive layouts across desktop and mobile devices
    - Manage view states and user session information
    - Support multi-account switching and authentication

## Interactions

- **Flet Framework**: Cross-platform UI rendering and event handling
- **Google Drive API**: File and folder operations via DriveService
- **OAuth2**: User authentication and session management
- **Multi-Account Manager**: Account switching and storage

## See Also

- `DriveService`: Google Drive API wrapper
- `TodoView`: Assignment management view
- `FileManager`: File operations handler
- `FolderNavigator`: Navigation manager
- `PasteLinksManager`: Link processor

## Notes

- Implements responsive design with 900px breakpoint for mobile/desktop
- Uses Flet framework for cross-platform UI rendering
- Integrates with Google Drive API v3 for file operations
- Supports OAuth2 authentication with multi-account capability
- All file operations are delegated to specialized manager modules

## References

- Google Drive API v3: https://developers.google.com/drive/api/v3/reference
- Flet Framework: https://flet.dev/docs/
