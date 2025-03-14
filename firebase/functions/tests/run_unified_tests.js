/**
 * Unified Test Runner
 * 
 * This script runs all the unified tests in sequence:
 * 1. Sets up test data in both structures
 * 2. Runs database tests for both structures
 * 3. Runs API tests for both structures
 */

const { 
  initializeFirebase,
  logColor, 
  testBanner
} = require('./unified_test_utils');

// Import test setup and test modules
const { createAllTestData } = require('./unified_test_setup');
const { runAllTests: runAllDatabaseTests } = require('./unified_database_tests');
const { runAllTests: runAllApiTests } = require('./unified_api_tests');

// Initialize Firebase
initializeFirebase();

/**
 * Run all tests in sequence
 */
async function runAllTests() {
  testBanner('UNIFIED TEST SUITE');
  
  try {
    // Step 1: Set up test data
    logColor('\nSTEP 1: Setting up test data...', 'blue');
    try {
      await createAllTestData();
      logColor('Test data setup completed successfully.', 'green');
    } catch (error) {
      logColor(`Error setting up test data: ${error.message}`, 'red');
      console.error(error);
      // Continue with tests even if data setup fails
      logColor('Continuing with tests even though data setup failed.', 'yellow');
    }
    
    // Step 2: Run database tests
    logColor('\nSTEP 2: Running database tests...', 'blue');
    try {
      // We need to require this again because the previous module might have called process.exit()
      const databaseTests = require('./unified_database_tests');
      await databaseTests.runAllTests();
      logColor('Database tests completed.', 'green');
    } catch (error) {
      logColor(`Error running database tests: ${error.message}`, 'red');
      console.error(error);
    }
    
    // Step 3: Run API tests
    logColor('\nSTEP 3: Running API tests...', 'blue');
    try {
      // We need to require this again because the previous module might have called process.exit()
      const apiTests = require('./unified_api_tests');
      await apiTests.runAllTests();
      logColor('API tests completed.', 'green');
    } catch (error) {
      logColor(`Error running API tests: ${error.message}`, 'red');
      console.error(error);
    }
    
    testBanner('ALL TESTS COMPLETED');
    
    logColor('\nNote: Check individual test results above for details.', 'yellow');
    logColor('Some tests might have expected failures if the test environment is not fully set up.', 'yellow');
    
  } catch (error) {
    logColor(`Error running unified test suite: ${error.message}`, 'red');
    console.error(error);
  }
}

/**
 * Run a specific test module
 * @param {string} testModule Name of the test module to run
 */
async function runSpecificTest(testModule) {
  switch (testModule) {
    case 'setup':
      testBanner('RUNNING TEST DATA SETUP');
      await createAllTestData();
      break;
    case 'database':
      testBanner('RUNNING DATABASE TESTS');
      await runAllDatabaseTests();
      break;
    case 'api':
      testBanner('RUNNING API TESTS');
      await runAllApiTests();
      break;
    default:
      logColor(`Unknown test module: ${testModule}`, 'red');
      logColor('Available modules: setup, database, api', 'yellow');
      process.exit(1);
  }
}

// Check if this script is being run directly
if (require.main === module) {
  // Check if a specific test module was requested
  const testModule = process.argv[2];
  
  if (testModule) {
    runSpecificTest(testModule);
  } else {
    runAllTests();
  }
}

module.exports = {
  runAllTests,
  runSpecificTest
}; 