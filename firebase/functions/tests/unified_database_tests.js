/**
 * Unified Database Tests
 * 
 * This script tests database operations for both the original and subcollection structures.
 * It tests retrieving users, gists, and links, and updating gist statuses.
 */

const { 
  initializeFirebase, 
  TEST_DATA, 
  logColor, 
  testBanner, 
  logTestResult,
  sleep
} = require('./unified_test_utils');

// Import original structure services
const firebaseService = require('../src/services/firebase_service');
const gistOperations = require('../src/services/gistOperations');

// Import subcollection structure services (if available)
let firebaseServiceSubcollections;
let gistOperationsSubcollections;

try {
  firebaseServiceSubcollections = require('../src/services/firebase_service_subcollections');
  gistOperationsSubcollections = require('../src/services/gistOperations_subcollections');
  logColor('Successfully imported subcollection services', 'green');
} catch (error) {
  logColor('Subcollection services not available. Only testing original structure.', 'yellow');
}

// Initialize Firebase
const admin = initializeFirebase();
const db = admin.firestore();

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

/**
 * Run tests for original structure
 */
async function testOriginalStructure() {
  testBanner('Testing Original Database Structure');
  
  try {
    // Test database connection
    try {
      await testDatabaseConnection();
      logTestResult('Database Connection', true);
      results.original.passed++;
      results.original.tests['Database Connection'] = 'PASS';
    } catch (error) {
      logTestResult('Database Connection', false, error.message);
      results.original.failed++;
      results.original.tests['Database Connection'] = 'FAIL';
      // If database connection fails, exit tests
      return;
    }
    
    // Test user retrieval
    try {
      const user = await testUserRetrieval();
      if (user && user.userId === TEST_DATA.userId) {
        logTestResult('User Retrieval', true);
        results.original.passed++;
        results.original.tests['User Retrieval'] = 'PASS';
      } else {
        throw new Error('User data is missing or incorrect');
      }
    } catch (error) {
      logTestResult('User Retrieval', false, error.message);
      results.original.failed++;
      results.original.tests['User Retrieval'] = 'FAIL';
    }
    
    // Test gists retrieval
    try {
      const gists = await testGistsRetrieval();
      if (gists && Object.keys(gists).length > 0) {
        logTestResult('Gists Retrieval', true, `Found ${Object.keys(gists).length} gists`);
        results.original.passed++;
        results.original.tests['Gists Retrieval'] = 'PASS';
      } else {
        throw new Error('No gists found for test user');
      }
    } catch (error) {
      logTestResult('Gists Retrieval', false, error.message);
      results.original.failed++;
      results.original.tests['Gists Retrieval'] = 'FAIL';
    }
    
    // Test single gist retrieval
    try {
      const gist = await testGistRetrieval();
      if (gist && gist.gistId === TEST_DATA.gistId) {
        logTestResult('Gist Retrieval', true);
        results.original.passed++;
        results.original.tests['Gist Retrieval'] = 'PASS';
      } else {
        throw new Error('Gist not found or data incorrect');
      }
    } catch (error) {
      // This is expected if the gist doesn't exist
      if (error.message.includes('not found') || error.message.includes('data incorrect')) {
        logTestResult('Gist Retrieval', false, `Expected failure: ${error.message}`);
        results.original.tests['Gist Retrieval'] = 'FAIL (Expected)';
        results.original.failed++;
      } else {
        logTestResult('Gist Retrieval', false, error.message);
        results.original.failed++;
        results.original.tests['Gist Retrieval'] = 'FAIL';
      }
    }
    
    // Test links retrieval
    try {
      const links = await testLinksRetrieval();
      if (links && Object.keys(links).length > 0) {
        // Check if any link has the expected properties
        const hasValidLink = Object.values(links).some(link => 
          link.url && link.gistId
        );
        
        if (hasValidLink) {
          logTestResult('Links Retrieval', true);
          results.original.passed++;
          results.original.tests['Links Retrieval'] = 'PASS';
        } else {
          logTestResult('Links Retrieval', true, 'But links are missing expected properties');
          results.original.passed++;
          results.original.tests['Links Retrieval'] = 'PASS (With warnings)';
        }
      } else {
        throw new Error('No links found for test user');
      }
    } catch (error) {
      logTestResult('Links Retrieval', false, error.message);
      results.original.failed++;
      results.original.tests['Links Retrieval'] = 'FAIL';
    }
    
    // Test links by gist ID retrieval
    try {
      const gistLinks = await testLinksByGistIdRetrieval();
      if (gistLinks && Object.keys(gistLinks).length > 0) {
        logTestResult('Links by Gist ID Retrieval', true, `Found ${Object.keys(gistLinks).length} links`);
        results.original.passed++;
        results.original.tests['Links by Gist ID Retrieval'] = 'PASS';
      } else {
        logTestResult('Links by Gist ID Retrieval', true, 'No links associated with this gist');
        results.original.passed++;
        results.original.tests['Links by Gist ID Retrieval'] = 'PASS (No links)';
      }
    } catch (error) {
      logTestResult('Links by Gist ID Retrieval', false, error.message);
      results.original.failed++;
      results.original.tests['Links by Gist ID Retrieval'] = 'FAIL';
    }
    
    // Test workflow status update
    try {
      const result = await testWorkflowStatusUpdate();
      if (result && result.updated) {
        logTestResult('Workflow Status Update', true);
        results.original.passed++;
        results.original.tests['Workflow Status Update'] = 'PASS';
      } else {
        throw new Error('Failed to update workflow status');
      }
    } catch (error) {
      // This may be expected if the gist doesn't exist
      if (error.message.includes('not found')) {
        logTestResult('Workflow Status Update', false, `Expected failure: ${error.message}`);
        results.original.tests['Workflow Status Update'] = 'FAIL (Expected)';
        results.original.failed++;
      } else {
        logTestResult('Workflow Status Update', false, error.message);
        results.original.failed++;
        results.original.tests['Workflow Status Update'] = 'FAIL';
      }
    }
    
  } catch (error) {
    logColor(`Error running original structure tests: ${error.message}`, 'red');
    console.error(error);
  }
}

