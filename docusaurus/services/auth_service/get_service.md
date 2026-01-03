---
id: "get_service"
sidebar_position: 13
title: "get_service"
---

# ⚙️ get_service

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 975
:::

Create and return authenticated Google Drive API v3 service.

Builds a Google Drive API service object for making API requests.
Requires valid authentication and automatically refreshes expired
tokens before creating service.

## Returns

**Type**: `googleapiclient.discovery.Resource or None`

                service object configured with authenticated credentials,
                or None if not authenticated or service creation failed.

## Algorithm

- **Phase 1: Check Authentication**
  - 1. Call self.is_authenticated()
  - 2. If False:
  - 3. Print "Cannot get service - not authenticated"
    - a. Return None immediately

- **Phase 2: Try Service Creation**
  - 1. Enter try block for error handling
  - 2. Call build('drive', 'v3', credentials=self.creds)
  - 3. 'drive': Google Drive API
    - a. 'v3': API version 3
    - b. credentials: OAuth credentials object
  - 4. Returns Resource object for API calls
  - 5. Store in service variable
  - 6. Print "Google Drive service created"
  - 7. Return service object

- **Phase 3: Handle Errors**
  - 1. Catch any Exception during service creation
  - 2. Print error message with exception details
  - 3. Return None (service creation failed)

## Interactions

- **is_authenticated()**: Validates and refreshes credentials
- **googleapiclient.discovery.build()**: Creates API service
- **Credentials**: Provides authentication for service

## Example

```python
# Get service for API calls
auth = GoogleAuth()
auth.login_desktop()
service = auth.get_service()
# Google Drive service created

# Use service for Drive operations
if service:
    results = service.files().list(pageSize=10).execute()
    files = results.get('files', [])
    for file in files:
    print(file['name'])

# Not authenticated
auth2 = GoogleAuth()
service = auth2.get_service()
# Cannot get service - not authenticated
print(service)
# None
```

## See Also

- `is_authenticated()`: Validates authentication
- `DriveService`: Wraps this service
- `Drive API Reference <[https://developers.google.com/drive/api/v3/reference>`_](https://developers.google.com/drive/api/v3/reference>`_)

## Notes

- Requires valid authentication (checked automatically)
- Automatically refreshes expired tokens
- Returns None if not authenticated
- Service object used for all Drive API calls
- DriveService class typically wraps this service
- API version v3 is current stable version
