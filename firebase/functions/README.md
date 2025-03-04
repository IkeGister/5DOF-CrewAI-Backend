# Firebase Functions for CrewAI Backend

This directory contains the Firebase Functions that serve as the API layer between client applications and the CrewAI backend system. These functions handle authentication, content management, and production workflow integration.

## 🏗️ Structure

```
functions/
├── src/
│   ├── config/         # Firebase configuration
│   │   ├── firebase.ts
│   │   └── serviceAccount.json
│   ├── controllers/    # Request handlers
│   │   └── contentApproval.ts
│   ├── middleware/     # Auth & validation
│   │   └── auth.ts
│   ├── routes/         # API routes
│   │   └── api.ts
│   ├── services/       # External services
│   │   ├── crewAIService.ts
│   │   └── firebase_service.ts
│   ├── types/          # TypeScript interfaces
│   │   └── index.ts
│   ├── tests/          # API testing
│   │   └── api.test.ts
│   └── index.ts        # Main entry point
├── package.json
└── tsconfig.json
```

## 🚀 Setup

1. Copy `src/config/serviceAccount.example.json` to `src/config/serviceAccount.json`
2. Fill in your service account credentials
3. Never commit the actual serviceAccount.json

## ⚙️ Configuration

Create a `.env` file in the functions directory with the following variables:

```
CREW_AI_BASE_URL=http://localhost:5000  # For local development
FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY=your-api-key-here
```

## 📋 API Endpoints

The API is deployed at: `https://api-yufqiolzaa-uc.a.run.app`

| Method | Endpoint | Description | Example URL |
|--------|----------|-------------|-------------|
| GET | `/api/health` | Health check endpoint | `https://api-yufqiolzaa-uc.a.run.app/api/health` |
| GET | `/api/gists/:userId` | Get all gists for a user | `https://api-yufqiolzaa-uc.a.run.app/api/gists/test_user_1741057003` |
| GET | `/api/gists/:userId/:gistId` | Get specific gist | `https://api-yufqiolzaa-uc.a.run.app/api/gists/test_user_1741057003/gist_1741057003` |
| PUT | `/api/gists/:userId/:gistId/status` | Update gist production status | `https://api-yufqiolzaa-uc.a.run.app/api/gists/test_user_1741057003/gist_1741057003/status` |
| PUT | `/api/gists/:userId/batch/status` | Batch update gists status | `https://api-yufqiolzaa-uc.a.run.app/api/gists/test_user_1741057003/batch/status` |
| PUT | `/api/gists/:userId/:gistId/with-links` | Update gist and associated links | `https://api-yufqiolzaa-uc.a.run.app/api/gists/test_user_1741057003/gist_1741057003/with-links` |
| GET | `/api/links/:userId` | Get all links for a user | `https://api-yufqiolzaa-uc.a.run.app/api/links/test_user_1741057003` |

### Sample Request/Response Data

#### Health Check

**Request:**
```
GET https://api-yufqiolzaa-uc.a.run.app/api/health
Headers:
  X-API-Key: your-api-key-here
```

**Response:**
```json
{
  "status": "ok",
  "message": "API is running"
}
```

#### Get User Gists

**Request:**
```
GET https://api-yufqiolzaa-uc.a.run.app/api/gists/test_user_1741057003
Headers:
  X-API-Key: your-api-key-here
```

**Response:**
```json
{
  "success": true,
  "gists": [
    {
      "gistId": "gist_1741057003",
      "category": "Technology",
      "is_published": true,
      "title": "Tech Trends Gist",
      "link": "https://example.com/tech-article",
      "image_url": "https://example.com/tech-article-image.jpg",
      "ratings": 4,
      "users": 42,
      "status": {
        "in_productionQueue": false,
        "production_status": "In Production - Content Approval Pending",
        "is_done_playing": false,
        "playback_time": 45,
        "is_now_playing": true
      },
      "is_played": false,
      "playback_duration": 180,
      "date_created": "2025-01-25T08:30:00Z",
      "publisher": "theNewGista",
      "segments": [
        {
          "segment_duration": 90,
          "segment_title": "Latest Gadgets",
          "segment_index": 0,
          "segment_audioUrl": "http://someAudioFile.mp3"
        }
      ]
    }
  ]
}
```