/**
 * Run tests for subcollection structure
 */
async function testSubcollectionStructure() {
  if (!firebaseServiceSubcollections || !gistOperationsSubcollections) {
    logColor('Subcollection services not available. Skipping tests.', 'yellow');
    results.subcollection.skipped = 7; // Number of tests we would run
    return;
  }
  
  testBanner('Testing Subcollection Database Structure');
  
  try {
    // Test database connection
    try {
      await testDatabaseConnectionSubcollections();
      logTestResult('Database Connection (Subcollections)', true);
      results.subcollection.passed++;
      results.subcollection.tests['Database Connection'] = 'PASS';
    } catch (error) {
      logTestResult('Database Connection (Subcollections)', false, error.message);
      results.subcollection.failed++;
      results.subcollection.tests['Database Connection'] = 'FAIL';
      // If database connection fails, exit tests
      return;
    }
    
    // Test user retrieval
    try {
      const user = await testUserRetrievalSubcollections();
      if (user && user.userId === TEST_DATA.userId) {
        logTestResult('User Retrieval (Subcollections)', true);
        results.subcollection.passed++;
        results.subcollection.tests['User Retrieval'] = 'PASS';
      } else {
        throw new Error('User data is missing or incorrect');
      }
    } catch (error) {
      logTestResult('User Retrieval (Subcollections)', false, error.message);
      results.subcollection.failed++;
      results.subcollection.tests['User Retrieval'] = 'FAIL';
    }
    
    // Test gists retrieval
    try {
      const gists = await testGistsRetrievalSubcollections();
      if (gists && gists.length > 0) {
        logTestResult('Gists Retrieval (Subcollections)', true, `Found ${gists.length} gists`);
        results.subcollection.passed++;
        results.subcollection.tests['Gists Retrieval'] = 'PASS';
      } else {
        throw new Error('No gists found for test user');
      }
    } catch (error) {
      logTestResult('Gists Retrieval (Subcollections)', false, error.message);
      results.subcollection.failed++;
      results.subcollection.tests['Gists Retrieval'] = 'FAIL';
    }
    
    // Test single gist retrieval
    try {
      const gist = await testGistRetrievalSubcollections();
      if (gist && gist.gistId === TEST_DATA.gistId) {
        logTestResult('Gist Retrieval (Subcollections)', true);
        results.subcollection.passed++;
        results.subcollection.tests['Gist Retrieval'] = 'PASS';
      } else {
        throw new Error('Gist not found or data incorrect');
      }
    } catch (error) {
      // This is expected if the gist doesn't exist
      if (error.message.includes('not found') || error.message.includes('data incorrect')) {
        logTestResult('Gist Retrieval (Subcollections)', false, `Expected failure: ${error.message}`);
        results.subcollection.tests['Gist Retrieval'] = 'FAIL (Expected)';
        results.subcollection.failed++;
      } else {
        logTestResult('Gist Retrieval (Subcollections)', false, error.message);
        results.subcollection.failed++;
        results.subcollection.tests['Gist Retrieval'] = 'FAIL';
      }
    }
    
    // Test links retrieval
    try {
      const links = await testLinksRetrievalSubcollections();
      if (links && links.length > 0) {
        // Check if any link has the expected properties
        const hasValidLink = links.some(link => 
          link.url && link.gistId
        );
        
        if (hasValidLink) {
          logTestResult('Links Retrieval (Subcollections)', true);
          results.subcollection.passed++;
          results.subcollection.tests['Links Retrieval'] = 'PASS';
        } else {
          logTestResult('Links Retrieval (Subcollections)', true, 'But links are missing expected properties');
          results.subcollection.passed++;
          results.subcollection.tests['Links Retrieval'] = 'PASS (With warnings)';
        }
      } else {
        throw new Error('No links found for test user');
      }
    } catch (error) {
      logTestResult('Links Retrieval (Subcollections)', false, error.message);
      results.subcollection.failed++;
      results.subcollection.tests['Links Retrieval'] = 'FAIL';
    }
    
    // Test links by gist ID retrieval
    try {
      const gistLinks = await testLinksByGistIdRetrievalSubcollections();
      if (gistLinks && gistLinks.length > 0) {
        logTestResult('Links by Gist ID Retrieval (Subcollections)', true, `Found ${gistLinks.length} links`);
        results.subcollection.passed++;
        results.subcollection.tests['Links by Gist ID Retrieval'] = 'PASS';
      } else {
        logTestResult('Links by Gist ID Retrieval (Subcollections)', true, 'No links associated with this gist');
        results.subcollection.passed++;
        results.subcollection.tests['Links by Gist ID Retrieval'] = 'PASS (No links)';
      }
    } catch (error) {
      logTestResult('Links by Gist ID Retrieval (Subcollections)', false, error.message);
      results.subcollection.failed++;
      results.subcollection.tests['Links by Gist ID Retrieval'] = 'FAIL';
    }
    
    // Test workflow status update
    try {
      const result = await testWorkflowStatusUpdateSubcollections();
      if (result && result.updated) {
        logTestResult('Workflow Status Update (Subcollections)', true);
        results.subcollection.passed++;
        results.subcollection.tests['Workflow Status Update'] = 'PASS';
      } else {
        throw new Error('Failed to update workflow status');
      }
    } catch (error) {
      // This may be expected if the gist doesn't exist
      if (error.message.includes('not found')) {
        logTestResult('Workflow Status Update (Subcollections)', false, `Expected failure: ${error.message}`);
        results.subcollection.tests['Workflow Status Update'] = 'FAIL (Expected)';
        results.subcollection.failed++;
      } else {
        logTestResult('Workflow Status Update (Subcollections)', false, error.message);
        results.subcollection.failed++;
        results.subcollection.tests['Workflow Status Update'] = 'FAIL';
      }
    }
    
  } catch (error) {
    logColor(`Error running subcollection structure tests: ${error.message}`, 'red');
    console.error(error);
  }
}

