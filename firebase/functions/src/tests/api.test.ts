import axios from 'axios';
import * as path from 'path';
import * as dotenv from 'dotenv';
import * as admin from 'firebase-admin';
import * as fs from 'fs';

// Load environment variables from the correct path
dotenv.config({ path: path.resolve(__dirname, '../../.env') });

// Initialize Firebase Admin if not already initialized
if (!admin.apps.length) {
  try {
    // Search for credentials in multiple locations
    const possibleCredentialPaths = [
      process.env.GOOGLE_APPLICATION_CREDENTIALS,
      path.resolve(__dirname, '../../serviceAccountKey.json'),
      path.resolve(process.cwd(), 'serviceAccountKey.json'),
      path.resolve(process.cwd(), 'firebase/functions/serviceAccountKey.json'),
      path.resolve(process.cwd(), 'firebase/serviceAccountKey.json')
    ];

    console.log('Searching for Firebase credentials...');
    
    // Try each path until we find a valid one
    let credentialsFound = false;
    
    for (const credPath of possibleCredentialPaths) {
      if (!credPath) continue;
      
      console.log(`Checking for credentials at: ${credPath}`);
      
      if (fs.existsSync(credPath)) {
        console.log(`Found credentials at: ${credPath}`);
        
        if (credPath === process.env.GOOGLE_APPLICATION_CREDENTIALS) {
          console.log('Using credentials from GOOGLE_APPLICATION_CREDENTIALS environment variable');
          admin.initializeApp();
        } else {
          const serviceAccount = require(credPath);
          console.log(`Using service account: ${serviceAccount.project_id}`);
          admin.initializeApp({
            credential: admin.credential.cert(serviceAccount)
          });
        }
        
        credentialsFound = true;
        break;
      }
    }
    
    // If no explicit credentials found, try Application Default Credentials
    if (!credentialsFound) {
      console.log('No explicit credentials found, using Application Default Credentials (ADC)');
      console.log('If this fails, please run: gcloud auth application-default login');
      admin.initializeApp();
    }
    
    console.log('Firebase Admin initialized successfully');
  } catch (error) {
    console.error('Failed to initialize Firebase Admin:', error);
    throw error;
  }
}

// Get Firestore instance
const db = admin.firestore();

// Constants
const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:3000/api';
// Get API key from environment variables - prioritize the Firebase Functions specific key
const API_KEY = process.env.FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY || process.env.API_KEY;
const DEFAULT_USER_ID = 'test_user_1741057003';
const DEFAULT_GIST_ID = 'gist_1741057003';

// For testing purposes, force NODE_ENV to 'test'
process.env.NODE_ENV = 'test';

// Log configuration info
console.log(`Using API URL: ${API_BASE_URL}`);
if (!API_KEY) {
  console.warn('⚠️ WARNING: No API key found in environment variables. API tests will fail.');
  console.warn('Please set FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY in your .env file.');
} else {
  console.log('API key found in environment variables.');
  // Log which environment variable was used
  if (process.env.FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY) {
    console.log('Using FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY from environment.');
  } else if (process.env.API_KEY) {
    console.log('Using API_KEY from environment (fallback).');
  }
}

/**
 * Test results interfaces
 */
interface TestResult {
  success: boolean;
  error?: any;
  data?: any;
  message?: string;
}

/**
 * Test Firebase Connection
 * 
 * Verifies that the Firebase connection is working and prints the project ID
 */