#### Get Specific Gist

**Request:**
```
GET https://api-yufqiolzaa-uc.a.run.app/api/gists/test_user_1741057003/gist_1741057003
Headers:
  X-API-Key: your-api-key-here
```

**Response:**
```json
{
  "success": true,
  "data": {
    "gistId": "gist_1741057003",
    "category": "Technology",
    "is_published": true,
    "title": "Tech Trends Gist",
    "link": "https://example.com/tech-article",
    "image_url": "https://example.com/tech-article-image.jpg",
    "ratings": 4,
    "users": 42,
    "status": {
      "in_productionQueue": false,
      "production_status": "In Production - Content Approval Pending",
      "is_done_playing": false,
      "playback_time": 45,
      "is_now_playing": true
    },
    "is_played": false,
    "playback_duration": 180,
    "date_created": "2025-01-25T08:30:00Z",
    "publisher": "theNewGista",
    "segments": [
      {
        "segment_duration": 90,
        "segment_title": "Latest Gadgets",
        "segment_index": 0,
        "segment_audioUrl": "http://someAudioFile.mp3"
      }
    ]
  }
}
```

#### Update Gist Production Status

**Request:**
```
PUT https://api-yufqiolzaa-uc.a.run.app/api/gists/test_user_1741057003/gist_1741057003/status
Headers:
  X-API-Key: your-api-key-here
  Content-Type: application/json
Body:
{
  "production": true
}
```

**Response:**
```json
{
  "error": "inProduction must be a boolean"
}
```

#### Batch Update Gists Status

**Request:**
```
PUT https://api-yufqiolzaa-uc.a.run.app/api/gists/test_user_1741057003/batch/status
Headers:
  X-API-Key: your-api-key-here
  Content-Type: application/json
Body:
{
  "gistIds": ["gist_1741057003"],
  "production": true
}
```

**Response:**
```json
{
  "error": "inProduction must be a boolean"
}
```

#### Update Gist With Links

**Request:**
```
PUT https://api-yufqiolzaa-uc.a.run.app/api/gists/test_user_1741057003/gist_1741057003/with-links
Headers:
  X-API-Key: your-api-key-here
  Content-Type: application/json
Body:
{
  "links": ["link1", "link2"]
}
```

**Response:**
```json
{
  "error": "inProduction must be a boolean"
}
```

#### Get User Links

**Request:**
```
GET https://api-yufqiolzaa-uc.a.run.app/api/links/test_user_1741057003
Headers:
  X-API-Key: your-api-key-here
```

**Response:**
```json
{
  "success": true,
  "links": [
    {
      "category": "Technology",
      "username": "testGistaUser",
      "user_id": "test_user_1741057003",
      "gist_created": {
        "gist_created": true,
        "link_id": "link_1741057003",
        "gist_id": "link_gist_1741057003",
        "link_title": "Tech Resource",
        "image_url": "https://example.com/storage-resource.jpg",
        "link_type": "Web",
        "url": "https://example.com/full-tech-resource"
      },
      "date_added": "2025-01-25T09:00:00Z"
    }
  ]
}
```

## 🔒 Authentication

All API endpoints are protected by API key authentication. Include the following header in all requests:

```
X-API-Key: your-api-key-here
```

### Error Responses

#### Authentication Failure

```json
{
  "status": "ok",
  "message": "API is running"
}
```

Note: The current implementation does not properly validate API keys. This is a security issue that should be addressed.

#### Resource Not Found

```json
{
  "error": "Gist not found"
}
```

#### Invalid Data Format