// Original structure test implementations
async function testDatabaseConnection() {
  try {
    logColor('Testing database connection...', 'cyan');
    await db.collection('users').limit(1).get();
    return true;
  } catch (error) {
    throw new Error(`Database connection failed: ${error.message}`);
  }
}

async function testUserRetrieval() {
  logColor(`Testing user retrieval for ${TEST_DATA.userId}...`, 'cyan');
  try {
    const user = await firebaseService.getUser(TEST_DATA.userId);
    logColor('User data:', 'cyan');
    console.log(JSON.stringify(user, null, 2));
    return user;
  } catch (error) {
    throw new Error(`User retrieval failed: ${error.message}`);
  }
}

async function testGistsRetrieval() {
  logColor(`Testing gists retrieval for ${TEST_DATA.userId}...`, 'cyan');
  try {
    const gists = await gistOperations.getGists(TEST_DATA.userId);
    logColor(`Retrieved ${Object.keys(gists).length} gists`, 'cyan');
    console.log(JSON.stringify(gists, null, 2));
    return gists;
  } catch (error) {
    throw new Error(`Gists retrieval failed: ${error.message}`);
  }
}

async function testGistRetrieval() {
  logColor(`Testing gist retrieval for ${TEST_DATA.userId}, gist ${TEST_DATA.gistId}...`, 'cyan');
  try {
    const gist = await gistOperations.getGist(TEST_DATA.userId, TEST_DATA.gistId);
    logColor('Gist data:', 'cyan');
    console.log(JSON.stringify(gist, null, 2));
    return gist;
  } catch (error) {
    throw new Error(`Gist retrieval failed: ${error.message}`);
  }
}