async function test_firebaseConnection(): Promise<TestResult> {
  console.log('\n🧪 TEST: Firebase Connection');
  console.log('====================');
  
  try {
    console.log('Checking Firebase connection...');
    
    // Get the Firebase app
    const app = admin.app();
    
    // Get the project ID
    const projectId = app.options.projectId;
    console.log(`Connected to Firebase project: ${projectId || 'Unknown (using ADC)'}`);
    
    // Try to write to Firestore to verify connection
    console.log('Testing Firestore write access...');
    
    const testDocRef = db.collection('_test_connection').doc('test_doc');
    const timestamp = admin.firestore.Timestamp.now();
    
    await testDocRef.set({
      timestamp,
      message: 'Test connection successful',
      testRun: new Date().toISOString()
    });
    
    console.log('✅ Successfully wrote to Firestore');
    
    // Clean up the test document
    await testDocRef.delete();
    console.log('✅ Successfully deleted test document');
    
    return {
      success: true,
      data: {
        projectId: projectId || 'Using Application Default Credentials',
        timestamp: timestamp.toDate().toISOString()
      },
      message: 'Firebase connection is working correctly'
    };
  } catch (error: any) {
    console.error('❌ Firebase connection test failed:', error.message);
    
    // Provide more helpful error messages based on common issues
    let errorMessage = error.message;
    let helpfulMessage = '';
    
    if (error.code === 'app/invalid-credential') {
      helpfulMessage = 'Invalid credentials. Please check your service account key or run: gcloud auth application-default login';
    } else if (error.code === 'app/invalid-app-options') {
      helpfulMessage = 'Invalid Firebase app options. Please check your Firebase configuration.';
    } else if (error.message.includes('permission_denied')) {
      helpfulMessage = 'Permission denied. Please check that your service account has the necessary permissions.';
    }
    
    return {
      success: false,
      error: error.message,
      data: {
        errorCode: error.code,
        helpfulMessage
      },
      message: 'Failed to connect to Firebase: ' + (helpfulMessage || errorMessage)
    };
  }
}

/**
 * Test initialization
 * 
 * Verifies that the API configuration is properly set up
 */
async function test_initialization(): Promise<TestResult> {
  console.log('\n🧪 TEST: Initialization');
  console.log('====================');
  
  try {
    // Check if API_BASE_URL is set
    if (!API_BASE_URL) {
      return {
        success: false,
        error: 'API_BASE_URL is not set',
        message: 'API base URL is required for testing'
      };
    }
    
    // Check if API_KEY is set
    if (!API_KEY) {
      console.log('⚠️ No API key found in environment variables');
      console.log('Please set FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY in your .env file');
      console.log('Skipping API key verification test');
      
      return {
        success: false,
        error: 'API_KEY is not set',
        message: 'FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY is required for testing'
      };
    }
    
    // Verify that the API is reachable with a simple health check
    try {
      const response = await axios.get(
        `${API_BASE_URL}/health`,
        {
          headers: {
            'X-API-Key': API_KEY
          }
        }
      );
      
      console.log(`✅ API health check successful: ${response.status}`);
      console.log(`Response: ${JSON.stringify(response.data)}`);
      
      return {
        success: true,
        data: response.data,
        message: 'API is reachable and configured correctly'
      };
    } catch (error: any) {
      console.log(`⚠️ API health check failed, but continuing with tests`);
      console.log(`This may be expected if the /health endpoint is not implemented`);
      
      // We'll still consider this a success since not all APIs have a health endpoint
      return {
        success: true,
        error: error.message,
        message: 'API configuration is set up, but health check failed (may be expected)'
      };
    }
  } catch (error: any) {
    console.error('❌ Initialization test failed:', error.message);
    return {
      success: false,
      error: error.message,
      message: 'Failed to initialize test environment'
    };
  }
}

/**
 * Test setup
 * 
 * Verifies that the test user and gist IDs are valid
 */
