/**
 * Unified Test Utilities
 * 
 * This module provides shared utilities for testing both original and subcollection
 * database structures in the CrewAI Backend.
 */

const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  white: '\x1b[37m'
};

/**
 * Initialize Firebase Admin
 * @param {Object} options Configuration options
 * @returns {Object} Firebase admin app instance
 */
function initializeFirebase(options = {}) {
  try {
    // Check if Firebase is already initialized
    return admin.app();
  } catch (error) {
    // Initialize with default credentials or service account if provided
    const serviceAccountPath = options.serviceAccountPath || '../lib/config/serviceAccount.json';
    
    try {
      if (fs.existsSync(serviceAccountPath)) {
        const serviceAccount = require(serviceAccountPath);
        const app = admin.initializeApp({
          credential: admin.credential.cert(serviceAccount)
        });
        console.log('Firebase Admin initialized with service account');
        return app;
      } else {
        console.log('No service account key found, using default credentials');
        const app = admin.initializeApp();
        console.log('Firebase Admin initialized with default credentials');
        return app;
      }
    } catch (initError) {
      console.error('Error initializing Firebase:', initError);
      throw initError;
    }
  }
}

/**
 * Constants for test data
 */
const TEST_DATA = {
  userId: 'crewAI-backend-tester',
  gistId: 'gist_35e92f298ea2453489a14d0869509c10',
  gistWithNoLinks: 'gist_with_no_links',
  linkId: 'link_primary',
  apiKey: process.env.API_KEY || 'your-test-api-key',
  baseUrl: process.env.API_BASE_URL || 'http://localhost:5001/your-project/us-central1/api'
};

/**
 * Log with color
 * @param {string} message Message to log
 * @param {string} color Color from colors object
 */
function logColor(message, color = 'white') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

/**
 * Create a test banner
 * @param {string} title Test title
 * @param {string} color Color for the banner
 */
function testBanner(title, color = 'blue') {
  const line = '='.repeat(title.length + 4);
  logColor(`\n${line}`, color);
  logColor(`  ${title}  `, color);
  logColor(`${line}`, color);
}

/**
 * Log a test result
 * @param {string} testName Name of the test
 * @param {boolean} success Whether the test succeeded
 * @param {string} message Optional message
 */
function logTestResult(testName, success, message = '') {
  const status = success ? `${colors.green}✅ PASS${colors.reset}` : `${colors.red}❌ FAIL${colors.reset}`;
  console.log(`${testName}: ${status} ${message ? `- ${message}` : ''}`);
}

/**
 * Check if a user exists
 * @param {string} userId User ID to check
 * @param {Object} db Firestore instance
 * @returns {Promise<boolean>} Whether the user exists
 */
async function userExists(userId, db) {
  const userDoc = await db.collection('users').doc(userId).get();
  return userDoc.exists;
}

/**
 * Create a standard test gist object
 * @param {string} gistId Gist ID
 * @param {Object} options Additional options
 * @returns {Object} Gist object
 */
function createTestGist(gistId, options = {}) {
  const hasLink = options.hasLink !== false;
  
  return {
    id: gistId,
    gistId: gistId,
    title: options.title || (hasLink ? "Test Gist with Link" : "Test Gist without Links"),
    content: options.content || `This is a test gist ${hasLink ? 'with' : 'without'} a link for testing the API.`,
    link: hasLink ? (options.link || "https://example.com/test-link") : undefined,
    status: {
      inProduction: options.inProduction || false,
      production_status: options.production_status || "Not Started"
    },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };
}

/**
 * Create a standard test link object
 * @param {string} linkId Link ID
 * @param {string} gistId Associated gist ID
 * @param {Object} options Additional options
 * @returns {Object} Link object
 */
function createTestLink(linkId, gistId, options = {}) {
  return {
    id: linkId,
    gistId: gistId,
    url: options.url || "https://example.com/test-link",
    title: options.title || "Test Link",
    description: options.description || "This is a test link for testing the API",
    date_added: admin.firestore.FieldValue.serverTimestamp()
  };
}

/**
 * Check if a file exists
 * @param {string} filePath Path to check
 * @returns {boolean} Whether the file exists
 */
function fileExists(filePath) {
  try {
    return fs.existsSync(filePath);
  } catch (err) {
    return false;
  }
}

/**
 * Sleep for a specified number of milliseconds
 * @param {number} ms Milliseconds to sleep
 * @returns {Promise<void>} Promise that resolves after sleeping
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

module.exports = {
  initializeFirebase,
  TEST_DATA,
  colors,
  logColor,
  testBanner,
  logTestResult,
  userExists,
  createTestGist,
  createTestLink,
  fileExists,
  sleep
}; 