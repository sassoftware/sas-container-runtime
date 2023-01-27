# CHANGES

> Note: If you plan to use this for a large number of calls, connection pooling must be implemented.

## Planned

- Implement connection pooling.
- Switch to redis-node V4 - makes for cleaner code with the async functions.
- Switch logging to morgan or watson package.

## 1.0.0

- First release.

## 1.1.0

Planned changes:

- Replace depends_on with link since Azure Apps do not support depends_on.
- Figure out why the UI for redis cannot resolve an Azure url for the database.
