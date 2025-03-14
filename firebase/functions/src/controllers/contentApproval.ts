import { Request, Response } from 'express';
import * as firebaseService from '../services/firebase_service';
import { crewAIService } from '../services/crewAIService';

// Always use real database service
const service = firebaseService;

/**
 * Update gist production status
 * 
 * This endpoint checks if the gist has a valid link and then updates
 * its status to "Reviewing Content" and triggers the content approval process.
 * 
 * @param req Express request
 * @param res Express response
 */
export const updateGistProductionStatus = async (req: Request, res: Response) => {
  try {
    // Get the user ID and gist ID from the request parameters
    const { userId, gistId } = req.params;
    
    console.log(`[updateGistProductionStatus] Request received with params:`, req.params);
    console.log(`[updateGistProductionStatus] Headers:`, req.headers);
    
    if (!userId || !gistId) {
      console.log(`[updateGistProductionStatus] Missing userId or gistId`);
      return res.status(400).json({ error: 'User ID and Gist ID are required' });
    }
    
    console.log(`[updateGistProductionStatus] Looking for gist ${gistId} for user ${userId}`);
    
    // First, retrieve the gist to get its link
    const gist = await service.getGist(userId, gistId);
    
    if (!gist) {
      console.log(`[updateGistProductionStatus] Gist ${gistId} not found for user ${userId}`);
      return res.status(404).json({ error: 'Gist not found' });
    }
    
    console.log(`[updateGistProductionStatus] Found gist:`, JSON.stringify(gist, null, 2));
    
    // Check if the gist has a link property
    if (!gist.link) {
      console.log(`[updateGistProductionStatus] No link found for gist ${gistId}`);
      return res.status(200).json({ 
        success: false, 
        linkFound: false,
        message: 'No link associated with this gist. Status not updated.' 
      });
    }
    
    // Store the link URL in memory - this will be passed to the CrewAI service
    const linkUrl = gist.link; // This is the URL string, not an object
    console.log(`[updateGistProductionStatus] Found link for gist ${gistId}: ${linkUrl}`);
    
    // Use the service variable instead of directly calling firebaseService
    console.log(`[updateGistProductionStatus] Updating gist status to inProduction=true and production_status="Reviewing Content"`);
    const result = await service.updateGistStatus(
      userId,
      gistId,
      true, // Always set to true
      "Reviewing Content" as any // Use type assertion to bypass parameter type checking
    );
    
    console.log(`[updateGistProductionStatus] Update result:`, result);
    
    // Check if the result is an error response
    if (result && !result.success && result.code) {
      console.log(`[updateGistProductionStatus] Error in result: ${result.error}`);
      if (result.code === 404) {
        return res.status(404).json({ error: result.error || 'Gist not found' });
      } else {
        return res.status(result.code).json({ error: result.error || 'Internal server error' });
      }
    }
    
    // Always initiate content approval since we're putting it into production
    try {
      // Pass the link URL to the CrewAI service
      console.log(`[updateGistProductionStatus] Initiating content approval with CrewAI service`);
      await crewAIService.initiateContentApproval(
        userId,
        gistId,
        linkUrl // Pass the link URL to the service
      );
    } catch (error) {
      console.error('[updateGistProductionStatus] Error initiating content approval:', error);
      // Continue with the response even if content approval fails
    }
    
    console.log(`[updateGistProductionStatus] Successfully updated gist status, returning success response`);
    return res.json({ 
      success: true, 
      linkFound: true,
      link: linkUrl, // Return the link URL string in the response
      message: 'Gist production status updated' 
    });
  } catch (error) {
    console.error('[updateGistProductionStatus] Error updating gist production status:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
};
