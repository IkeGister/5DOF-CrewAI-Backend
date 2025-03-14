/**
 * Check Gist Status
 * 
 * This script checks the current status of a gist in the database.
 */

// Initialize Firebase Admin SDK
const admin = require('firebase-admin');

// Check if we already have an active app
try {
  admin.app();
  console.log('Using existing Firebase app');
} catch (error) {
  // Initialize with default credentials
  admin.initializeApp();
  console.log('Firebase Admin initialized with default credentials');
}

console.log('Firebase Admin initialized (REAL DATABASE CONNECTION ONLY)');
console.log(`Firebase Admin initialized with project ID: ${admin.app().options.projectId || 'default'}`);

// Firestore reference
const db = admin.firestore();

// Test data
const testUserId = 'crewAI-backend-tester';
const testGistId = 'gist_35e92f298ea2453489a14d0869509c10';

/**
 * Check gist status
 */
async function checkGistStatus() {
  console.log('🔍 CHECKING GIST STATUS');
  console.log('====================');
  
  try {
    // Get user document
    const userRef = db.collection('users').doc(testUserId);
    const userDoc = await userRef.get();
    
    if (!userDoc.exists) {
      console.log(`❌ User ${testUserId} does not exist`);
      process.exit(1);
    }
    
    const userData = userDoc.data();
    
    if (!userData.gists || !userData.gists[testGistId]) {
      console.log(`❌ Gist ${testGistId} not found for user ${testUserId}`);
      process.exit(1);
    }
    
    const gist = userData.gists[testGistId];
    
    console.log(`✅ Found gist ${gist.id}`);
    console.log('\nGist details:');
    console.log(`- Title: ${gist.title}`);
    console.log(`- Content: ${gist.content ? gist.content.substring(0, 50) + '...' : 'N/A'}`);
    console.log(`- Link: ${gist.link || 'N/A'}`);
    
    console.log('\nStatus:');
    console.log(`- inProduction: ${gist.status?.inProduction}`);
    console.log(`- production_status: ${gist.status?.production_status}`);
    
    console.log('\nTimestamps:');
    console.log(`- created_at: ${gist.created_at}`);
    console.log(`- updated_at: ${gist.updated_at}`);
    
    console.log('\nRaw status object:');
    console.log(JSON.stringify(gist.status, null, 2));
    
    process.exit(0);
  } catch (error) {
    console.error('Error checking gist status:', error);
    process.exit(1);
  }
}

// Run the function
checkGistStatus().catch(error => {
  console.error('Unhandled error:', error);
  process.exit(1);
}); 