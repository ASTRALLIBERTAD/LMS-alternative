---
id: "login_with_token"
sidebar_position: 8
title: "login_with_token"
---

# ⚙️ login_with_token

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`auth_service.py`](./auth_service.py) | **Line:** 240
:::

Authenticate using existing OAuth token from external source.

Bridges external OAuth implementations (like web flows) with Google's
credential system. Validates and refreshes tokens as needed.

## Purpose

- Support server-side OAuth flows
            - Enable custom authentication systems
            - Bridge external OAuth providers

## Parameters

- **`token_data`** (dict): OAuth token information: - access_token (str, required): Current access token - refresh_token (str, optional): Refresh token - client_id (str, optional): Falls back to loaded value - client_secret (str, optional): Falls back to loaded value - scope (str or list, optional): OAuth scopes

## Returns

**Type**: `bool`


## Algorithm

- 1. Validate token_data structure
  - 2. Extract tokens and client credentials
  - 3. Create Credentials object
  - 4. Validate and refresh if needed
  - 5. Persist credentials

## Example

```python
token = {
    'access_token': 'ya29.a0...',
    'refresh_token': '1//0g...',
    'client_id': '123.apps.googleusercontent.com',
    'client_secret': 'abc123'
    }
if auth.login_with_token(token):
    print("Authenticated successfully")
```

## See Also

- `login_desktop()`: Browser-based alternative
- `_validate_and_refresh_credentials()`: Validates tokens

## Notes

- Falls back to stored client credentials
- Refresh token optional but recommended
- Detailed logging for debugging

## Security Considerations

:::note
- Access tokens grant immediate Drive access
            - Refresh tokens allow indefinite access
            - Never log token values in production
:::