```json
{
  "error": "Invalid production_status"
}
```

#### Server Error

```json
{
  "success": false,
  "error": "Internal server error"
}
```

## 🔄 Production Workflow

1. Client application sends request to Firebase Functions
2. Firebase Functions authenticate the request
3. Functions interact with Firestore to update/retrieve data
4. When needed, Functions make requests to the CrewAI backend service
5. Functions return results back to the client application

## 🖥️ Local Development

1. Install dependencies:
   ```bash
   npm install
   ```

2. Run the emulator:
   ```bash
   npm run serve
   ```

3. Test locally:
   ```bash
   # Start the local server
   NODE_ENV=development npx ts-node src/index.ts
   
   # Test endpoints with curl
   curl -H "X-API-Key: your-api-key-here" http://localhost:3000/api/health
   curl -H "X-API-Key: your-api-key-here" http://localhost:3000/api/gists/test_user_1741057003
   ```

4. Run the test script:
   ```bash
   # Make the script executable
   chmod +x test-api.sh
   
   # Run the test script
   ./test-api.sh
   ```

## 🧪 Testing

The project includes automated API tests to verify endpoint functionality.

1. Configure your `.env` file with the correct API key
2. Run the tests:
   ```bash
   # Run tests with default user ID
   npm run test:api
   
   # Run tests with a specific user ID
   npm run test:api -- user123
   ```

### Shell Script Testing

You can use the included shell script to test all API endpoints:

```bash
# Make the script executable
chmod +x test-api.sh

# Run the test script
./test-api.sh
```

### Python Script Testing

For more advanced testing, you can use the Python script:

```bash
# Make the script executable
chmod +x test_api.py

# Run the test script with default settings
./test_api.py

# Run with custom settings
./test_api.py --base-url http://localhost:3000 --api-key your-api-key --user-id test_user --verbose
```

The script only requires the `requests` module, which is usually already installed. If not, you can install it with:

```bash
pip install requests
```

