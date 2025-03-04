import { Request, Response } from 'express';
import * as firebaseService from '../services/firebase_service';
import { crewAIService } from '../services/crewAIService';

/**
 * Fetch user gists
 * 
 * @param req Express request
 * @param res Express response
 */
export const fetchUserGists = async (req: Request, res: Response) => {
  try {
    const { userId } = req.params;
    
    if (!userId) {
      return res.status(400).json({ error: 'User ID is required' });
    }
    
    // Use the Firebase service to get user gists
    const gists = await firebaseService.getUserGists(userId);
    
    return res.status(200).json({ 
      success: true, 
      gists 
    });
  } catch (error: any) {
    console.error('Error fetching user gists:', error);
    return res.status(500).json({ 
      error: 'Failed to fetch user gists',
      message: error.message 
    });
  }
};

/**
 * Fetch a specific gist for a user
 * 
 * @param req Express request
 * @param res Express response
 */
export const fetchUserGist = async (req: Request, res: Response) => {
  try {
    const { userId, gistId } = req.params;
    
    if (!userId || !gistId) {
      return res.status(400).json({ error: 'User ID and Gist ID are required' });
    }
    
    // Use the Firebase service to get the gist
    const gist = await firebaseService.getGist(userId, gistId);
    
    if (!gist) {
      return res.status(404).json({ error: 'Gist not found' });
    }
    
    return res.status(200).json({ 
      success: true, 
      data: gist 
    });
  } catch (error: any) {
    console.error('Error fetching user gist:', error);
    return res.status(500).json({ 
      error: 'Failed to fetch user gist',
      message: error.message 
    });
  }
};

/**
 * Update gist production status
 * 
 * @param req Express request
 * @param res Express response
 */
export const updateGistProductionStatus = async (req: Request, res: Response) => {
  try {
    const { userId, gistId } = req.params;
    const { inProduction, production_status } = req.body;
    
    if (!gistId) {
      return res.status(400).json({ error: 'Gist ID is required' });
    }
    
    if (!userId) {
      return res.status(400).json({ error: 'User ID is required' });
    }
    
    if (typeof inProduction !== 'boolean') {
      return res.status(400).json({ error: 'inProduction must be a boolean' });
    }
    
    if (!['draft', 'review', 'published'].includes(production_status)) {
      return res.status(400).json({ error: 'Invalid production_status' });
    }
    
    // Use the Firebase service to update the gist status
    await firebaseService.updateGistStatus(userId, gistId, inProduction, production_status);
    
    // If moving to production, initiate CrewAI workflow
    if (inProduction && production_status === 'review') {
      // Get the gist data
      const gist = await firebaseService.getGist(userId, gistId);
      
      if (gist) {
        // Initiate CrewAI workflow
        try {
          await crewAIService.initiateContentApproval(gist);
        } catch (error) {
          console.error('Error initiating CrewAI workflow:', error);
        }
      }
    }
    
    return res.status(200).json({ 
      success: true, 
      message: 'Gist production status updated successfully' 
    });
  } catch (error: any) {
    console.error('Error updating gist production status:', error);
    return res.status(500).json({ 
      error: 'Failed to update gist production status',
      message: error.message 
    });
  }
};

/**
 * Fetch user links
 * 
 * @param req Express request
 * @param res Express response
 */
export const fetchUserLinks = async (req: Request, res: Response) => {
  try {
    const { userId } = req.params;
    
    if (!userId) {
      return res.status(400).json({ error: 'User ID is required' });
    }
    
    // Use the Firebase service to get user links
    const links = await firebaseService.getUserLinks(userId);
    
    return res.status(200).json({ 
      success: true, 
      links 
    });
  } catch (error: any) {
    console.error('Error fetching user links:', error);
    return res.status(500).json({ 
      error: 'Failed to fetch user links',
      message: error.message 
    });
  }
};

/**
 * Update multiple gists and their links in a batch operation
 * 
 * @param req Express request
 * @param res Express response
 */
export const batchUpdateGists = async (req: Request, res: Response) => {
  try {
    const { userId } = req.params;
    const { gistIds, inProduction, production_status } = req.body;
    
    if (!userId) {
      return res.status(400).json({ error: 'User ID is required' });
    }
    
    if (!gistIds || !Array.isArray(gistIds) || gistIds.length === 0) {
      return res.status(400).json({ error: 'gistIds must be a non-empty array' });
    }
    
    if (typeof inProduction !== 'boolean') {
      return res.status(400).json({ error: 'inProduction must be a boolean' });
    }
    
    if (!['draft', 'review', 'published'].includes(production_status)) {
      return res.status(400).json({ error: 'Invalid production_status' });
    }
    
    // Use the Firebase service to batch update gists
    await firebaseService.batchUpdateGists(
      userId,
      gistIds,
      inProduction,
      production_status
    );
    
    return res.status(200).json({ 
      success: true, 
      message: 'Gists updated successfully' 
    });
  } catch (error: any) {
    console.error('Error batch updating gists:', error);
    return res.status(500).json({ 
      error: 'Failed to batch update gists',
      message: error.message 
    });
  }
};

/**
 * Update a gist and all its related links atomically
 * 
 * @param req Express request
 * @param res Express response
 */
export const updateGistAndLinks = async (req: Request, res: Response) => {
  try {
    const { userId, gistId } = req.params;
    const { inProduction, production_status } = req.body;
    
    if (!gistId) {
      return res.status(400).json({ error: 'Gist ID is required' });
    }
    
    if (!userId) {
      return res.status(400).json({ error: 'User ID is required' });
    }
    
    if (typeof inProduction !== 'boolean') {
      return res.status(400).json({ error: 'inProduction must be a boolean' });
    }
    
    if (!['draft', 'review', 'published'].includes(production_status)) {
      return res.status(400).json({ error: 'Invalid production_status' });
    }
    
    // Use the Firebase service to update the gist and its links
    await firebaseService.updateGistAndLinks(userId, gistId, inProduction, production_status);
    
    return res.status(200).json({ 
      success: true, 
      message: 'Gist and related links updated successfully' 
    });
  } catch (error: any) {
    console.error('Error updating gist and links:', error);
    return res.status(500).json({ 
      error: 'Failed to update gist and links',
      message: error.message 
    });
  }
};
