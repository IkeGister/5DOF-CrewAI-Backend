import * as admin from 'firebase-admin';

// Initialize Firebase Admin SDK without service account
// This uses Application Default Credentials (ADC)
admin.initializeApp();

// Export Firestore for use in other files
export const db = admin.firestore();

// Export specific collections for easier access
// Based on the actual Firestore structure, we only have a users collection
// gists and links are arrays within user documents, not separate collections
export const usersCollection = db.collection('users');

// Export Firebase Admin for use in other files
export default admin;
