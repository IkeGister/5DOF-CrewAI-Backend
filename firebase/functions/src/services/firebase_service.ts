import * as admin from 'firebase-admin';
import { db, usersCollection } from '../config/firebase';

/**
 * Interfaces for Firestore documents
 */
interface Gist {
  id?: string;
  gistId?: string;
  title: string;
  content: string;
  is_played: boolean;
  status: string;
  // Other gist properties as needed
}

interface Link {
  id: string;
  url: string;
  title: string;
  description: string;
  date_added: admin.firestore.Timestamp;
  gistId?: string;
  // Other link properties as needed
}

interface User {
  id: string;
  username: string;
  email: string;
  gists?: Gist[];
  links?: Link[];
}

/**
 * User Operations
 */

/**
 * Get a user by ID
 */
export async function getUser(userId: string): Promise<User | null> {
  const doc = await usersCollection.doc(userId).get();
  if (!doc.exists) return null;
  return { id: doc.id, ...doc.data() } as User;
}

/**
 * Gist Operations
 */

/**
 * Get a single gist by ID for a specific user
 */
export async function getGist(userId: string, gistId: string): Promise<Gist | null> {
  const userDoc = await usersCollection.doc(userId).get();
  if (!userDoc.exists) return null;
  
  const userData = userDoc.data() as User;
  const gists = userData.gists || [];
  
  // Check for both 'id' and 'gistId' properties
  const gist = gists.find(g => g.id === gistId || g.gistId === gistId);
  return gist || null;
}

/**
 * Get all gists for a user
 */
export async function getUserGists(userId: string): Promise<Gist[]> {
  const userDoc = await usersCollection.doc(userId).get();
  if (!userDoc.exists) return [];
  
  const userData = userDoc.data() as User;
  return userData.gists || [];
}

/**
 * Update a gist's production status
 */
export async function updateGistStatus(
  userId: string,
  gistId: string, 
  inProduction: boolean, 
  status: 'draft' | 'review' | 'published'
): Promise<void> {
  // Get the user document
  const userRef = usersCollection.doc(userId);
  const userDoc = await userRef.get();
  
  if (!userDoc.exists) {
    throw new Error('User not found');
  }
  
  const userData = userDoc.data() as User;
  const gists = userData.gists || [];
  
  // Find the gist index
  const gistIndex = gists.findIndex(g => g.id === gistId);
  
  if (gistIndex === -1) {
    throw new Error('Gist not found');
  }
  
  // Update the gist in the array
  await userRef.update({
    [`gists.${gistIndex}.inProduction`]: inProduction,
    [`gists.${gistIndex}.production_status`]: status,
    [`gists.${gistIndex}.updatedAt`]: admin.firestore.FieldValue.serverTimestamp()
  });
}

/**
 * Link Operations
 */

/**
 * Get a single link by ID for a specific user
 */
export async function getLink(userId: string, linkId: string): Promise<Link | null> {
  const userDoc = await usersCollection.doc(userId).get();
  if (!userDoc.exists) return null;
  
  const userData = userDoc.data() as User;
  const links = userData.links || [];
  
  const link = links.find(l => l.id === linkId);
  return link || null;
}

/**
 * Get all links for a user
 */
export async function getUserLinks(userId: string): Promise<Link[]> {
  const userDoc = await usersCollection.doc(userId).get();
  if (!userDoc.exists) return [];
  
  const userData = userDoc.data() as User;
  return userData.links || [];
}

/**
 * Get all links related to a gist for a user
 */
export async function getLinksByGistId(userId: string, gistId: string): Promise<Link[]> {
  const userDoc = await usersCollection.doc(userId).get();
  if (!userDoc.exists) return [];
  
  const userData = userDoc.data() as User;
  const links = userData.links || [];
  
  return links.filter(link => link.gistId === gistId);
}

/**
 * Update a link's production status
 */
