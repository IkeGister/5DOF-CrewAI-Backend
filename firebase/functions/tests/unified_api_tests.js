/**
 * Unified API Tests
 * 
 * This script tests API endpoints for both the original and subcollection structures.
 * It tests the update gist production status endpoint.
 */

const axios = require('axios');
const { 
  initializeFirebase, 
  TEST_DATA, 
  logColor, 
  testBanner, 
  logTestResult
} = require('./unified_test_utils');

// Initialize Firebase
const admin = initializeFirebase();
const db = admin.firestore();

// Configure axios defaults
axios.defaults.validateStatus = () => true; // Don't throw on error status codes

// Test results
const results = {
  original: {
    passed: 0,
    failed: 0,
    skipped: 0,
    tests: {}
  },
  subcollection: {
    passed: 0,
    failed: 0,
    skipped: 0,
    tests: {}
  }
};

// API base URLs
const apiUrls = {
  original: process.env.API_BASE_URL || 'http://localhost:5001/your-project/us-central1/api',
  subcollection: process.env.SUBCOLLECTION_API_BASE_URL || 'http://localhost:5001/your-project/us-central1/api_subcollections'
};

// API Key
const apiKey = process.env.API_KEY || TEST_DATA.apiKey;

/**
 * Test original structure API
 */
async function testOriginalApi() {
  testBanner('Testing Original Structure API');
  
  try {
    // Test health check
    try {
      const result = await testHealthCheck(apiUrls.original);
      if (result.success) {
        logTestResult('Health Check', true, result.message);
        results.original.passed++;
        results.original.tests['Health Check'] = 'PASS';
      } else {
        throw new Error(result.message);
      }
    } catch (error) {
      logTestResult('Health Check', false, error.message);
      results.original.failed++;
      results.original.tests['Health Check'] = 'FAIL';
      // Skip other tests if health check fails
      logColor('Skipping remaining tests due to health check failure', 'yellow');
      return;
    }
    
    // Test update gist production status
    try {
      const result = await testUpdateGistProductionStatus(apiUrls.original);
      if (result.success) {
        logTestResult('Update Gist Production Status', true, result.message);
        results.original.passed++;
        results.original.tests['Update Gist Production Status'] = 'PASS';
      } else {
        throw new Error(result.message);
      }
    } catch (error) {
      // This may be expected if the gist doesn't exist
      if (error.message.includes('not found')) {
        logTestResult('Update Gist Production Status', false, `Expected failure: ${error.message}`);
        results.original.tests['Update Gist Production Status'] = 'FAIL (Expected)';
        results.original.failed++;
      } else {
        logTestResult('Update Gist Production Status', false, error.message);
        results.original.failed++;
        results.original.tests['Update Gist Production Status'] = 'FAIL';
      }
    }
  } catch (error) {
    logColor(`Error running original API tests: ${error.message}`, 'red');
    console.error(error);
  }
}

/**
 * Test subcollection structure API
 */
async function testSubcollectionApi() {
  testBanner('Testing Subcollection Structure API');
  
  // If API URL is not available, skip tests
  if (!apiUrls.subcollection || apiUrls.subcollection === 'http://localhost:5001/your-project/us-central1/api_subcollections') {
    logColor('Subcollection API URL not configured. Skipping tests.', 'yellow');
    results.subcollection.skipped = 2; // Number of tests we would run
    return;
  }
  
  try {
    // Test health check
    try {
      const result = await testHealthCheck(apiUrls.subcollection);
      if (result.success) {
        logTestResult('Health Check (Subcollections)', true, result.message);
        results.subcollection.passed++;
        results.subcollection.tests['Health Check'] = 'PASS';
      } else {
        throw new Error(result.message);
      }
    } catch (error) {
      logTestResult('Health Check (Subcollections)', false, error.message);
      results.subcollection.failed++;
      results.subcollection.tests['Health Check'] = 'FAIL';
      // Skip other tests if health check fails
      logColor('Skipping remaining tests due to health check failure', 'yellow');
      return;
    }
    
    // Test update gist production status
    try {
      const result = await testUpdateGistProductionStatus(apiUrls.subcollection);
      if (result.success) {
        logTestResult('Update Gist Production Status (Subcollections)', true, result.message);
        results.subcollection.passed++;
        results.subcollection.tests['Update Gist Production Status'] = 'PASS';
      } else {
        throw new Error(result.message);
      }
    } catch (error) {
      // This may be expected if the gist doesn't exist
      if (error.message.includes('not found')) {
        logTestResult('Update Gist Production Status (Subcollections)', false, `Expected failure: ${error.message}`);
        results.subcollection.tests['Update Gist Production Status'] = 'FAIL (Expected)';
        results.subcollection.failed++;
      } else {
        logTestResult('Update Gist Production Status (Subcollections)', false, error.message);
        results.subcollection.failed++;
        results.subcollection.tests['Update Gist Production Status'] = 'FAIL';
      }
    }
  } catch (error) {
    logColor(`Error running subcollection API tests: ${error.message}`, 'red');
    console.error(error);
  }
}