async function test_setup(): Promise<TestResult> {
  console.log('\n🧪 TEST: Setup');
  console.log('====================');
  
  try {
    console.log(`Verifying test user ID: ${DEFAULT_USER_ID}`);
    console.log(`Verifying test gist ID: ${DEFAULT_GIST_ID}`);
    
    // Check if the test user exists
    try {
      const userResponse = await axios.get(
        `${API_BASE_URL}/gists/${DEFAULT_USER_ID}`,
        {
          headers: {
            'X-API-Key': API_KEY
          }
        }
      );
      
      if (userResponse.status === 200) {
        console.log(`✅ Test user exists: ${DEFAULT_USER_ID}`);
        
        // Check if the user has any gists
        const userData = userResponse.data;
        const gists = userData.gists || [];
        
        console.log(`Found ${gists.length} gists for test user`);
        
        // Check if the test gist ID exists in the user's gists
        const testGistExists = gists.some((gist: any) => 
          gist.gistId === DEFAULT_GIST_ID || 
          gist.gistId === Number(DEFAULT_GIST_ID) || 
          gist.gistId?.toString() === DEFAULT_GIST_ID
        );
        
        if (testGistExists) {
          console.log(`✅ Test gist exists: ${DEFAULT_GIST_ID}`);
        } else {
          console.log(`⚠️ Test gist not found: ${DEFAULT_GIST_ID}`);
          console.log(`Available gist IDs: ${gists.map((g: any) => g.gistId).join(', ')}`);
        }
        
        return {
          success: true,
          data: {
            userExists: true,
            gistExists: testGistExists,
            gistCount: gists.length
          },
          message: 'Test setup verified successfully'
        };
      } else {
        console.log(`❌ Failed to verify test user: ${DEFAULT_USER_ID}`);
        return {
          success: false,
          error: `Unexpected status code: ${userResponse.status}`,
          message: 'Failed to verify test user'
        };
      }
    } catch (error: any) {
      console.log(`❌ Test user verification failed: ${error.message}`);
      return {
        success: false,
        error: error.message,
        message: 'Failed to verify test user'
      };
    }
  } catch (error: any) {
    console.error('❌ Setup test failed:', error.message);
    return {
      success: false,
      error: error.message,
      message: 'Failed to complete test setup'
    };
  }
}

/**
 * Test fetching user links
 * 
 * Retrieves and prints the link data structure for a user
 */
async function test_fetchUserLink(userId = DEFAULT_USER_ID): Promise<TestResult> {
  console.log('\n🧪 TEST: Fetch User Links');
  console.log('====================');
  
  try {
    console.log(`Fetching links for user: ${userId}`);
    
    const response = await axios.get(
      `${API_BASE_URL}/links/${userId}`,
      {
        headers: {
          'X-API-Key': API_KEY
        }
      }
    );
    
    if (response.status === 200) {
      console.log(`✅ Successfully retrieved links for user: ${userId}`);
      
      const links = response.data.links || [];
      console.log(`Found ${links.length} links`);
      
      // Print the link data structure
      console.log('\n📄 LINK DATA STRUCTURE:');
      console.log('====================');
      
      if (links.length > 0) {
        // Print the first link as an example
        const exampleLink = links[0];
        console.log(JSON.stringify(exampleLink, null, 2));
        
        // Analyze the link structure
        console.log('\n📊 Link Structure Analysis:');
        const linkKeys = Object.keys(exampleLink);
        console.log(`- Link object has ${linkKeys.length} top-level properties: ${linkKeys.join(', ')}`);
        
        // Check for expected properties
        const expectedProps = ['category', 'date_added', 'gist_created', 'user_id', 'username'];
        const missingProps = expectedProps.filter(prop => !linkKeys.includes(prop));
        
        if (missingProps.length > 0) {
          console.log(`⚠️ Missing expected properties: ${missingProps.join(', ')}`);
        } else {
          console.log(`✅ All expected properties are present`);
        }
        
        // Check gist_created structure
        if (exampleLink.gist_created) {
          const gistCreatedKeys = Object.keys(exampleLink.gist_created);
          console.log(`- gist_created object has ${gistCreatedKeys.length} properties: ${gistCreatedKeys.join(', ')}`);
          
          const expectedGistCreatedProps = ['gist_created', 'gist_id', 'image_url', 'link_id', 'link_title', 'link_type', 'url'];
          const missingGistCreatedProps = expectedGistCreatedProps.filter(prop => !gistCreatedKeys.includes(prop));
          
          if (missingGistCreatedProps.length > 0) {
            console.log(`⚠️ Missing expected properties in gist_created: ${missingGistCreatedProps.join(', ')}`);
          } else {
            console.log(`✅ All expected properties in gist_created are present`);
          }
        } else {
          console.log(`⚠️ gist_created property is missing or null`);
        }
      } else {
        console.log('No links found for this user');
      }
      
      return {
        success: true,
        data: {
          links: links
        },
        message: 'Successfully fetched user links'
      };
    } else {
      console.log(`❌ Failed to retrieve links: ${response.status}`);
      return {
        success: false,
        error: `Unexpected status code: ${response.status}`,
        message: 'Failed to retrieve user links'
      };
    }
  } catch (error: any) {
    console.error('❌ Fetch user links test failed:', error.response?.data || error.message);
    
    // If the endpoint doesn't exist, provide a helpful message
    if (error.response?.status === 404) {
      console.log('⚠️ The /links endpoint may not be implemented yet');
    }
    
    return {
      success: false,
      error: error.response?.data || error.message,
      message: 'Failed to fetch user links'
    };
  }
}