Available options:
- `--base-url`: Base URL for the API (default: http://localhost:3000)
- `--api-key`: API key for authentication
- `--user-id`: User ID for testing
- `--gist-id`: Gist ID for testing
- `--save-dir`: Directory to save test results
- `--verbose`: Print verbose output

The script will test all endpoints and save the responses to JSON files in the `test-results` directory.

### Test Results

The test script saves all API responses to the `test-results` directory. These files can be used for documentation and reference:

- `health.json`: Response from the health endpoint
- `gists.json`: Response from the get gists endpoint
- `gist.json`: Response from the get specific gist endpoint
- `links.json`: Response from the get links endpoint
- `update_status.json`: Response from the update gist status endpoint
- `batch_update.json`: Response from the batch update status endpoint
- `update_with_links.json`: Response from the update gist with links endpoint
- `invalid_api_key.json`: Response when using an invalid API key
- `non_existent_user.json`: Response when requesting a non-existent user
- `non_existent_gist.json`: Response when requesting a non-existent gist
- `invalid_json.json`: Response when sending invalid JSON data

These files can be used to understand the API response format and to generate documentation.

### Testing with Postman or Hoppscotch

1. Create a new collection
2. Set up environment variables:
   - `baseUrl`: `https://api-yufqiolzaa-uc.a.run.app`
   - `apiKey`: Your API key

3. Create requests for each endpoint:

   **Health Check:**
   - Method: GET
   - URL: {{baseUrl}}/api/health
   - Headers: X-API-Key: {{apiKey}}

   **Get User Gists:**
   - Method: GET
   - URL: {{baseUrl}}/api/gists/test_user_1741057003
   - Headers: X-API-Key: {{apiKey}}

   **Get Specific Gist:**
   - Method: GET
   - URL: {{baseUrl}}/api/gists/test_user_1741057003/gist_1741057003
   - Headers: X-API-Key: {{apiKey}}

   **Update Gist Status:**
   - Method: PUT
   - URL: {{baseUrl}}/api/gists/test_user_1741057003/gist_1741057003/status
   - Headers: 
     - X-API-Key: {{apiKey}}
     - Content-Type: application/json
   - Body: 
     ```json
     {
       "inProduction": true
     }
     ```

   **Batch Update Gists Status:**
   - Method: PUT
   - URL: {{baseUrl}}/api/gists/test_user_1741057003/batch/status
   - Headers: 
     - X-API-Key: {{apiKey}}
     - Content-Type: application/json
   - Body: 
     ```json
     {
       "gistIds": ["gist_1741057003"],
       "inProduction": true
     }
     ```

   **Update Gist With Links:**
   - Method: PUT
   - URL: {{baseUrl}}/api/gists/test_user_1741057003/gist_1741057003/with-links
   - Headers: 
     - X-API-Key: {{apiKey}}
     - Content-Type: application/json
   - Body: 
     ```json
     {
       "links": ["link1", "link2"],
       "inProduction": true
     }
     ```

   **Get User Links:**
   - Method: GET
   - URL: {{baseUrl}}/api/links/test_user_1741057003
   - Headers: X-API-Key: {{apiKey}}

4. Run the requests and verify responses

### Data Structure

#### User Document

```json
{
  "id": "test_user_1741057003",
  "username": "testGistaUser",
  "email": "test@example.com",
  "createdAt": "2023-06-01T10:00:00.000Z",
  "gists": [
    {
      "gistId": "gist_1741057003",
      "category": "Technology",
      "is_published": true,
      "title": "Tech Trends Gist",
      "link": "https://example.com/tech-article",
      "image_url": "https://example.com/tech-article-image.jpg",
      "ratings": 4,
      "users": 42,
      "status": {
        "in_productionQueue": false,
        "production_status": "In Production - Content Approval Pending",
        "is_done_playing": false,
        "playback_time": 45,
        "is_now_playing": true
      },
      "is_played": false,
      "playback_duration": 180,
      "date_created": "2025-01-25T08:30:00Z",
      "publisher": "theNewGista",
      "segments": [
        {
          "segment_duration": 90,
          "segment_title": "Latest Gadgets",
          "segment_index": 0,
          "segment_audioUrl": "http://someAudioFile.mp3"
        }
      ]
    }
  ],
  "links": [
    {
      "category": "Technology",
      "username": "testGistaUser",
      "user_id": "test_user_1741057003",
      "gist_created": {
        "gist_created": true,
        "link_id": "link_1741057003",
        "gist_id": "link_gist_1741057003",
        "link_title": "Tech Resource",
        "image_url": "https://example.com/storage-resource.jpg",
        "link_type": "Web",
        "url": "https://example.com/full-tech-resource"
      },
      "date_added": "2025-01-25T09:00:00Z"
    }
  ]
}
```

## 🚀 Deployment

```bash
# Deploy from the functions directory
cd firebase/functions
firebase deploy --only functions
```

The deployment will provide you with the function URL, which will be in the format:
`https://api-yufqiolzaa-uc.a.run.app`

## 🔄 Integration with CrewAI Backend

The Firebase Functions communicate with the CrewAI backend service via HTTP requests. The `crewAIService.ts` file contains methods for interacting with the CrewAI API.

Example workflow:
1. Function receives request to update a gist's production status
2. Function updates status in Firestore
3. Function calls CrewAI backend to process the content
4. CrewAI returns results which are stored in Firestore
5. Client is notified of the status change 

# Firebase Admin SDK Implementation

This project uses the Firebase Admin SDK to interact with Firestore and other Firebase services. The implementation follows best practices for authentication and security.

## Authentication Options

There are two main ways to authenticate with Firebase:

### 1. Application Default Credentials (ADC) - Recommended

This is the recommended approach for production environments. It uses the Google Cloud Platform's Application Default Credentials mechanism.

#### Setup:

1. Install the Google Cloud SDK: https://cloud.google.com/sdk/docs/install
2. Login with your Google account:
   ```bash
   gcloud auth login
   ```
3. Set up application default credentials:
   ```bash
   gcloud auth application-default login
   ```
4. Initialize Firebase without explicit credentials:
   ```typescript
   import * as admin from 'firebase-admin';
   admin.initializeApp();
   ```

### 2. Service Account Key - For Development

For local development, you can use a service account key file.

#### Setup:

1. Go to the Firebase Console > Project Settings > Service accounts
2. Click "Generate new private key"
3. Save the JSON file securely
4. Place the file in one of these locations:
   - `firebase/functions/serviceAccountKey.json` (preferred)
   - Project root directory as `serviceAccountKey.json`
5. The code will automatically detect and use the service account key

## Running Tests

The test suite includes comprehensive tests for Firebase connectivity and API functionality:

```bash
cd firebase/functions
npm test
```

Or run the test file directly:

```bash
npx ts-node src/tests/api.test.ts
```

## Firebase Collections

The main collections used in this project are:

- `users`: User profiles and metadata with nested `gists` and `links` arrays

### Firestore Data Structure

The Firestore database uses a nested structure where each user document contains arrays for gists and links:

```
users/
  ├── user_id_1/
  │   ├── username: string
  │   ├── email: string
  │   ├── createdAt: timestamp
  │   ├── gists: array [
  │   │   ├── {
  │   │   │   gistId: string,
  │   │   │   category: string,
  │   │   │   is_published: boolean,
  │   │   │   title: string,
  │   │   │   link: string,
  │   │   │   image_url: string,
  │   │   │   ratings: number,
  │   │   │   users: number,
  │   │   │   status: {
  │   │   │     in_productionQueue: boolean,
  │   │   │     production_status: string,
  │   │   │     is_done_playing: boolean,
  │   │   │     playback_time: number,
  │   │   │     is_now_playing: boolean
  │   │   │   },
  │   │   │   is_played: boolean,
  │   │   │   playback_duration: number,
  │   │   │   date_created: timestamp,
  │   │   │   publisher: string,
  │   │   │   segments: array
  │   │   }
  │   │   │
  │   │   └── ...
  │   │
  │   ├── links: array [
  │   │   ├── {
  │   │   │   category: string,
  │   │   │   username: string,
  │   │   │   user_id: string,
  │   │   │   gist_created: {
  │   │   │     gist_created: boolean,
  │   │   │     link_id: string,
  │   │   │     gist_id: string,
  │   │   │     link_title: string,
  │   │   │     image_url: string,
  │   │   │     link_type: string,
  │   │   │     url: string
  │   │   │   },
  │   │   │   date_added: timestamp
  │   │   │
  │   │   └── ...
  │   │
  │   └── user_id_2/
  │       ├── ...
```

## Best Practices Implemented

1. **Authentication**: Using ADC for secure authentication
2. **Collection References**: Exporting collection references for consistent access
3. **Error Handling**: Comprehensive error handling with helpful messages
4. **Testing**: Thorough testing of Firebase connectivity and operations
5. **Security**: No hardcoded credentials in the codebase

## Troubleshooting

If you encounter authentication issues:

1. Check that you've run `gcloud auth application-default login`
2. Verify that your account has the necessary permissions for the Firebase project
3. For local development, ensure your service account key is in the correct location
4. Run the Firebase connection test to diagnose issues:
   ```bash
   npx ts-node src/tests/api.test.ts
   ```

### Common Error Messages

**API Key Authentication Failure:**
```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing API key"
}
```

**Resource Not Found:**
```json
{
  "error": "Gist not found"
}
```

**Invalid Data Format:**
```json
{
  "error": "inProduction must be a boolean"
}
```

**Server Error:**
```json
{
  "success": false,
  "error": "Internal server error"
}
``` 