export async function updateLinkStatus(
  userId: string,
  linkId: string, 
  inProduction: boolean, 
  status: 'draft' | 'review' | 'published'
): Promise<void> {
  // Get the user document
  const userRef = usersCollection.doc(userId);
  const userDoc = await userRef.get();
  
  if (!userDoc.exists) {
    throw new Error('User not found');
  }
  
  const userData = userDoc.data() as User;
  const links = userData.links || [];
  
  // Find the link index
  const linkIndex = links.findIndex(l => l.id === linkId);
  
  if (linkIndex === -1) {
    throw new Error('Link not found');
  }
  
  // Update the link in the array
  await userRef.update({
    [`links.${linkIndex}.inProduction`]: inProduction,
    [`links.${linkIndex}.production_status`]: status,
    [`links.${linkIndex}.updatedAt`]: admin.firestore.FieldValue.serverTimestamp()
  });
}

/**
 * Batch Operations
 */

/**
 * Batch update multiple gists for a user
 */
export async function batchUpdateGists(
  userId: string,
  gistIds: string[],
  inProduction: boolean,
  status: 'draft' | 'review' | 'published'
): Promise<void> {
  // Get the user document
  const userRef = usersCollection.doc(userId);
  const userDoc = await userRef.get();
  
  if (!userDoc.exists) {
    throw new Error('User not found');
  }
  
  const userData = userDoc.data() as User;
  const gists = userData.gists || [];
  
  // Create a batch
  const batch = db.batch();
  
  // For each gist ID, find its index and update it
  gistIds.forEach(gistId => {
    const gistIndex = gists.findIndex(g => g.id === gistId);
    
    if (gistIndex !== -1) {
      batch.update(userRef, {
        [`gists.${gistIndex}.inProduction`]: inProduction,
        [`gists.${gistIndex}.production_status`]: status,
        [`gists.${gistIndex}.updatedAt`]: admin.firestore.FieldValue.serverTimestamp()
      });
    }
  });
  
  // Commit the batch
  await batch.commit();
}

/**
 * Update a gist and all its related links for a user
 */
export async function updateGistAndLinks(
  userId: string,
  gistId: string,
  inProduction: boolean,
  status: 'draft' | 'review' | 'published'
): Promise<void> {
  await db.runTransaction(async (transaction) => {
    // Get the user document
    const userRef = usersCollection.doc(userId);
    const userDoc = await transaction.get(userRef);
    
    if (!userDoc.exists) {
      throw new Error('User not found');
    }
    
    const userData = userDoc.data() as User;
    const gists = userData.gists || [];
    const links = userData.links || [];
    
    // Find the gist index
    const gistIndex = gists.findIndex(g => g.id === gistId);
    
    if (gistIndex === -1) {
      throw new Error('Gist not found');
    }
    
    // Update the gist
    transaction.update(userRef, {
      [`gists.${gistIndex}.inProduction`]: inProduction,
      [`gists.${gistIndex}.production_status`]: status,
      [`gists.${gistIndex}.updatedAt`]: admin.firestore.FieldValue.serverTimestamp()
    });
    
    // Find and update all related links
    links.forEach((link, linkIndex) => {
      if (link.gistId === gistId) {
        transaction.update(userRef, {
          [`links.${linkIndex}.inProduction`]: inProduction,
          [`links.${linkIndex}.production_status`]: status,
          [`links.${linkIndex}.updatedAt`]: admin.firestore.FieldValue.serverTimestamp()
        });
      }
    });
  });
}

/**
 * Firebase Connection Test
 * 
 * Utility function to test Firebase connection
 */
export async function testFirebaseConnection(): Promise<{
  success: boolean;
  projectId?: string;
  error?: string;
}> {
  try {
    // Get the Firebase app
    const app = admin.app();
    
    // Get the project ID
    const projectId = app.options.projectId;
    
    // Try to write to Firestore to verify connection
    const testDocRef = db.collection('_test_connection').doc('test_doc');
    const timestamp = admin.firestore.Timestamp.now();
    
    await testDocRef.set({
      timestamp,
      message: 'Test connection successful',
      testRun: new Date().toISOString()
    });
    
    // Clean up the test document
    await testDocRef.delete();
    
    return {
      success: true,
      projectId: projectId || 'Using Application Default Credentials'
    };
  } catch (error: any) {
    return {
      success: false,
      error: error.message
    };
  }
} 