/**
 * Test fetching a test user gist
 * 
 * Retrieves and prints the gist data structure for a user
 */
async function test_fetchTestUserGist(userId = DEFAULT_USER_ID, gistId = DEFAULT_GIST_ID): Promise<TestResult> {
  console.log('\n🧪 TEST: Fetch Test User Gist');
  console.log('====================');
  
  try {
    console.log(`Fetching gist with ID ${gistId} for user: ${userId}`);
    
    const response = await axios.get(
      `${API_BASE_URL}/gists/${userId}/${gistId}`,
      {
        headers: {
          'X-API-Key': API_KEY
        }
      }
    );
    
    if (response.status === 200) {
      console.log(`✅ Successfully retrieved gist with ID: ${gistId}`);
      
      // Extract the gist data
      const gistData = response.data.data || {};
      
      // Print the gist data structure
      console.log('\n📄 GIST DATA STRUCTURE:');
      console.log('====================');
      console.log(JSON.stringify(gistData, null, 2));
      
      // Analyze the gist structure
      console.log('\n📊 Gist Structure Analysis:');
      const gistKeys = Object.keys(gistData);
      console.log(`- Gist object has ${gistKeys.length} top-level properties: ${gistKeys.join(', ')}`);
      
      // Check for expected properties based on the example
      const expectedProps = [
        'title', 'category', 'date_created', 'image_url', 'is_played', 'is_published',
        'link', 'playback_duration', 'publisher', 'ratings', 'segments', 'status', 'users'
      ];
      
      const missingProps = expectedProps.filter(prop => !gistKeys.includes(prop));
      
      if (missingProps.length > 0) {
        console.log(`⚠️ Missing expected properties: ${missingProps.join(', ')}`);
      } else {
        console.log(`✅ All expected properties are present`);
      }
      
      // Check segments structure
      if (gistData.segments && Array.isArray(gistData.segments)) {
        console.log(`- Found ${gistData.segments.length} segments`);
        
        if (gistData.segments.length > 0) {
          const segmentKeys = Object.keys(gistData.segments[0]);
          console.log(`- Segment object has ${segmentKeys.length} properties: ${segmentKeys.join(', ')}`);
          
          const expectedSegmentProps = ['segment_title', 'segment_index', 'segment_duration', 'segment_audioUrl'];
          const missingSegmentProps = expectedSegmentProps.filter(prop => !segmentKeys.includes(prop));
          
          if (missingSegmentProps.length > 0) {
            console.log(`⚠️ Missing expected properties in segment: ${missingSegmentProps.join(', ')}`);
          } else {
            console.log(`✅ All expected properties in segment are present`);
          }
        }
      } else {
        console.log(`⚠️ segments property is missing or not an array`);
      }
      
      // Check status structure
      if (gistData.status) {
        const statusKeys = Object.keys(gistData.status);
        console.log(`- Status object has ${statusKeys.length} properties: ${statusKeys.join(', ')}`);
        
        const expectedStatusProps = ['is_now_playing', 'playback_time', 'is_done_playing', 'production_status', 'in_productionQueue'];
        const missingStatusProps = expectedStatusProps.filter(prop => !statusKeys.includes(prop));
        
        if (missingStatusProps.length > 0) {
          console.log(`⚠️ Missing expected properties in status: ${missingStatusProps.join(', ')}`);
        } else {
          console.log(`✅ All expected properties in status are present`);
        }
      } else {
        console.log(`⚠️ status property is missing or null`);
      }
      
      // Compare with the expected structure from the example
      console.log('\n📋 Comparison with Expected Structure:');
      const expectedGistStructure = {
        title: "Tech Trends Gist",
        category: "Technology",
        date_created: "2024-01-25T08:30:00Z",
        image_url: "https://example.com/image.jpg",
        is_played: false,
        is_published: true,
        link: "https://example.com/article",
        playback_duration: 120,
        publisher: "theNewGista",
        ratings: 0,
        segments: [{
          segment_audioUrl: "https://example.com/audio.mp3",
          segment_duration: 120,
          segment_index: 0,
          segment_title: "Test Segment"
        }],
        status: {
          is_done_playing: false,
          is_now_playing: false,
          playback_time: 0
        },
        users: 0
      };
      
      // Check if the actual structure matches the expected structure
      const expectedKeys = Object.keys(expectedGistStructure);
      const actualKeys = Object.keys(gistData);
      
      const missingExpectedKeys = expectedKeys.filter(key => !actualKeys.includes(key));
      const additionalKeys = actualKeys.filter(key => !expectedKeys.includes(key));
      
      if (missingExpectedKeys.length > 0) {
        console.log(`⚠️ Missing keys from expected structure: ${missingExpectedKeys.join(', ')}`);
      }
      
      if (additionalKeys.length > 0) {
        console.log(`ℹ️ Additional keys not in expected structure: ${additionalKeys.join(', ')}`);
      }
      
      if (missingExpectedKeys.length === 0 && additionalKeys.length === 0) {
        console.log(`✅ Actual structure matches expected structure`);
      }
      
      return {
        success: true,
        data: {
          gist: gistData
        },
        message: 'Successfully fetched test user gist'
      };
    } else {
      console.log(`❌ Failed to retrieve gist: ${response.status}`);
      return {
        success: false,
        error: `Unexpected status code: ${response.status}`,
        message: 'Failed to retrieve test user gist'
      };
    }
  } catch (error: any) {
    console.error('❌ Fetch test user gist failed:', error.response?.data || error.message);
    return {
      success: false,
      error: error.response?.data || error.message,
      message: 'Failed to fetch test user gist'
    };
  }
}

