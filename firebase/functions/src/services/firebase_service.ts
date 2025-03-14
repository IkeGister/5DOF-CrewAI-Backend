import * as admin from 'firebase-admin';
import { usersCollection } from '../config/firebase';

// Always use real database connections - no mocks allowed
console.log(`Firebase Service running in REAL DATABASE MODE ONLY`);

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
  inProduction?: boolean;
  production_status?: string;
  createdAt?: any;
  updatedAt?: any;
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
  // Updated implementation to match database structure
  try {
    console.log(`[getGist] Looking for gist ${gistId} for user ${userId}`);
    
    const db = admin.firestore();
    const userRef = db.collection('users').doc(userId);
    const userDoc = await userRef.get();
    
    if (!userDoc.exists) {
      console.log(`[getGist] User ${userId} not found`);
      return null;
    }
    
    const userData = userDoc.data();
    if (!userData) {
      console.log(`[getGist] User data is empty for ${userId}`);
      return null;
    }
    
    console.log(`[getGist] User data retrieved. Gists property type: ${typeof userData.gists}`);
    console.log(`[getGist] Is gists an array? ${Array.isArray(userData.gists)}`);
    
    // Check if gists exists and is an array
    if (userData.gists && Array.isArray(userData.gists)) {
      console.log(`[getGist] Gists array length: ${userData.gists.length}`);
      console.log(`[getGist] Available gistIds: ${JSON.stringify(userData.gists.map(g => g.gistId || g.id))}`);
      
      // Find the gist by gistId
      const gist = userData.gists.find(g => g.gistId === gistId);
      if (gist) {
        console.log(`[getGist] Found gist in array with gistId: ${gist.gistId}`);
        return gist;
      }
      
      // Try finding by 'id' property as a fallback
      const gistById = userData.gists.find(g => g.id === gistId);
      if (gistById) {
        console.log(`[getGist] Found gist in array with id: ${gistById.id}`);
        return gistById;
      }
    } 
    // Check if gists exists and is an object with numeric keys
    else if (userData.gists && typeof userData.gists === 'object') {
      console.log(`[getGist] Gists is an object with keys: ${Object.keys(userData.gists).join(', ')}`);
      
      // Look through the object entries
      for (const key in userData.gists) {
        const gist = userData.gists[key];
        console.log(`[getGist] Checking gist at key ${key} with gistId: ${gist?.gistId || 'undefined'} and id: ${gist?.id || 'undefined'}`);
        
        if (gist && (gist.gistId === gistId || gist.id === gistId)) {
          console.log(`[getGist] Found matching gist at key ${key}`);
          return gist;
        }
      }
    }
    
    console.log(`[getGist] Gist ${gistId} not found for user ${userId}`);
    return null;
  } catch (error) {
    console.error(`[getGist] Error getting gist ${gistId} for user ${userId}:`, error);
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
  // Original implementation for production
  try {
    console.log(`[updateGistStatus] Updating status for gist ${gistId} for user ${userId}`);
    console.log(`[updateGistStatus] Setting inProduction=${inProduction}, status=${status}`);
    
    // Get the user document
    const userRef = usersCollection.doc(userId);
    const userDoc = await userRef.get();
    
    if (!userDoc.exists) {
      throw new Error('User not found');
    }
    
    const userData = userDoc.data() as User;
    const gists = userData.gists;
    
    // Handle the case where gists is not defined
    if (!gists) {
      throw new Error('Gists not found');
    }
    
    // Handle the case where gists is an object with numeric keys
    if (typeof gists === 'object' && !Array.isArray(gists)) {
      // Check if the gist exists in the object
      let found = false;
      
      // Try to find the gist by ID
      for (const key in gists as Record<string, any>) {
        if (Object.prototype.hasOwnProperty.call(gists, key)) {
          const gist = (gists as Record<string, any>)[key];
          if (gist && (gist.id === gistId || gist.gistId === gistId)) {
            // Update both top-level properties and the nested status object
            console.log(`[updateGistStatus] Found gist at key ${key}, updating status`);
            await userRef.update({
              // Top-level properties
              [`gists.${key}.inProduction`]: inProduction,
              [`gists.${key}.production_status`]: status,
              // Nested status object
              [`gists.${key}.status.inProduction`]: inProduction,
              [`gists.${key}.status.production_status`]: status
            });
            
            found = true;
            break;
          }
        }
      }
      
      if (!found) {
        // If the gist doesn't exist, add it to the object
        console.log(`[updateGistStatus] Gist not found, adding new entry`);
        const newKey = Object.keys(gists).length;
        await userRef.update({
          [`gists.${newKey}.id`]: gistId,
          [`gists.${newKey}.inProduction`]: inProduction,
          [`gists.${newKey}.production_status`]: status,
          [`gists.${newKey}.status.inProduction`]: inProduction,
          [`gists.${newKey}.status.production_status`]: status
        });
      }
      
      // Return the updated user document
      console.log(`[updateGistStatus] Successfully updated gist status`);
      const updatedUserDoc = await userRef.get();
      const updatedUserData = updatedUserDoc.data() as User;
      
      return updatedUserData.gists;
    }
    
    // Handle the case where gists is an array
    if (Array.isArray(gists)) {
      // Find the gist index
      const gistIndex = gists.findIndex(g => g.id === gistId || g.gistId === gistId);
      
      if (gistIndex === -1) {
        throw new Error('Gist not found');
      }
      
      console.log(`[updateGistStatus] Found gist at index ${gistIndex}, updating status`);
      // Update both top-level properties and the nested status object
      await userRef.update({
        // Top-level properties
        [`gists.${gistIndex}.inProduction`]: inProduction,
        [`gists.${gistIndex}.production_status`]: status,
        // Nested status object
        [`gists.${gistIndex}.status.inProduction`]: inProduction,
        [`gists.${gistIndex}.status.production_status`]: status
      });
      
      // Return updated gist
      console.log(`[updateGistStatus] Successfully updated gist status`);
      const updatedUserDoc = await userRef.get();
      const updatedUserData = updatedUserDoc.data() as User;
      return updatedUserData.gists?.[gistIndex] || null;
    }
    
    // If we get here, gists is neither an object nor an array
    throw new Error('Gists has an unsupported type');
  } catch (error) {
    console.error(`[updateGistStatus] Error updating gist ${gistId} for user ${userId}:`, error);
    // Return a structured error response instead of throwing
    return {
      success: false,
      error: error instanceof Error ? error.message : String(error),
      code: error instanceof Error && 
            (error.message === 'Gist not found' || 
             error.message === 'User not found' || 
             error.message === 'Gists not found') ? 404 : 500
    };
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
 * Update a gist and its links
 */
export async function updateGistAndLinks(
  userId: string,
  gistId: string,
  links: string[] = [],
  inProduction: boolean,
  status: 'draft' | 'review' | 'published'
): Promise<any> {
  // Original implementation for production
  try {
    console.log(`[updateGistAndLinks] Updating gist ${gistId} and links for user ${userId}`);
    console.log(`[updateGistAndLinks] Setting inProduction=${inProduction}, status=${status}`);
    
    // Get the user document
    const userRef = usersCollection.doc(userId);
    const userDoc = await userRef.get();
    
    if (!userDoc.exists) {
      throw new Error('User not found');
    }
    
    const userData = userDoc.data() as User;
    const gists = userData.gists;
    const existingLinks = userData.links;
    
    // Handle the case where gists is not defined
    if (!gists) {
      throw new Error('Gists not found');
    }
    
    // Handle the case where gists is an object with keys
    if (typeof gists === 'object' && !Array.isArray(gists)) {
      let gistKey = null;
      
      // Try to find the gist by ID
      for (const key in gists as Record<string, any>) {
        if (Object.prototype.hasOwnProperty.call(gists, key)) {
          const gist = (gists as Record<string, any>)[key];
          if (gist && (gist.id === gistId || gist.gistId === gistId)) {
            gistKey = key;
            break;
          }
        }
      }
      
      if (gistKey === null) {
        throw new Error('Gist not found');
      }
      
      // Update both top-level properties and the nested status object
      console.log(`[updateGistAndLinks] Found gist at key ${gistKey}, updating status`);
      await userRef.update({
        // Top-level properties
        [`gists.${gistKey}.inProduction`]: inProduction,
        [`gists.${gistKey}.production_status`]: status,
        // Nested status object
        [`gists.${gistKey}.status.inProduction`]: inProduction,
        [`gists.${gistKey}.status.production_status`]: status
      });
      
      // Update links if provided
      if (links && links.length > 0) {
        await userRef.update({ links });
      }
      
      // Find and update all related links
      if (Array.isArray(existingLinks)) {
        for (let linkIndex = 0; linkIndex < existingLinks.length; linkIndex++) {
          const link = existingLinks[linkIndex];
          if (link && link.gistId === gistId) {
            await userRef.update({
              [`links.${linkIndex}.inProduction`]: inProduction,
              [`links.${linkIndex}.production_status`]: status
            });
          }
        }
      }
      
      // Get updated data
      console.log(`[updateGistAndLinks] Successfully updated gist status and links`);
      const updatedUserDoc = await userRef.get();
      const updatedUserData = updatedUserDoc.data() as User;
      
      return {
        gist: (updatedUserData.gists as Record<string, any>)[gistKey],
        links: updatedUserData.links || []
      };
    }
    
    // Handle the case where gists is an array
    if (Array.isArray(gists)) {
      // Make sure gists is an array
      if (!Array.isArray(gists)) {
        throw new Error('Gists is not an array');
      }
      
      // Find the gist index
      const gistIndex = gists.findIndex(g => g.id === gistId || g.gistId === gistId);
      
      if (gistIndex === -1) {
        throw new Error('Gist not found');
      }
      
      // Update both top-level properties and the nested status object
      console.log(`[updateGistAndLinks] Found gist at index ${gistIndex}, updating status`);
      await userRef.update({
        // Top-level properties
        [`gists.${gistIndex}.inProduction`]: inProduction,
        [`gists.${gistIndex}.production_status`]: status,
        // Nested status object
        [`gists.${gistIndex}.status.inProduction`]: inProduction,
        [`gists.${gistIndex}.status.production_status`]: status
      });
      
      // Update links if provided
      if (links && links.length > 0) {
        await userRef.update({ links });
      }
      
      // Find and update all related links
      if (Array.isArray(existingLinks)) {
        for (let linkIndex = 0; linkIndex < existingLinks.length; linkIndex++) {
          const link = existingLinks[linkIndex];
          if (link && link.gistId === gistId) {
            await userRef.update({
              [`links.${linkIndex}.inProduction`]: inProduction,
              [`links.${linkIndex}.production_status`]: status
            });
          }
        }
      }
      
      // Get updated data
      console.log(`[updateGistAndLinks] Successfully updated gist status and links`);
      const updatedUserDoc = await userRef.get();
      const updatedUserData = updatedUserDoc.data() as User;
      const updatedGist = updatedUserData.gists?.find(g => g.id === gistId || g.gistId === gistId);
      
      return {
        gist: updatedGist,
        links: updatedUserData.links || []
      };
    }
    
    // If we get here, gists is neither an object nor an array
    throw new Error('Gists has an unsupported type');
  } catch (error) {
    console.error(`[updateGistAndLinks] Error updating gist ${gistId} and links for user ${userId}:`, error);
    // Return a structured error response instead of throwing
    return {
      success: false,
      error: error instanceof Error ? error.message : String(error),
      code: error instanceof Error && 
            (error.message === 'Gist not found' || 
             error.message === 'User not found' || 
             error.message === 'Gists not found') ? 404 : 500
    };
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
): Promise<number | { success: boolean; error: string; code: number }> {
  // Original implementation for production
  try {
    // In the mock implementation, we're using a different data structure
    // For the real implementation, we need to use the Firestore collection structure
    const userRef = usersCollection.doc(userId);
    const userDoc = await userRef.get();
    
    if (!userDoc.exists) {
      throw new Error('User not found');
    }
    
    let updatedCount = 0;
    const userData = userDoc.data() as User;
    const gists = userData.gists;
    
    // Handle the case where gists is not defined
    if (!gists) {
      throw new Error('Gists not found');
    }
    
    // Handle the case where gists is an object with numeric keys
    if (typeof gists === 'object' && !Array.isArray(gists)) {
      // Process each gist ID
      for (const gistId of gistIds) {
        let found = false;
        
        // Try to find the gist by ID
        for (const key in gists as Record<string, any>) {
          if (Object.prototype.hasOwnProperty.call(gists, key)) {
            const gist = (gists as Record<string, any>)[key];
            if (gist && (gist.id === gistId || gist.gistId === gistId)) {
              // Update the gist
              await userRef.update({
                [`gists.${key}.inProduction`]: inProduction,
                [`gists.${key}.production_status`]: status
              });
              
              updatedCount++;
              found = true;
              break;
            }
          }
        }
        
        if (!found) {
          console.error(`Gist ${gistId} not found for user ${userId}`);
        }
      }
      
      return updatedCount;
    }
    
    // Handle the case where gists is an array
    if (Array.isArray(gists)) {
      // Process each gist ID individually
      for (const gistId of gistIds) {
        try {
          // Find the gist index
          const gistIndex = gists.findIndex(g => g.id === gistId || g.gistId === gistId);
          
          if (gistIndex === -1) {
            console.error(`Gist ${gistId} not found for user ${userId}`);
            continue;
          }
          
          // Update the gist
          await userRef.update({
            [`gists.${gistIndex}.inProduction`]: inProduction,
            [`gists.${gistIndex}.production_status`]: status
          });
          
          updatedCount++;
        } catch (error) {
          console.error(`Error updating gist ${gistId} for user ${userId}:`, error);
          // Continue with the next gist
        }
      }
      
      return updatedCount;
    }
    
    // If we get here, gists is neither an object nor an array
    throw new Error('Gists has an unsupported type');
  } catch (error) {
    console.error(`Error batch updating gists for user ${userId}:`, error);
    // Return a structured error response instead of throwing
    return {
      success: false,
      error: error instanceof Error ? error.message : String(error),
      code: error instanceof Error && 
            (error.message === 'Gist not found' || 
             error.message === 'User not found' || 
             error.message === 'Gists not found') ? 404 : 500
    };
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
  return getUserGists(userId);
};

export const getLinks = async (userId: string): Promise<any[]> => {
  return getUserLinks(userId);
}; 