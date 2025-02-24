import * as admin from 'firebase-admin';
import * as serviceAccount from './serviceAccount.json';

// Initialize Firebase Admin
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount as admin.ServiceAccount)
});

// Export Firestore for use in other files
export const db = admin.firestore();
export default admin;
