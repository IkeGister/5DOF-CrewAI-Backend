# CrewAI Backend Tests

This directory contains test scripts for the CrewAI Backend Firebase project. The tests cover both database operations and API endpoints for both the original and subcollection-based database structures.

## Unified Test Architecture

We've created a unified test architecture to eliminate redundancies and standardize testing for both database structures:

```
tests/
├── unified_test_utils.js          # Shared utilities for all tests
├── unified_test_setup.js          # Creates test data for both structures
├── unified_database_tests.js      # Database operation tests for both structures
├── unified_api_tests.js           # API endpoint tests for both structures
├── run_unified_tests.js           # Runner for all tests
└── ... (legacy test files)
```

## Setup

Before running tests, make sure you have installed all dependencies:

```bash
npm install
```

Also, ensure that you have:

1. Firebase CLI installed globally: `npm install -g firebase-tools`
2. Firebase emulators installed: `firebase setup:emulators:firestore`
3. Proper API key configured in your environment or in a `.env` file

## Running Tests

### Unified Test Runner

The unified test runner can run all tests in sequence:

```bash
node tests/run_unified_tests.js
```

You can also run specific test modules:

```bash
# Just set up test data
node tests/run_unified_tests.js setup

# Only run database tests
node tests/run_unified_tests.js database

# Only run API tests
node tests/run_unified_tests.js api
```

### Individual Test Files

You can run individual test files directly:

```bash
# Set up test data
node tests/unified_test_setup.js

# Run database tests
node tests/unified_database_tests.js

# Run API tests
node tests/unified_api_tests.js
```

## Test Data Structure

The test suite creates the following test data:

- Test user: `crewAI-backend-tester`
- Test gist with link: `gist_35e92f298ea2453489a14d0869509c10`
- Test gist without links: `gist_with_no_links`
- Test link: `link_primary`

The test data is created in both the original structure (nested gists and links) and the new subcollection structure.

## Test Environment

By default, tests run against the local Firebase emulator. To run against production:

1. Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to your service account key file
2. Set the `API_BASE_URL` to your deployed function URL
3. Set the `SUBCOLLECTION_API_BASE_URL` to your deployed subcollection function URL
4. Set the `API_KEY` to your production API key

## Legacy Test Files

The following legacy test files are kept for reference but will be phased out:

- `test_database_operations.js` - Tests for original structure
- `test_api_endpoint.js` - API tests for original structure
- `test_database_operations_subcollections.js` - Tests for subcollection structure
- `test_api_endpoint_subcollections.js` - API tests for subcollection structure

## Environment Variables

The following environment variables can be configured:

- `API_KEY` - API key for authentication
- `API_BASE_URL` - Base URL for the original API
- `SUBCOLLECTION_API_BASE_URL` - Base URL for the subcollection API
- `GOOGLE_APPLICATION_CREDENTIALS` - Path to service account for Firebase Auth

## Troubleshooting

If tests fail, check these common issues:

1. **Firebase Emulator Not Running**: Start it with `firebase emulators:start`
2. **Missing Test Data**: Run `node tests/unified_test_setup.js` to create test data
3. **Environment Variables**: Make sure API keys and URLs are correctly set
4. **API Server Not Running**: Deploy or start the Firebase functions locally 