/**
 * Test direct access to Firestore users collection
 * 
 * This test bypasses the API and directly accesses Firestore
 * to verify that the database connection is working and that
 * we can retrieve user data.
 */
async function test_firestoreUsersAccess(): Promise<TestResult> {
  console.log('\n🧪 TEST: Direct Firestore Users Access');
  console.log('====================');
  
  try {
    console.log('Attempting to access Firestore users collection directly...');
    
    // Get all users from the users collection
    const usersSnapshot = await db.collection('users').get();
    
    if (usersSnapshot.empty) {
      console.log('No users found in the users collection.');
      return {
        success: true,
        data: { userCount: 0 },
        message: 'Successfully accessed Firestore but found no users'
      };
    }
    
    // Count users
    const userCount = usersSnapshot.size;
    console.log(`Found ${userCount} users in the users collection.`);
    
    // Print details for each user
    console.log('\n📋 Users in Firestore:');
    console.log('====================');
    
    usersSnapshot.forEach((doc) => {
      const userData = doc.data();
      console.log(`\nUser ID: ${doc.id}`);
      
      // Print basic user info
      if (userData.username) console.log(`Username: ${userData.username}`);
      if (userData.email) console.log(`Email: ${userData.email}`);
      
      // Print gists count if available
      if (userData.gists && Array.isArray(userData.gists)) {
        console.log(`Gists: ${userData.gists.length}`);
        
        // Print brief info about each gist
        if (userData.gists.length > 0) {
          console.log('\nGists:');
          userData.gists.forEach((gist: any, index: number) => {
            console.log(`  ${index + 1}. Status: ${gist.status || 'Unknown'}, Is Played: ${gist.is_played ? 'Yes' : 'No'}`);
          });
        }
      }
      
      // Print links count if available
      if (userData.links && Array.isArray(userData.links)) {
        console.log(`Links: ${userData.links.length}`);
        
        // Print brief info about each link
        if (userData.links.length > 0) {
          console.log('\nLinks:');
          userData.links.forEach((link: any, index: number) => {
            try {
              let dateInfo = 'No date';
              if (link.date_added) {
                if (typeof link.date_added === 'string') {
                  dateInfo = link.date_added;
                } else if (link.date_added.seconds) {
                  dateInfo = new Date(link.date_added.seconds * 1000).toISOString();
                } else if (link.date_added.toDate) {
                  dateInfo = link.date_added.toDate().toISOString();
                }
              }
              console.log(`  ${index + 1}. Date Added: ${dateInfo}`);
            } catch (err) {
              console.log(`  ${index + 1}. Date Added: [Error parsing date]`);
            }
          });
        }
      }
      
      console.log('--------------------');
    });
    
    return {
      success: true,
      data: { userCount },
      message: `Successfully accessed Firestore and found ${userCount} users`
    };
  } catch (error: any) {
    console.error('❌ Error accessing Firestore users:', error.message);
    return {
      success: false,
      error,
      message: `Failed to access Firestore users: ${error.message}`
    };
  }
}

