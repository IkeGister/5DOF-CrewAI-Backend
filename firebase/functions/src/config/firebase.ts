import * as admin from 'firebase-admin';

// Initialize without service account
admin.initializeApp();

// Export Firestore for use in other files
export const db = admin.firestore();