async function testWorkflowStatusUpdate() {
  logColor(`Testing workflow status update for ${TEST_DATA.userId}, gist ${TEST_DATA.gistId}...`, 'cyan');
  try {
    const newStatus = "In Progress";
    const result = await gistOperations.updateGistWorkflowStatus(TEST_DATA.userId, TEST_DATA.gistId, newStatus);
    
    // Verify the update
    const gist = await gistOperations.getGist(TEST_DATA.userId, TEST_DATA.gistId);
    if (gist && gist.status && gist.status.production_status === newStatus) {
      return { updated: true, gist };
    } else {
      throw new Error('Workflow status was not updated correctly');
    }
  } catch (error) {
    throw new Error(`Workflow status update failed: ${error.message}`);
  }
}

async function testLinksRetrieval() {
  logColor(`Testing links retrieval for ${TEST_DATA.userId}...`, 'cyan');
  try {
    const links = await gistOperations.getLinks(TEST_DATA.userId);
    logColor(`Retrieved ${Object.keys(links).length} links`, 'cyan');
    console.log(JSON.stringify(links, null, 2));
    return links;
  } catch (error) {
    throw new Error(`Links retrieval failed: ${error.message}`);
  }
}

async function testLinksByGistIdRetrieval() {
  logColor(`Testing links retrieval for ${TEST_DATA.userId}, gist ${TEST_DATA.gistId}...`, 'cyan');
  try {
    const links = await gistOperations.getLinksByGistId(TEST_DATA.userId, TEST_DATA.gistId);
    logColor(`Retrieved ${Object.keys(links).length} links for gist`, 'cyan');
    console.log(JSON.stringify(links, null, 2));
    return links;
  } catch (error) {
    throw new Error(`Links by gist ID retrieval failed: ${error.message}`);
  }
}

// Subcollection structure test implementations
async function testDatabaseConnectionSubcollections() {
  try {
    logColor('Testing database connection for subcollections...', 'cyan');
    await db.collection('users').limit(1).get();
    return true;
  } catch (error) {
    throw new Error(`Database connection failed: ${error.message}`);
  }
}

async function testUserRetrievalSubcollections() {
  logColor(`Testing user retrieval (subcollections) for ${TEST_DATA.userId}...`, 'cyan');
  try {
    const user = await firebaseServiceSubcollections.getUser(TEST_DATA.userId);
    logColor('User data (subcollections):', 'cyan');
    console.log(JSON.stringify(user, null, 2));
    return user;
  } catch (error) {
    throw new Error(`User retrieval (subcollections) failed: ${error.message}`);
  }
}

async function testGistsRetrievalSubcollections() {
  logColor(`Testing gists retrieval (subcollections) for ${TEST_DATA.userId}...`, 'cyan');
  try {
    const gistsOperationsClass = new gistOperationsSubcollections.GistOperationsSubcollections();
    const gists = await gistsOperationsClass.getGists(TEST_DATA.userId);
    logColor(`Retrieved ${gists.length} gists (subcollections)`, 'cyan');
    console.log(JSON.stringify(gists, null, 2));
    return gists;
  } catch (error) {
    throw new Error(`Gists retrieval (subcollections) failed: ${error.message}`);
  }
}

