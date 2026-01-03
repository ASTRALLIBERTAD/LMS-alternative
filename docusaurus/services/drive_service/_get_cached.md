---
id: "_get_cached"
sidebar_position: 5
title: "_get_cached"
---

# ⚙️ _get_cached

![Has Examples](https://img.shields.io/badge/Examples-✓-green) ![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue) ![Completeness](https://img.shields.io/badge/Docs-60%25-orange)

:::info Source
**File:** [`drive_service.py`](./drive_service.py) | **Line:** 319
:::

Retrieve data from time-based cache if not expired.

Checks if cached data exists and is still valid based on TTL
(time-to-live). Automatically removes expired entries.

## Parameters

- **`key`** (str): Cache key to lookup. Typically formatted as operation_parameter format (e.g., "files_root_100_None").

## Returns

**Type**: `Any`

                or expired. Return type matches cached data type (typically
                dict or list for Drive operations).

## Algorithm

  - 1. **Check Key Existence**:
    - a. If key in self._cache dictionary:
    - i. Proceed to validation
    - b. If key not in cache:
    - i. Return None (cache miss)

  - 2. **Extract Cache Entry**:
    - a. Get tuple from cache: (data, timestamp)
    - b. data: The cached response data
    - c. timestamp: datetime when cached

  - 3. **Validate Timestamp**:
    - a. Calculate age: datetime.now() - timestamp
    - b. Compare age to self._cache_ttl
    - c. If age < cache_ttl:
    - i. Data still valid
    - ii. Return data
    - d. If age &gt;= cache_ttl:
    - i. Data expired
    - ii. Delete cache entry
    - iii. Return None (expired)

## Interactions

- **datetime.now()**: Gets current timestamp
- **timedelta**: Calculates time differences

## Example

```python
# Internal usage by public methods
cached = drive._get_cached('files_root_100_None')
if cached:
    print("Cache hit!")
    return cached
    else:
    print("Cache miss, calling API...")
```

## See Also

- `_set_cache()`: Stores data in cache
- `_invalidate_cache()`: Clears cache entries

## Notes

- Automatically removes expired entries
- TTL set during initialization (default 300s)
- Returns None for both miss and expiration
- Cache keys are operation-specific strings
- Expired entries deleted to free memory