/**
 * Test health check endpoint
 * @param {string} baseUrl Base URL for the API
 * @returns {Promise<Object>} Test result
 */
async function testHealthCheck(baseUrl) {
  logColor(`Testing health check endpoint at ${baseUrl}/...`, 'cyan');
  
  try {
    const response = await axios.get(`${baseUrl}/`);
    
    logColor('Health check response:', 'cyan');
    console.log(JSON.stringify(response.data, null, 2));
    
    if (response.status === 200) {
      return {
        success: true,
        message: `API is healthy: ${response.data.message || 'OK'}`
      };
    } else {
      return {
        success: false,
        message: `API health check failed with status ${response.status}`
      };
    }
  } catch (error) {
    return {
      success: false,
      message: `API health check request failed: ${error.message}`
    };
  }
}

/**
 * Test update gist production status endpoint
 * @param {string} baseUrl Base URL for the API
 * @returns {Promise<Object>} Test result
 */
async function testUpdateGistProductionStatus(baseUrl) {
  const userId = TEST_DATA.userId;
  const gistId = TEST_DATA.gistId;
  const url = `${baseUrl}/users/${userId}/gists/${gistId}/production-status`;
  
  logColor(`Testing update gist production status endpoint at ${url}...`, 'cyan');
  
  try {
    // Set production status to true
    const response = await axios.put(
      url,
      { inProduction: true },
      {
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': apiKey
        }
      }
    );
    
    logColor('Update gist production status response:', 'cyan');
    console.log(JSON.stringify(response.data, null, 2));
    
    if (response.status === 200) {
      // Now set it back to false
      const revertResponse = await axios.put(
        url,
        { inProduction: false },
        {
          headers: {
            'Content-Type': 'application/json',
            'x-api-key': apiKey
          }
        }
      );
      
      if (revertResponse.status === 200) {
        return {
          success: true,
          message: 'Successfully updated gist production status'
        };
      } else {
        return {
          success: false,
          message: `Failed to revert gist production status: ${revertResponse.status} ${revertResponse.data.error || ''}`
        };
      }
    } else {
      return {
        success: false,
        message: `Failed to update gist production status: ${response.status} ${response.data.error || ''}`
      };
    }
  } catch (error) {
    return {
      success: false,
      message: `API request failed: ${error.message}`
    };
  }
}

/**
 * Run all API tests
 */
async function runAllTests() {
  testBanner('RUNNING ALL API TESTS');
  
  try {
    // First test original API
    await testOriginalApi();
    
    // Then test subcollection API
    await testSubcollectionApi();
    
    // Print test results
    testBanner('API TEST RESULTS SUMMARY');
    
    logColor('\nOriginal Structure API Tests:', 'magenta');
    logColor(`Tests Passed: ${results.original.passed}`, 'green');
    logColor(`Tests Failed: ${results.original.failed}`, 'red');
    logColor(`Tests Skipped: ${results.original.skipped}`, 'yellow');
    
    logColor('\nSubcollection Structure API Tests:', 'magenta');
    logColor(`Tests Passed: ${results.subcollection.passed}`, 'green');
    logColor(`Tests Failed: ${results.subcollection.failed}`, 'red');
    logColor(`Tests Skipped: ${results.subcollection.skipped}`, 'yellow');
    
    const allPassed = 
      results.original.failed === 0 && 
      (results.subcollection.failed === 0 || results.subcollection.skipped > 0);
    
    if (allPassed) {
      logColor('\nALL API TESTS PASSED', 'green');
    } else {
      logColor('\nSOME API TESTS FAILED', 'red');
    }
    
    logColor('\nNote: Some tests might have expected failures if test data is not set up correctly.', 'yellow');
    logColor('Ensure the API servers are running and the test data is properly set up.', 'yellow');
    
  } catch (error) {
    logColor(`Error running API tests: ${error.message}`, 'red');
    console.error(error);
  } finally {
    // Ensure process exits
    process.exit(0);
  }
}

// Check if this script is being run directly
if (require.main === module) {
  runAllTests();
} else {
  // Export functions for use in other scripts
  module.exports = {
    testOriginalApi,
    testSubcollectionApi,
    runAllTests
  };
} 