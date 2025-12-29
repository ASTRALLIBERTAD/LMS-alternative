---
id: "get_user_info"
sidebar_position: 14
title: "get_user_info"
---

# ⚙️ get_user_info

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 1037
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

- 1. **Try Getting User Info**:
    - a. Enter try block for error handling
    - b. Call self.get_service() to get Drive service
    - c. If service is None:
    - i. Not authenticated
    - ii. Return empty dict &#123;&#125;

  - 2. **Make API Call**:
    - a. Call service.about().get(fields="user").execute()
    - i. about(): Endpoint for account info
    - ii. get(): Retrieve information
    - iii. fields="user": Request only user fields
    - iv. execute(): Perform API request
    - b. Store response in about variable

  - 3. **Extract User Data**:
    - a. Get 'user' field from response: about.get('user', &#123;&#125;)
    - b. Store in user variable
    - c. Extract email: user.get('emailAddress', 'unknown')
    - d. Print success message with email
    - e. Return user dictionary

  - 4. **Handle Errors**:
    - a. Catch any Exception during API call
    - b. Print error message with exception details
    - c. Return empty dict &#123;&#125; (API call failed)

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
