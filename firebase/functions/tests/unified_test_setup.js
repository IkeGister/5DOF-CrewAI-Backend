/**
 * Unified Test Setup
 * 
 * This script sets up test data in both the original and subcollection structure.
 * It can be used to create test users, gists, and links for testing purposes.
 */

const { 
  initializeFirebase, 
  TEST_DATA, 
  logColor, 
  testBanner, 
  createTestGist, 
  createTestLink,
  userExists
} = require('./unified_test_utils');

// Initialize Firebase
const admin = initializeFirebase();
const db = admin.firestore();

/**
 * Create test data in original structure
 * @param {Object} options Options for creating test data
 * @returns {Promise<Object>} Created test data
 */
async function createOriginalStructureTestData(options = {}) {
  const userId = options.userId || TEST_DATA.userId;
  const gistId = options.gistId || TEST_DATA.gistId;
  const gistWithNoLinks = options.gistWithNoLinks || TEST_DATA.gistWithNoLinks;
  const linkId = options.linkId || TEST_DATA.linkId;

  testBanner('Setting up test data (original structure)');
  
  try {
    // Check if user already exists
    const userDoc = await db.collection('users').doc(userId).get();
    
    if (userDoc.exists) {
      logColor(`User ${userId} already exists, updating...`, 'yellow');
      
      // Create gists structure if it doesn't exist
      const gists = {};
      
      // Add test gist with link
      const gistWithLink = createTestGist(gistId);
      gists[gistId] = gistWithLink;
      
      // Add test gist without links
      const gistNoLinks = createTestGist(gistWithNoLinks, { hasLink: false });
      gists[gistWithNoLinks] = gistNoLinks;
      
      // Create links structure
      const links = {};
      links[linkId] = createTestLink(linkId, gistId);
      
      // Update user document
      await db.collection('users').doc(userId).update({
        gists,
        links
      });
      
      logColor(`Updated user ${userId} with test data`, 'green');
      return { userId, gists, links };
    } else {
      logColor(`Creating new user ${userId}...`, 'cyan');
      
      // Create gists structure
      const gists = {};
      
      // Add test gist with link
      const gistWithLink = createTestGist(gistId);
      gists[gistId] = gistWithLink;
      
      // Add test gist without links
      const gistNoLinks = createTestGist(gistWithNoLinks, { hasLink: false });
      gists[gistWithNoLinks] = gistNoLinks;
      
      // Create links structure
      const links = {};
      links[linkId] = createTestLink(linkId, gistId);
      
      // Create new user document
      await db.collection('users').doc(userId).set({
        userId,
        email: `${userId}@example.com`,
        displayName: 'Test User',
        gists,
        links
      });
      
      logColor(`Created new user ${userId} with test data`, 'green');
      return { userId, gists, links };
    }
  } catch (error) {
    logColor(`Error creating original structure test data: ${error.message}`, 'red');
    console.error(error);
    throw error;
  }
}

/**
 * Create test data in subcollection structure
 * @param {Object} options Options for creating test data
 * @returns {Promise<Object>} Created test data
 */
async function createSubcollectionStructureTestData(options = {}) {
  const userId = options.userId || TEST_DATA.userId;
  const gistId = options.gistId || TEST_DATA.gistId;
  const gistWithNoLinks = options.gistWithNoLinks || TEST_DATA.gistWithNoLinks;
  const linkId = options.linkId || TEST_DATA.linkId;

  testBanner('Setting up test data (subcollection structure)');
  
  try {
    // Check if user already exists
    const userDoc = await db.collection('users').doc(userId).get();
    
    if (!userDoc.exists) {
      logColor(`Creating new user ${userId}...`, 'cyan');
      
      // Create new user document
      await db.collection('users').doc(userId).set({
        userId,
        email: `${userId}@example.com`,
        displayName: 'Test User',
        created_at: admin.firestore.FieldValue.serverTimestamp(),
        updated_at: admin.firestore.FieldValue.serverTimestamp()
      });
      
      logColor(`Created new user ${userId}`, 'green');
    } else {
      logColor(`User ${userId} already exists`, 'yellow');
    }
    
    // Add test gist with link
    const gistWithLinkRef = db.collection('users').doc(userId).collection('gists').doc(gistId);
    const gistWithLinkDoc = await gistWithLinkRef.get();
    
    if (!gistWithLinkDoc.exists) {
      await gistWithLinkRef.set(createTestGist(gistId));
      logColor(`Created gist ${gistId} for user ${userId}`, 'green');
    } else {
      logColor(`Gist ${gistId} already exists for user ${userId}`, 'yellow');
    }
    
    // Add test gist without links
    const gistNoLinksRef = db.collection('users').doc(userId).collection('gists').doc(gistWithNoLinks);
    const gistNoLinksDoc = await gistNoLinksRef.get();
    
    if (!gistNoLinksDoc.exists) {
      await gistNoLinksRef.set(createTestGist(gistWithNoLinks, { hasLink: false }));
      logColor(`Created gist ${gistWithNoLinks} for user ${userId}`, 'green');
    } else {
      logColor(`Gist ${gistWithNoLinks} already exists for user ${userId}`, 'yellow');
    }
    
    // Add test link
    const linkRef = db.collection('users').doc(userId).collection('links').doc(linkId);
    const linkDoc = await linkRef.get();
    
    if (!linkDoc.exists) {
      await linkRef.set(createTestLink(linkId, gistId));
      logColor(`Created link ${linkId} for user ${userId}`, 'green');
    } else {
      logColor(`Link ${linkId} already exists for user ${userId}`, 'yellow');
    }
    
    return {
      userId,
      gists: {
        [gistId]: await gistWithLinkRef.get().then(doc => doc.data()),
        [gistWithNoLinks]: await gistNoLinksRef.get().then(doc => doc.data())
      },
      links: {
        [linkId]: await linkRef.get().then(doc => doc.data())
      }
    };
  } catch (error) {
    logColor(`Error creating subcollection structure test data: ${error.message}`, 'red');
    console.error(error);
    throw error;
  }
}

/**
 * Run both test data creation scripts
 */
async function createAllTestData() {
  try {
    await createOriginalStructureTestData();
    await createSubcollectionStructureTestData();
    logColor('Successfully created all test data for both structures', 'green');
  } catch (error) {
    logColor(`Error creating test data: ${error.message}`, 'red');
    console.error(error);
  } finally {
    // Ensure process exits
    process.exit(0);
  }
}

// Check if this script is being run directly
if (require.main === module) {
  createAllTestData();
} else {
  // Export functions for use in other scripts
  module.exports = {
    createOriginalStructureTestData,
    createSubcollectionStructureTestData,
    createAllTestData
  };
} 