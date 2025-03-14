import * as admin from 'firebase-admin';

// Always use real database connections - no mocks allowed
console.log(`Firebase Service running in REAL DATABASE MODE ONLY`);

// Firestore references
const db = admin.firestore();
const usersCollection = db.collection('users');

/**
 * Interfaces for Firestore documents
 */
interface Gist {
  id: string;
  title?: string;
  content?: string;
  is_played?: boolean;
  status?: {
    inProduction?: boolean;
    production_status?: string;
  };
  link?: string;
  createdAt?: any;
  updatedAt?: any;
  // Other gist properties as needed
}

interface Link {
  id: string;
  url: string;
  title?: string;
  description?: string;
  date_added: admin.firestore.Timestamp;
  gistId?: string;
  // Other link properties as needed
}

interface User {
  id: string;
  username: string;
  email: string;
  createdAt?: any;
  updatedAt?: any;
  // Note: gists and links are now stored in subcollections, not in the user document
}

/**
 * User Operations
 */

/**
 * Get a user by ID
 */
export async function getUser(userId: string): Promise<User | null> {
  try {
    const doc = await usersCollection.doc(userId).get();
    if (!doc.exists) return null;
    return { id: doc.id, ...doc.data() } as User;
  } catch (error) {
    console.error(`[getUser] Error retrieving user ${userId}:`, error);
    return null;
  }
}

/**
 * Gist Operations
 */

/**
 * Get all gists for a user
 */
export async function getUserGists(userId: string): Promise<Gist[]> {
  try {
    const gistsSnapshot = await usersCollection.doc(userId).collection('gists').get();
    if (gistsSnapshot.empty) return [];
    
    return gistsSnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    })) as Gist[];
  } catch (error) {
    console.error(`[getUserGists] Error retrieving gists for user ${userId}:`, error);
    return [];
  }
}

/**
 * Get a gist by ID for a specific user
 */
export async function getGist(userId: string, gistId: string): Promise<Gist | null> {
  try {
    console.log(`[getGist] Retrieving gist ${gistId} for user ${userId}`);
    
    const gistDoc = await usersCollection.doc(userId).collection('gists').doc(gistId).get();
    
    if (!gistDoc.exists) {
      console.log(`[getGist] Gist ${gistId} not found for user ${userId}`);
      return null;
    }
    
    const gistData = gistDoc.data() as Omit<Gist, 'id'>;
    console.log(`[getGist] Found gist ${gistId}`);
    
    return {
      id: gistDoc.id,
      ...gistData
    };
  } catch (error) {
    console.error(`[getGist] Error retrieving gist ${gistId} for user ${userId}:`, error);
    return null;
  }
}

/**
 * Create a new gist for a user
 */
