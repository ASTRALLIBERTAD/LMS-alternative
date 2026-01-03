---
id: "get_redirect_url"
sidebar_position: 5
title: "get_redirect_url"
---

# ⚙️ get_redirect_url

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-40%25-red)

:::info Source
**File:** [`main.py`](./main.py) | **Line:** 384
:::

Get the OAuth 2.0 redirect URL for desktop authentication.

Returns the localhost callback URL used for OAuth authentication on
desktop platforms. This URL must match the authorized redirect URIs
configured in Google Cloud Console for the OAuth client.

## Returns

**Type**: `str`

            "http://localhost:8550/oauth_callback". Port 8550 chosen to
            avoid conflicts with common services.

## Algorithm

- **Phase 1: Return Static URL**:
  - 1. Return hardcoded string: "http://localhost:8550/oauth_callback"
  - 2. No computation or configuration needed
  - 3. Must match Google Console settings

## Interactions

- **GoogleOAuthProvider**: Uses this URL for OAuth configuration

## Example

```python
url = get_redirect_url()
print(url)
# http://localhost:8550/oauth_callback

# Used in OAuth provider setup
provider = GoogleOAuthProvider(
    client_id=client_id,
    redirect_url=get_redirect_url()
    )
```

## See Also

- `main()`: Uses this for OAuth provider configuration
- `GoogleAuth`: Implements OAuth flow
- `GoogleOAuthProvider`: OAuth provider

## Notes

- Port 8550 chosen to avoid common conflicts
- Must be authorized in Google Cloud Console
- Desktop authentication only (not mobile)
- Local HTTP server listens on this port during auth
- URL format must be exact: ``http://localhost:&#123;PORT&#125;/&#123;PATH&#125;``
- No HTTPS for localhost (not required by Google)