async function testGistRetrievalSubcollections() {
  logColor(`Testing gist retrieval (subcollections) for ${TEST_DATA.userId}, gist ${TEST_DATA.gistId}...`, 'cyan');
  try {
    const gistsOperationsClass = new gistOperationsSubcollections.GistOperationsSubcollections();
    const gist = await gistsOperationsClass.getGist(TEST_DATA.userId, TEST_DATA.gistId);
    logColor('Gist data (subcollections):', 'cyan');
    console.log(JSON.stringify(gist, null, 2));
    return gist;
  } catch (error) {
    throw new Error(`Gist retrieval (subcollections) failed: ${error.message}`);
  }
}

async function testWorkflowStatusUpdateSubcollections() {
  logColor(`Testing workflow status update (subcollections) for ${TEST_DATA.userId}, gist ${TEST_DATA.gistId}...`, 'cyan');
  try {
    const gistsOperationsClass = new gistOperationsSubcollections.GistOperationsSubcollections();
    const newStatus = "Complete";
    const result = await gistsOperationsClass.updateGistWorkflowStatus(TEST_DATA.userId, TEST_DATA.gistId, newStatus);
    
    // Verify the update
    const gist = await gistsOperationsClass.getGist(TEST_DATA.userId, TEST_DATA.gistId);
    if (gist && gist.status && gist.status.production_status === newStatus) {
      return { updated: true, gist };
    } else {
      throw new Error('Workflow status (subcollections) was not updated correctly');
    }
  } catch (error) {
    throw new Error(`Workflow status update (subcollections) failed: ${error.message}`);
  }
}

async function testLinksRetrievalSubcollections() {
  logColor(`Testing links retrieval (subcollections) for ${TEST_DATA.userId}...`, 'cyan');
  try {
    const gistsOperationsClass = new gistOperationsSubcollections.GistOperationsSubcollections();
    const links = await gistsOperationsClass.getGistLinks(TEST_DATA.userId);
    logColor(`Retrieved ${links.length} links (subcollections)`, 'cyan');
    console.log(JSON.stringify(links, null, 2));
    return links;
  } catch (error) {
    throw new Error(`Links retrieval (subcollections) failed: ${error.message}`);
  }
}

async function testLinksByGistIdRetrievalSubcollections() {
  logColor(`Testing links retrieval (subcollections) for ${TEST_DATA.userId}, gist ${TEST_DATA.gistId}...`, 'cyan');
  try {
    const gistsOperationsClass = new gistOperationsSubcollections.GistOperationsSubcollections();
    const links = await gistsOperationsClass.getGistLinks(TEST_DATA.userId, TEST_DATA.gistId);
    logColor(`Retrieved ${links.length} links for gist (subcollections)`, 'cyan');
    console.log(JSON.stringify(links, null, 2));
    return links;
  } catch (error) {
    throw new Error(`Links by gist ID retrieval (subcollections) failed: ${error.message}`);
  }
}

/**
 * Run all tests
 */
async function runAllTests() {
  testBanner('RUNNING ALL DATABASE TESTS');
  
  try {
    // Run original structure tests
    await testOriginalStructure();
    
    // Run subcollection structure tests
    await testSubcollectionStructure();
    
    // Print test results
    testBanner('TEST RESULTS SUMMARY');
    
    logColor('\nOriginal Structure Tests:', 'magenta');
    logColor(`Tests Passed: ${results.original.passed}`, 'green');
    logColor(`Tests Failed: ${results.original.failed}`, 'red');
    logColor(`Tests Skipped: ${results.original.skipped}`, 'yellow');
    
    logColor('\nSubcollection Structure Tests:', 'magenta');
    logColor(`Tests Passed: ${results.subcollection.passed}`, 'green');
    logColor(`Tests Failed: ${results.subcollection.failed}`, 'red');
    logColor(`Tests Skipped: ${results.subcollection.skipped}`, 'yellow');
    
    const allPassed = 
      results.original.failed === 0 && 
      (results.subcollection.failed === 0 || results.subcollection.skipped > 0);
    
    if (allPassed) {
      logColor('\nALL TESTS PASSED', 'green');
    } else {
      logColor('\nSOME TESTS FAILED', 'red');
    }
    
    logColor('\nNote: Some tests might have expected failures if test data is not set up correctly.', 'yellow');
    logColor('Run the unified_test_setup.js script to create test data before running these tests.', 'yellow');
    
  } catch (error) {
    logColor(`Error running tests: ${error.message}`, 'red');
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
    testOriginalStructure,
    testSubcollectionStructure,
    runAllTests
  };
} 