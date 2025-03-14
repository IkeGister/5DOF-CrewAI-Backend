# CrewAI Backend Database Structure

This document describes the database structure for the CrewAI Backend application. The database is organized using Firestore collections and subcollections for optimal performance and scalability.

## User-Gist-Link Relationship

The core of the application revolves around three main entities:

1. **Users** - People using the CrewAI platform
2. **Gists** - Content snippets or articles created or saved by users
3. **Links** - Web links associated with gists

## Database Structure

The database is structured using subcollections to maintain clean separation and efficient querying:

```
/users/{userId}/                       # User document with basic user information
    /gists/{gistId}/                   # Gist subcollection - individual gists owned by a user
        /links/{linkId}/               # Links subcollection - links associated with a specific gist
    /links/{linkId}/                   # General links subcollection - all links owned by a user (can reference gists)
```

### User Document Structure

**Collection Path**: `/users/{userId}`

```json
{
  "id": "string",          // User ID, same as the document ID
  "username": "string",    // Username for display
  "email": "string",       // User's email address
  "createdAt": "timestamp", // When the user was created
  "updatedAt": "timestamp"  // When the user was last updated
}
```

### Gist Document Structure

**Collection Path**: `/users/{userId}/gists/{gistId}`

```json
{
  "id": "string",          // Gist ID, same as the document ID
  "title": "string",       // Gist title
  "content": "string",     // Gist content or description
  "category": "string",    // Category or topic
  "is_played": "boolean",  // Whether the gist has been played
  "is_published": "boolean", // Whether the gist is published
  "link": "string",        // Direct link URL (optional)
  "image_url": "string",   // Image URL (optional)
  "publisher": "string",   // Publisher name
  "playback_duration": "number", // Duration in seconds
  "ratings": "number",     // User ratings
  "segments": [            // Audio segments (optional)
    {
      "segment_title": "string",
      "segment_audioUrl": "string",
      "playback_duration": "string",
      "segment_index": "string"
    }
  ],
  "status": {              // Production status
    "inProduction": "boolean",
    "production_status": "string" // 'draft', 'review', 'published'
  },
  "createdAt": "timestamp", // When the gist was created
  "updatedAt": "timestamp"  // When the gist was last updated
}
```

### Link Document Structure

**Collection Path**: `/users/{userId}/gists/{gistId}/links/{linkId}` OR `/users/{userId}/links/{linkId}`

```json
{
  "id": "string",          // Link ID, same as the document ID
  "url": "string",         // The URL of the link
  "title": "string",       // Link title
  "description": "string", // Link description
  "category": "string",    // Link category
  "date_added": "timestamp", // When the link was added
  "gistId": "string",      // Reference to parent gist (if applicable)
  "inProduction": "boolean", // Whether the link is in production
  "production_status": "string", // 'draft', 'review', 'published'
  "updatedAt": "timestamp"  // When the link was last updated
}
```

## Benefits of This Structure

This structure offers several advantages:

1. **Direct Access** - You can access any gist or link directly with its ID without loading the entire user document
2. **Efficient Updates** - You can update a single gist or link without retrieving all user data
3. **Scalability** - Each user can have thousands of gists and links without performance degradation
4. **Query Flexibility** - You can easily query all gists by a specific user or all links for a specific gist
5. **Security Rules** - You can apply granular security rules at each level

## Data Access Patterns

Common data access patterns include:

- Get a user: `db.collection('users').doc(userId).get()`
- Get all gists for a user: `db.collection('users').doc(userId).collection('gists').get()`
- Get a specific gist: `db.collection('users').doc(userId).collection('gists').doc(gistId).get()`
- Get all links for a gist: `db.collection('users').doc(userId).collection('gists').doc(gistId).collection('links').get()`
- Get all links for a user: `db.collection('users').doc(userId).collection('links').get()`

## Migration

If you're migrating from a structure where gists and links were stored as arrays or objects within the user document, the `update_user_structure.js` and `create_subcollection_test_data.js` scripts in the `tests` directory demonstrate how to transition to this new structure.

## Using This Structure in Code

The `firebase_service_subcollections.ts` file provides service functions for working with this structure, including functions for retrieving, creating, and updating users, gists, and links.

## Test Data

For testing purposes, a test user with ID `crewAI-backend-tester` is created with sample gists and links. This data can be used to test the API and database operations.

To create the test data, run:

```
node tests/create_subcollection_test_data.js
``` 