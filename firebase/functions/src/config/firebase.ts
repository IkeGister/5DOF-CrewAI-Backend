import * as admin from 'firebase-admin';

// Force REAL DATABASE connection only - no mocks
console.log('Firebase Admin initialized (REAL DATABASE CONNECTION ONLY)');

// Initialize Firebase Admin if not already initialized
if (!admin.apps.length) {
  try {
    // Initialize using Application Default Credentials
    admin.initializeApp();
    
    console.log(`Firebase Admin initialized with project ID: ${admin.app().options.projectId || 'default'}`);
  } catch (error) {
    console.error('Failed to initialize Firebase Admin:', error);
    throw error;
  }
}

// Export Firestore for use in other files
export const db = admin.firestore();

// Export specific collections for easier access
// Based on the actual Firestore structure, we only have a users collection
// gists and links are arrays within user documents, not separate collections
export const usersCollection = db.collection('users');

// Export Firebase Admin for use in other files
export default admin;
