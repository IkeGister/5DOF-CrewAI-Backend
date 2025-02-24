import { db } from '../config/firebase';
import * as admin from 'firebase-admin';
import { Link, Gist, GistStatus } from '../types';

export const firestoreService = {
  async getUserGists(userId: string) {
    try {
      const userDoc = await db.collection('users').doc(userId).get();

      if (!userDoc.exists) {
        throw new Error('User not found');
      }

      const userData = userDoc.data();
      return {
        gists: userData?.gists || [],
        count: (userData?.gists || []).length
      };
    } catch (error) {
      console.error('Error fetching gists:', error);
      throw error;
    }
  },

  async updateGistStatus(userId: string, gistId: string, status: Partial<GistStatus>) {
    try {
      const userRef = db.collection('users').doc(userId);
      const userDoc = await userRef.get();
      
      if (!userDoc.exists) {
        throw new Error('User not found');
      }

      const userData = userDoc.data();
      const gists = userData?.gists || [];
      const gistIndex = gists.findIndex((g: Gist) => g.gistId === gistId);

      if (gistIndex === -1) {
        throw new Error('Gist not found');
      }

      // Update the gist status
      gists[gistIndex].status = {
        ...gists[gistIndex].status,
        ...status
      };

      // Update the document
      await userRef.update({
        gists: gists,
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
      });

      return gists[gistIndex];
    } catch (error) {
      console.error('Firestore update error:', error);
      throw error;
    }
  },

  async getUserLinks(userId: string) {
    try {
      const userDoc = await db.collection('users').doc(userId).get();

      if (!userDoc.exists) {
        throw new Error('User not found');
      }

      const userData = userDoc.data();
      return {
        links: (userData?.links || []) as Link[],
        count: (userData?.links || []).length
      };
    } catch (error) {
      console.error('Error fetching links:', error);
      throw error;
    }
  },

  // Add other Firestore operations as needed
};
