---
id: "_retry_request"
sidebar_position: 8
title: "_retry_request"
---

# ⚙️ _retry_request

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`drive_service.py`](./drive_service.py) | **Line:** 509
:::

Execute API request with exponential backoff retry logic.

Attempts API request multiple times with increasing delays on
transient failures. Handles rate limits, timeouts, and server errors.

## Parameters

- **`request_func`** (Callable): Function to execute that returns API response. Should be parameterless lambda or closure wrapping the actual API call. Example: lambda: service.files().list().execute()
- **`operation_name`** (str, optional): Descriptive name for logging purposes. Helps identify which operation failed. Defaults to "operation".

## Returns

**Type**: `Any`

                all retries exhausted. Return type depends on API endpoint.

## Algorithm

  - 1. **Retry Loop**:
    - a. For attempt in range(max_retries):
    - i. Attempt index: 0 to max_retries-1

  - 2. **Try Request Execution**:
    - a. Enter try block
    - b. Call request_func() to execute API request
    - c. If successful, return result immediately

  - 3. **Handle Errors**:
    - a. Catch TimeoutError, HttpError, or generic Exception
    - b. Determine if error is retryable:
    - i. TimeoutError: Always retryable
    - ii. HttpError with status 429 (rate limit): Retryable
    - iii. HttpError with status 500/503 (server error): Retryable
    - iv. Other HttpError: Not retryable
    - v. Other Exception: Retryable if not last attempt

  - 4. **Retry Decision**:
    - a. If should_retry AND not last attempt:
    - i. Calculate delay: self.retry_delay * (2 ** attempt)
    - - Attempt 0: 1s, Attempt 1: 2s, Attempt 2: 4s, etc.
    - ii. Print retry message with operation, attempt, delay
    - iii. Sleep for calculated delay
    - iv. Continue to next iteration
    - b. If final attempt or non-retryable:
    - i. Print final error message
    - ii. Return None (failure)

  - 5. **Exhausted Retries**:
    - a. If loop completes without return
    - b. Return None (all retries failed)

## Interactions

- **time.sleep()**: Implements backoff delay
- **googleapiclient.errors.HttpError**: HTTP error detection

## Example

```python
# Internal usage for API calls
def make_request():
    return self.service.files().list(q='...').execute()

result = drive._retry_request(make_request, "list_files")
if result:
    print("Success!")
else:
    print("Failed after retries")

# Handles rate limits automatically
# 429 error -> wait 1s -> retry
# 429 error -> wait 2s -> retry
# Success -> return result
```

## See Also

- `_execute_file_list_query()`: Uses this for queries
- `_execute_file_mutation()`: Uses this for mutations

## Notes

- Exponential backoff prevents request storms
- Rate limit (429) always retried
- Server errors (500, 503) retried
- Client errors (400, 404) not retried
- Timeout errors always retried
- Logs all retry attempts
- Returns None on final failure
- Max delay: retry_delay * (2 ** (max_retries - 1))
