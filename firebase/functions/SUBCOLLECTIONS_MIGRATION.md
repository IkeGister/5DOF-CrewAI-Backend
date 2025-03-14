# Migrating to the Subcollection-Based Structure

This document explains how to migrate from the old structure where gists and links were stored directly in the user document to the new subcollection-based structure.

## Benefits of Subcollection Structure

The new structure offers several advantages:

1. **Direct Access** - You can access any gist or link directly with its ID without loading the entire user document
2. **Efficient Updates** - You can update a single gist or link without retrieving all user data
3. **Scalability** - Each user can have thousands of gists and links without performance degradation
4. **Query Flexibility** - You can easily query all gists by a specific user or all links for a specific gist
5. **Security Rules** - You can apply granular security rules at each level

See `DATABASE_STRUCTURE.md` for more details on the new structure.

## Migration Steps

### 1. Create Test Data

First, create test data using the new structure to verify it works correctly:

```bash
node tests/create_subcollection_test_data.js
```

This will create a test user with gists and links using the subcollection structure.

### 2. Migrate Existing Users

To migrate an existing user from the old structure to the new structure:

```bash
node tests/update_user_structure.js
```

This will:
1. Retrieve an existing user document
2. Create a new user document with the subcollection structure
3. Convert gists and links to subcollections

You can modify this script to migrate specific users or all users in your database.

### 3. Use Subcollection-Based Services

Instead of using the original service files, use the subcollection-based versions:

- `firebase_service_subcollections.ts` - Core database operations
- `gistOperations_subcollections.ts` - Higher-level gist operations
- `contentApproval_subcollections.ts` - API controllers
- `api_subcollections.ts` - API routes
- `index_subcollections.ts` - Main Firebase function

### 4. Deploy with the Subcollection Structure

To deploy the API with the new subcollection structure:

```bash
firebase deploy --only functions:api --config firebase.subcollections.json
```

You'll need to create a `firebase.subcollections.json` configuration file that uses the subcollection-based entry point.

## Switching Between Structures

During the migration period, you might want to maintain both implementations:

### Original Structure

- Database: `/users/{userId}` with gists and links as properties
- Firebase Function: `firebase_service.ts` → `gistOperations.ts` → `contentApproval.ts` → `api.ts` → `index.ts`

### Subcollection Structure

- Database: `/users/{userId}/gists/{gistId}` and `/users/{userId}/gists/{gistId}/links/{linkId}`
- Firebase Function: `firebase_service_subcollections.ts` → `gistOperations_subcollections.ts` → `contentApproval_subcollections.ts` → `api_subcollections.ts` → `index_subcollections.ts`

## Testing the New Structure

1. Create test data as described above
2. Manually verify through the Firebase Console that the data is structured correctly
3. Run the API tests against the new structure:

```bash
API_BASE_URL=http://localhost:5001/your-project/us-central1/api-subcollections node tests/test_api_endpoint.js
```

## Rollback Plan

If there are issues with the new structure, you can continue using the original structure until they're resolved. The original files remain untouched.

## Complete Migration

Once you've verified that everything works correctly with the new structure:

1. Migrate all users from the old structure to the new structure
2. Update any client applications to work with the new API responses
3. Replace the original implementation with the subcollection-based one
4. Deploy the updated functions 