export async function createGist(
  userId: string, 
  gistData: Omit<Gist, 'id' | 'createdAt' | 'updatedAt'>
): Promise<Gist | null> {
  try {
    const userDoc = await usersCollection.doc(userId).get();
    if (!userDoc.exists) {
      console.log(`[createGist] User ${userId} not found`);
      return null;
    }
    
    // Generate a new gist ID
    const gistId = `gist_${Date.now().toString(36)}`;
    const gistRef = usersCollection.doc(userId).collection('gists').doc(gistId);
    
    const newGist = {
      ...gistData,
      id: gistId,
      createdAt: admin.firestore.FieldValue.serverTimestamp(),
      updatedAt: admin.firestore.FieldValue.serverTimestamp()
    };
    
    await gistRef.set(newGist);
    
    // If the gist has a link property, create a link document in the links subcollection
    if (gistData.link) {
      const linkId = `link_${Date.now().toString(36)}`;
      const linkRef = gistRef.collection('links').doc(linkId);
      
      await linkRef.set({
        id: linkId,
        url: gistData.link,
        title: gistData.title || 'Gist Link',
        description: 'Primary link for gist',
        date_added: admin.firestore.FieldValue.serverTimestamp(),
        gistId: gistId
      });
    }
    
    // Return the created gist
    const createdGistDoc = await gistRef.get();
    const createdGistData = createdGistDoc.data() as Omit<Gist, 'id'>;
    return {
      id: createdGistDoc.id,
      ...createdGistData
    };
  } catch (error) {
    console.error(`[createGist] Error creating gist for user ${userId}:`, error);
    return null;
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
): Promise<Gist | { success: false, error: string, code: number }> {
  try {
    console.log(`[updateGistStatus] Updating status for gist ${gistId} for user ${userId}`);
    
    // Get the user document to ensure it exists
    const userDoc = await usersCollection.doc(userId).get();
    if (!userDoc.exists) {
      console.log(`[updateGistStatus] User ${userId} not found`);
      return {
        success: false,
        error: 'User not found',
        code: 404
      };
    }
    
    // Get the gist document
    const gistRef = usersCollection.doc(userId).collection('gists').doc(gistId);
    const gistDoc = await gistRef.get();
    
    if (!gistDoc.exists) {
      console.log(`[updateGistStatus] Gist ${gistId} not found for user ${userId}`);
      return {
        success: false,
        error: 'Gist not found',
        code: 404
      };
    }
    
    // Update the gist status
    await gistRef.update({
      'status.inProduction': inProduction,
      'status.production_status': status,
      updatedAt: admin.firestore.FieldValue.serverTimestamp()
    });
    
    // Return the updated gist
    const updatedGistDoc = await gistRef.get();
    return {
      id: updatedGistDoc.id,
      ...updatedGistDoc.data()
    } as Gist;
  } catch (error) {
    console.error(`[updateGistStatus] Error updating gist ${gistId} for user ${userId}:`, error);
    return {
      success: false,
      error: error instanceof Error ? error.message : String(error),
      code: 500
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
  try {
    // Try to find the link in the user's links collection
    const linkDoc = await usersCollection.doc(userId).collection('links').doc(linkId).get();
    
    if (linkDoc.exists) {
      return {
        id: linkDoc.id,
        ...linkDoc.data()
      } as Link;
    }
    
    // If not found, search in all gists' links collections
    const gistsSnapshot = await usersCollection.doc(userId).collection('gists').get();
    
    for (const gistDoc of gistsSnapshot.docs) {
      const gistLinkDoc = await gistDoc.ref.collection('links').doc(linkId).get();
      
      if (gistLinkDoc.exists) {
        return {
          id: gistLinkDoc.id,
          ...gistLinkDoc.data()
        } as Link;
      }
    }
    
    return null;
  } catch (error) {
    console.error(`[getLink] Error retrieving link ${linkId} for user ${userId}:`, error);
    return null;
  }
}

/**
 * Get all links for a user
 */
export async function getUserLinks(userId: string): Promise<Link[]> {
  try {
    // Get links directly attached to the user
    const userLinks: Link[] = [];
    
    const userLinksSnapshot = await usersCollection.doc(userId).collection('links').get();
    if (!userLinksSnapshot.empty) {
      userLinksSnapshot.docs.forEach(doc => {
        userLinks.push({
          id: doc.id,
          ...doc.data()
        } as Link);
      });
    }
    
    // Get links attached to gists
    const gistsSnapshot = await usersCollection.doc(userId).collection('gists').get();
    
    for (const gistDoc of gistsSnapshot.docs) {
      const gistLinksSnapshot = await gistDoc.ref.collection('links').get();
      
      if (!gistLinksSnapshot.empty) {
        gistLinksSnapshot.docs.forEach(doc => {
          userLinks.push({
            id: doc.id,
            gistId: gistDoc.id,
            ...doc.data()
          } as Link);
        });
      }
    }
    
    return userLinks;
  } catch (error) {
    console.error(`[getUserLinks] Error retrieving links for user ${userId}:`, error);
    return [];
  }
}

/**
 * Get all links related to a gist for a user
 */
export async function getLinksByGistId(userId: string, gistId: string): Promise<Link[]> {
  try {
    const gistLinksSnapshot = await usersCollection
      .doc(userId)
      .collection('gists')
      .doc(gistId)
      .collection('links')
      .get();
    
    if (gistLinksSnapshot.empty) return [];
    
    return gistLinksSnapshot.docs.map(doc => ({
      id: doc.id,
      gistId,
      ...doc.data()
    })) as Link[];
  } catch (error) {
    console.error(`[getLinksByGistId] Error retrieving links for gist ${gistId}:`, error);
    return [];
  }
}

/**
 * Update a link's production status
 */
export async function updateLinkStatus(
  userId: string,
  linkId: string, 
  inProduction: boolean, 
  status: 'draft' | 'review' | 'published'
): Promise<Link | { success: false, error: string, code: number }> {
  try {
    // Try to find the link in the user's links collection
    const userLinkRef = usersCollection.doc(userId).collection('links').doc(linkId);
    const userLinkDoc = await userLinkRef.get();
    
    if (userLinkDoc.exists) {
      await userLinkRef.update({
        inProduction,
        production_status: status,
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
      });
      
      const updatedLinkDoc = await userLinkRef.get();
      return {
        id: updatedLinkDoc.id,
        ...updatedLinkDoc.data()
      } as Link;
    }
    
    // If not in user links, search in all gists' links collections
    const gistsSnapshot = await usersCollection.doc(userId).collection('gists').get();
    
    for (const gistDoc of gistsSnapshot.docs) {
      const gistLinkRef = gistDoc.ref.collection('links').doc(linkId);
      const gistLinkDoc = await gistLinkRef.get();
      
      if (gistLinkDoc.exists) {
        await gistLinkRef.update({
          inProduction,
          production_status: status,
          updatedAt: admin.firestore.FieldValue.serverTimestamp()
        });
        
        const updatedLinkDoc = await gistLinkRef.get();
        return {
          id: updatedLinkDoc.id,
          gistId: gistDoc.id,
          ...updatedLinkDoc.data()
        } as Link;
      }
    }
    
    return {
      success: false,
      error: 'Link not found',
      code: 404
    };
  } catch (error) {
    console.error(`[updateLinkStatus] Error updating link ${linkId} for user ${userId}:`, error);
    return {
      success: false,
      error: error instanceof Error ? error.message : String(error),
      code: 500
    };
  }
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
  inProduction: boolean,
  status: 'draft' | 'review' | 'published'
): Promise<{ gist: Gist, links: Link[] } | { success: false, error: string, code: number }> {
  try {
    // Get the user document to ensure it exists
    const userDoc = await usersCollection.doc(userId).get();
    if (!userDoc.exists) {
      return {
        success: false,
        error: 'User not found',
        code: 404
      };
    }
    
    // Get the gist document
    const gistRef = usersCollection.doc(userId).collection('gists').doc(gistId);
    const gistDoc = await gistRef.get();
    
    if (!gistDoc.exists) {
      return {
        success: false,
        error: 'Gist not found',
        code: 404
      };
    }
    
    // Update the gist status
    await gistRef.update({
      'status.inProduction': inProduction,
      'status.production_status': status,
      updatedAt: admin.firestore.FieldValue.serverTimestamp()
    });
    
    // Update all links related to this gist
    const gistLinksSnapshot = await gistRef.collection('links').get();
    const updatedLinks: Link[] = [];
    
    for (const linkDoc of gistLinksSnapshot.docs) {
      await linkDoc.ref.update({
        inProduction,
        production_status: status,
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
      });
      
      const updatedLinkDoc = await linkDoc.ref.get();
      updatedLinks.push({
        id: updatedLinkDoc.id,
        gistId,
        ...updatedLinkDoc.data()
      } as Link);
    }
    
    // Return the updated gist and links
    const updatedGistDoc = await gistRef.get();
    return {
      gist: {
        id: updatedGistDoc.id,
        ...updatedGistDoc.data()
      } as Gist,
      links: updatedLinks
    };
  } catch (error) {
    console.error(`[updateGistAndLinks] Error updating gist ${gistId} and links for user ${userId}:`, error);
    return {
      success: false,
      error: error instanceof Error ? error.message : String(error),
      code: 500
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
  try {
    // Get the user document to ensure it exists
    const userDoc = await usersCollection.doc(userId).get();
    if (!userDoc.exists) {
      return {
        success: false,
        error: 'User not found',
        code: 404
      };
    }
    
    let updatedCount = 0;
    const batch = db.batch();
    
    // Process each gist ID
    for (const gistId of gistIds) {
      const gistRef = usersCollection.doc(userId).collection('gists').doc(gistId);
      const gistDoc = await gistRef.get();
      
      if (gistDoc.exists) {
        batch.update(gistRef, {
          'status.inProduction': inProduction,
          'status.production_status': status,
          updatedAt: admin.firestore.FieldValue.serverTimestamp()
        });
        
        updatedCount++;
      } else {
        console.log(`[batchUpdateGists] Gist ${gistId} not found for user ${userId}`);
      }
    }
    
    // Commit the batch
    if (updatedCount > 0) {
      await batch.commit();
    }
    
    return updatedCount;
  } catch (error) {
    console.error(`[batchUpdateGists] Error batch updating gists for user ${userId}:`, error);
    return {
      success: false,
      error: error instanceof Error ? error.message : String(error),
      code: 500
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
    console.error('[testFirebaseConnection] Error testing Firebase connection:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

// Alias functions for compatibility
export const getGists = getUserGists;
export const getLinks = getUserLinks; 