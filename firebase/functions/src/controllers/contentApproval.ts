import { Request, Response } from 'express';
import * as firebaseService from '../services/firebase_service';
import * as mockService from '../services/mock/firebase_service_mock';
import { crewAIService } from '../services/crewAIService';

// Define the allowed production status values
type ProductionStatus = 'draft' | 'review' | 'published';

// Use mock service in development mode
const isDevelopment = process.env.NODE_ENV === 'development';
const service = isDevelopment ? mockService : firebaseService;

/**
 * Fetch user gists
 * 
 * @param req Express request
 * @param res Express response
 */
export const fetchUserGists = async (req: Request, res: Response) => {
  try {
    // Get the user ID from the request parameters
    const { userId } = req.params;
    
    if (!userId) {
      return res.status(400).json({ error: 'User ID is required' });
    }
    
    // Use the service variable instead of directly calling firebaseService
    const gists = await service.getGists(userId);
    
    return res.json({ success: true, gists });
  } catch (error) {
    console.error('Error fetching user gists:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
};

/**
 * Fetch a specific user gist
 * 
 * @param req Express request
 * @param res Express response
 */
export const fetchUserGist = async (req: Request, res: Response) => {
  try {
    // Get the user ID and gist ID from the request parameters
    const { userId, gistId } = req.params;
    
    if (!userId || !gistId) {
      return res.status(400).json({ error: 'User ID and Gist ID are required' });
    }
    
    // Use the service variable instead of directly calling firebaseService
    const gist = await service.getGist(userId, gistId);
    
    if (!gist) {
      return res.status(404).json({ error: 'Gist not found' });
    }
    
    return res.json({ success: true, data: gist });
  } catch (error) {
    console.error('Error fetching user gist:', error);
    return res.status(500).json({ error: 'Internal server error' });
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
    // Get the user ID and gist ID from the request parameters
    const { userId, gistId } = req.params;
    // Get production status from the request body
    const { inProduction, production_status } = req.body;
    
    if (!userId || !gistId) {
      return res.status(400).json({ error: 'User ID and Gist ID are required' });
    }
    
    // Validate inProduction is a boolean
    if (typeof inProduction !== 'boolean') {
      return res.status(400).json({ error: 'inProduction must be a boolean' });
    }
    
    // Validate production_status is one of the allowed values
    if (!['draft', 'review', 'published'].includes(production_status)) {
      return res.status(400).json({ 
        error: 'Invalid production_status',
        message: 'production_status must be one of: draft, review, published'
      });
    }
    
    // Use the service variable instead of directly calling firebaseService
    await service.updateGistStatus(
      userId,
      gistId,
      inProduction,
      production_status as ProductionStatus
    );
    
    // If the gist is being put into production, initiate content approval
    if (inProduction) {
      try {
        await crewAIService.initiateContentApproval({
          userId,
          gistId,
          production_status
        });
      } catch (error) {
        console.error('Error initiating content approval:', error);
        // Continue with the response even if content approval fails
      }
    }
    
    return res.json({ success: true, message: 'Gist production status updated' });
  } catch (error) {
    console.error('Error updating gist production status:', error);
    return res.status(500).json({ error: 'Internal server error' });
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
    // Get the user ID from the request parameters
    const { userId } = req.params;
    
    if (!userId) {
      return res.status(400).json({ error: 'User ID is required' });
    }
    
    // Use the service variable instead of directly calling firebaseService
    const links = await service.getLinks(userId);
    
    return res.json({ success: true, links });
  } catch (error) {
    console.error('Error fetching user links:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
};

/**
 * Batch update gists status
 * 
 * @param req Express request
 * @param res Express response
 */
export const batchUpdateGists = async (req: Request, res: Response) => {
  try {
    // Get the user ID from the request parameters
    const { userId } = req.params;
    // Get gist IDs and production status from the request body
    const { gistIds, inProduction, production_status } = req.body;
    
    if (!userId) {
      return res.status(400).json({ error: 'User ID is required' });
    }
    
    if (!Array.isArray(gistIds) || gistIds.length === 0) {
      return res.status(400).json({ error: 'gistIds must be a non-empty array' });
    }
    
    // Validate inProduction is a boolean
    if (typeof inProduction !== 'boolean') {
      return res.status(400).json({ error: 'inProduction must be a boolean' });
    }
    
    // Validate production_status is one of the allowed values
    if (!['draft', 'review', 'published'].includes(production_status)) {
      return res.status(400).json({ 
        error: 'Invalid production_status',
        message: 'production_status must be one of: draft, review, published'
      });
    }
    
    // Update the gists production status using the appropriate service
    const updatedCount = await service.batchUpdateGists(
      userId,
      gistIds,
      inProduction,
      production_status as ProductionStatus
    );
    
    // If the gists are being put into production, initiate content approval for each
    if (inProduction) {
      try {
        // Process each gist in parallel
        await Promise.all(
          gistIds.map(gistId => 
            crewAIService.initiateContentApproval({
              userId,
              gistId,
              production_status
            })
          )
        );
      } catch (error) {
        console.error('Error initiating batch content approval:', error);
        // Continue with the response even if content approval fails
      }
    }
    
    // Return success response with the count of updated gists
    return res.status(200).json({
      success: true,
      message: 'Gists production status updated',
      count: updatedCount
    });
  } catch (error) {
    console.error('Error batch updating gists status:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
};

/**
 * Update gist and associated links
 * 
 * @param req Express request
 * @param res Express response
 */
export const updateGistAndLinks = async (req: Request, res: Response) => {
  try {
    const { userId, gistId } = req.params;
    const { links, inProduction, production_status } = req.body;
    
    if (!userId || !gistId) {
      return res.status(400).json({ error: 'User ID and Gist ID are required' });
    }
    
    if (!Array.isArray(links)) {
      return res.status(400).json({ error: 'links must be an array' });
    }
    
    if (typeof inProduction !== 'boolean') {
      return res.status(400).json({ error: 'inProduction must be a boolean' });
    }
    
    if (!['draft', 'review', 'published'].includes(production_status)) {
      return res.status(400).json({ 
        error: 'Invalid production_status',
        message: 'production_status must be one of: draft, review, published'
      });
    }
    
    // Use the service variable instead of directly calling firebaseService
    if (isDevelopment) {
      await mockService.updateGistAndLinks(
        userId,
        gistId,
        links,
        inProduction,
        production_status as ProductionStatus
      );
    } else {
      await firebaseService.updateGistAndLinks(
        userId,
        gistId,
        links,
        inProduction,
        production_status as ProductionStatus
      );
    }
    
    // If the gist is being put into production, initiate content approval
    if (inProduction && production_status === 'review') {
      try {
        await crewAIService.initiateContentApproval({
          userId,
          gistId,
          production_status,
          links
        });
      } catch (error) {
        console.error('Error initiating content approval:', error);
        // Continue even if content approval fails
      }
    }
    
    return res.json({ 
      success: true, 
      message: 'Gist and links updated'
    });
  } catch (error) {
    console.error('Error updating gist and links:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
};
