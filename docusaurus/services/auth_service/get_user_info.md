---
id: "get_user_info"
sidebar_position: 14
title: "get_user_info"
---

# ⚙️ get_user_info

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 1061
:::

Retrieve authenticated user's Google account information.

Fetches user details from the Google Drive API including email address,
display name, and profile information. Requires valid authentication.

## Returns

**Type**: `dict`

                - emailAddress (str): User's email
                - displayName (str): User's display name
                - photoLink (str): Profile photo URL
                - permissionId (str): User's permission ID
                Returns empty dict &#123;&#125; if not authenticated or API call fails.

## Algorithm

- **Phase 1: Try Getting User Info**
  - 1. Enter try block for error handling
  - 2. Call self.get_service() to get Drive service
  - 3. If service is None:
  - 4. Not authenticated
    - a. Return empty dict &#123;&#125;

- **Phase 2: Make API Call**
  - 1. Call service.about().get(fields="user").execute()
  - 2. about(): Endpoint for account info
    - a. get(): Retrieve information
    - b. fields="user": Request only user fields
    - c. execute(): Perform API request
  - 3. Store response in about variable

- **Phase 3: Extract User Data**
  - 1. Get 'user' field from response: about.get('user', &#123;&#125;)
  - 2. Store in user variable
  - 3. Extract email: user.get('emailAddress', 'unknown')
  - 4. Print success message with email
  - 5. Return user dictionary

- **Phase 4: Handle Errors**
  - 1. Catch any Exception during API call
  - 2. Print error message with exception details
  - 3. Return empty dict &#123;&#125; (API call failed)

## Interactions

- **get_service()**: Gets authenticated Drive service
- **Drive API about().get()**: Retrieves user information

## Example

```python
# Get user info
auth = GoogleAuth()
auth.login_desktop()
user_info = auth.get_user_info()
# ✓ User info retrieved: user@example.com

print(user_info)
# {
# 'emailAddress': 'user@example.com',
# 'displayName': 'John Doe',
# 'photoLink': 'https://...',
# 'permissionId': '...'
# }

# Display user email
print(f"Logged in as: {user_info.get('emailAddress')}")
# Logged in as: user@example.com

# Not authenticated
auth2 = GoogleAuth()
user_info = auth2.get_user_info()
print(user_info)
# {}
```

## See Also

- `get_service()`: Gets authenticated Drive service
- `is_authenticated()`: Validates authentication
- `Drive API About <[https://developers.google.com/drive/api/v3/reference/about>`_](https://developers.google.com/drive/api/v3/reference/about>`_)

## Notes

- Requires valid authentication
- Returns empty dict if not authenticated
- Returns empty dict on API errors
- Email address used for displaying logged-in user
- Single API call to get user information
- Useful for displaying current user in UI
