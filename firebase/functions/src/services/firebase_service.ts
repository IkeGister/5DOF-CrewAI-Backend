import * as admin from 'firebase-admin';
import { db, usersCollection } from '../config/firebase';
import * as mockService from './mock/firebase_service_mock';

// Use mock implementations in development mode
const isDevelopment = process.env.NODE_ENV === 'development';

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

// Mock data for testing
const mockGists: Record<string, Record<string, any>> = {
  'test_user_1741057003': {
    'gist_1741057003': {
      id: 'gist_1741057003',
      title: 'Test Gist',
      content: 'This is a test gist',
      production_status: 'draft',
      inProduction: false,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
  }
};

const mockLinks: Record<string, string[]> = {
  'test_user_1741057003': ['link1', 'link2']
};

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
 * Get all gists for a user
 */
export async function getUserGists(userId: string): Promise<Gist[]> {
  const userDoc = await usersCollection.doc(userId).get();
  if (!userDoc.exists) return [];
  
  const userData = userDoc.data() as User;
  return userData.gists || [];
}

/**
 * Get a single gist by ID for a specific user
 */
export async function getGist(userId: string, gistId: string): Promise<any> {
  if (isDevelopment) {
    console.log(`[MOCK] Getting gist: ${gistId} for user: ${userId}`);
    const userGists = mockGists[userId];
    if (!userGists || !userGists[gistId]) return null;
    return userGists[gistId];
  }
  
  // Original implementation for production
  try {
    const db = admin.firestore();
    const gistRef = db.collection('users').doc(userId).collection('gists').doc(gistId);
    const doc = await gistRef.get();
    
    if (!doc.exists) {
      return null;
    }
    
    return {
      id: doc.id,
      ...doc.data()
    };
  } catch (error) {
    console.error(`Error getting gist ${gistId} for user ${userId}:`, error);
    throw error;
  }
}

/**
 * Update a gist's production status
 */
export async function updateGistStatus(
  userId: string,
  gistId: string, 
  inProduction: boolean, 
  status: 'draft' | 'review' | 'published'
): Promise<any> {
  if (isDevelopment) {
    console.log(`[MOCK] Updating gist status: ${gistId} for user: ${userId}`);
    console.log(`[MOCK] inProduction: ${inProduction}, production_status: ${status}`);
    
    if (!mockGists[userId]) mockGists[userId] = {};
    if (!mockGists[userId][gistId]) {
      mockGists[userId][gistId] = {
        id: gistId,
        title: 'New Test Gist',
        content: 'This is a new test gist',
        production_status: 'draft',
        inProduction: false,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };
    }
    
    mockGists[userId][gistId].inProduction = inProduction;
    mockGists[userId][gistId].production_status = status;
    mockGists[userId][gistId].updatedAt = new Date().toISOString();
    
    return mockGists[userId][gistId];
  }
  
  // Original implementation for production
  try {
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
    
    // Return updated gist
    const updatedUserDoc = await userRef.get();
    const updatedUserData = updatedUserDoc.data() as User;
    return updatedUserData.gists?.[gistIndex] || null;
  } catch (error) {
    console.error(`Error updating gist ${gistId} for user ${userId}:`, error);
    throw error;
  }
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
  
  const link = links.find(link => link.id === linkId);
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
 * Update a gist and all its related links for a user
 */
export async function updateGistAndLinks(
  userId: string,
  gistId: string,
  links: string[] = [],
  inProduction: boolean,
  status: 'draft' | 'review' | 'published'
): Promise<any> {
  if (isDevelopment) {
    console.log(`[MOCK] Updating gist and links: ${gistId} for user: ${userId}`);
    console.log(`[MOCK] links: ${links.join(', ')}`);
    console.log(`[MOCK] inProduction: ${inProduction}, production_status: ${status}`);
    
    // Update gist
    if (!mockGists[userId]) mockGists[userId] = {};
    if (!mockGists[userId][gistId]) {
      mockGists[userId][gistId] = {
        id: gistId,
        title: 'New Test Gist',
        content: 'This is a new test gist',
        production_status: 'draft',
        inProduction: false,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };
    }
    
    mockGists[userId][gistId].inProduction = inProduction;
    mockGists[userId][gistId].production_status = status;
    mockGists[userId][gistId].updatedAt = new Date().toISOString();
    
    // Update links
    mockLinks[userId] = links;
    
    return {
      gist: mockGists[userId][gistId],
      links: mockLinks[userId]
    };
  }
  
  // Original implementation for production
  try {
    await db.runTransaction(async (transaction) => {
      // Get the user document
      const userRef = usersCollection.doc(userId);
      const userDoc = await transaction.get(userRef);
      
      if (!userDoc.exists) {
        throw new Error('User not found');
      }
      
      const userData = userDoc.data() as User;
      const gists = userData.gists || [];
      const existingLinks = userData.links || [];
      
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
      
      // Update links if provided
      if (links && links.length > 0) {
        transaction.update(userRef, { links });
      }
      
      // Find and update all related links
      existingLinks.forEach((link, linkIndex) => {
        if (link.gistId === gistId) {
          transaction.update(userRef, {
            [`links.${linkIndex}.inProduction`]: inProduction,
            [`links.${linkIndex}.production_status`]: status,
            [`links.${linkIndex}.updatedAt`]: admin.firestore.FieldValue.serverTimestamp()
          });
        }
      });
    });
    
    // Get updated data
    const userDoc = await usersCollection.doc(userId).get();
    const userData = userDoc.data() as User;
    const gist = userData.gists?.find(g => g.id === gistId);
    
    return {
      gist,
      links: userData.links || []
    };
  } catch (error) {
    console.error(`Error updating gist ${gistId} and links for user ${userId}:`, error);
    throw error;
  }
}

/**
 * Batch update multiple gists
 */
export async function batchUpdateGists(
  userId: string,
  gistIds: string[],
  inProduction: boolean,
  status: 'draft' | 'review' | 'published'
): Promise<number> {
  if (isDevelopment) {
    return mockService.batchUpdateGists(userId, gistIds, inProduction, status);
  }
  
  // Original implementation for production
  try {
    const db = admin.firestore();
    const batch = db.batch();
    let updatedCount = 0;
    
    for (const gistId of gistIds) {
      const gistRef = db.collection('users').doc(userId).collection('gists').doc(gistId);
      batch.update(gistRef, {
        inProduction,
        production_status: status,
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
      });
      updatedCount++;
    }
    
    await batch.commit();
    return updatedCount;
  } catch (error) {
    console.error(`Error batch updating gists for user ${userId}:`, error);
    throw error;
  }
}

/**
 * Test Firebase connection
 */
export async function testFirebaseConnection(): Promise<{
  success: boolean;
  projectId?: string;
  error?: string;
}> {
  try {
    const projectId = admin.app().options.projectId;
    return {
      success: true,
      projectId
    };
  } catch (error: any) {
    console.error('Error testing Firebase connection:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

// Alias functions for compatibility
export const getGists = async (userId: string): Promise<any[]> => {
  if (isDevelopment) {
    return mockService.getGists(userId);
  }
  return getUserGists(userId);
};

export const getLinks = async (userId: string): Promise<any[]> => {
  if (isDevelopment) {
    return mockService.getLinks(userId);
  }
  return getUserLinks(userId);
}; 