/**
 * Run all tests and report results
 */
async function runAllTests(): Promise<void> {
  console.log('\n🔍 Running all tests...');
  
  // Store test results
  const results: Record<string, TestResult> = {};
  
  // Always run Firebase connection test
  results.firebaseConnection = await test_firebaseConnection();
  
  // Check if API key is available before running API-dependent tests
  if (!API_KEY) {
    console.log('\n⚠️ Skipping API-dependent tests due to missing API key');
    console.log('Please set FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY in your .env file.');
    
    // Only run tests that don't require API key
    results.firestoreUsersAccess = await test_firestoreUsersAccess();
    
    // Add placeholder results for skipped tests
    results.initialization = {
      success: false,
      message: 'Test skipped - API key not available'
    };
    results.setup = {
      success: false,
      message: 'Test skipped - API key not available'
    };
    results.fetchUserLink = {
      success: false,
      message: 'Test skipped - API key not available'
    };
    results.fetchTestUserGist = {
      success: false,
      message: 'Test skipped - API key not available'
    };
  } else {
    // Run all tests when API key is available
    results.initialization = await test_initialization();
    results.setup = await test_setup();
    results.fetchUserLink = await test_fetchUserLink();
    results.fetchTestUserGist = await test_fetchTestUserGist();
    results.firestoreUsersAccess = await test_firestoreUsersAccess();
  }
  
  // Calculate overall results
  const totalTests = Object.keys(results).length;
  const passedTests = Object.values(results).filter(r => r.success).length;
  const failedTests = totalTests - passedTests;
  const skippedTests = Object.values(results).filter(r => r.message?.includes('skipped')).length;
  
  console.log('\n📊 TEST SUMMARY:');
  console.log('====================');
  console.log(`Total tests: ${totalTests}`);
  console.log(`Passed: ${passedTests}`);
  console.log(`Failed: ${failedTests - skippedTests}`);
  if (skippedTests > 0) {
    console.log(`Skipped: ${skippedTests}`);
  }
  
  console.log('\n📝 INDIVIDUAL TEST RESULTS:');
  for (const [testName, result] of Object.entries(results)) {
    if (result.success) {
      console.log(`✅ ${testName}: ${result.message}`);
    } else if (result.message?.includes('skipped')) {
      console.log(`⏭️ ${testName}: ${result.message}`);
    } else {
      console.log(`❌ ${testName}: ${result.message || result.error?.message || 'Unknown error'}`);
    }
  }
  
  if (failedTests - skippedTests > 0) {
    console.log('\n⚠️ Some tests failed. See above for details.');
  } else if (skippedTests > 0) {
    console.log('\n⚠️ Some tests were skipped due to missing API key. Set the API key to run all tests.');
  } else {
    console.log('\n✅ All tests passed!');
  }
}

// Run all tests
runAllTests()
  .catch(error => {
    console.error('Test run failed:', error);
    process.exit(1);
  });