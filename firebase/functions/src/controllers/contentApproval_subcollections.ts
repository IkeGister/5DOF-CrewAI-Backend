import { Request, Response } from 'express';
import * as firebaseServiceSubcollections from '../services/firebase_service_subcollections';
import { crewAIService } from '../services/crewAIService';
import { gistOperationsSubcollections } from '../services/gistOperations_subcollections';

// Use subcollection-based database service
const service = firebaseServiceSubcollections;
const gistOps = gistOperationsSubcollections;

/**
 * Update gist production status (Subcollection Version)
 * 
 * This endpoint checks if the gist has a valid link and then updates
 * its status to "Reviewing Content" and triggers the content approval process.
 * 
 * Uses the subcollection-based database structure.
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
    // Using the gistOperations service for consistent error handling
    const gistResult = await gistOps.getGist(userId, gistId);
    
    if (!gistResult.success) {
      console.log(`[updateGistProductionStatus] ${gistResult.error}`);
      return res.status(gistResult.code || 404).json({ error: gistResult.error });
    }
    
    const gist = gistResult.data;
    console.log(`[updateGistProductionStatus] Found gist:`, JSON.stringify(gist, null, 2));
    
    // Check if the gist has a link property
    if (!gist.link) {
      // Also check if there are any links in the links subcollection
      const linksResult = await gistOps.getGistLinks(userId, gistId);
      
      if (!linksResult.success || !linksResult.links || linksResult.links.length === 0) {
        console.log(`[updateGistProductionStatus] No link found for gist ${gistId}`);
        return res.status(200).json({ 
          success: false, 
          linkFound: false,
          message: 'No link associated with this gist. Status not updated.' 
        });
      }
      
      // Use the first link's URL
      const linkUrl = linksResult.links[0].url;
      console.log(`[updateGistProductionStatus] Found link in subcollection for gist ${gistId}: ${linkUrl}`);
      
      // Proceed with this link URL
      return processGistWithLink(userId, gistId, linkUrl, res);
    }
    
    // If the gist has a direct link property, use that
    const linkUrl = gist.link;
    console.log(`[updateGistProductionStatus] Found direct link property for gist ${gistId}: ${linkUrl}`);
    
    return processGistWithLink(userId, gistId, linkUrl, res);
  } catch (error) {
    console.error('[updateGistProductionStatus] Error updating gist production status:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
};

/**
 * Helper function to process a gist with a link
 * 
 * @param userId User ID
 * @param gistId Gist ID
 * @param linkUrl Link URL
 * @param res Express response
 */
async function processGistWithLink(userId: string, gistId: string, linkUrl: string, res: Response) {
  // Update the gist status
  console.log(`[processGistWithLink] Updating gist status to inProduction=true and production_status="Reviewing Content"`);
  const result = await service.updateGistStatus(
    userId,
    gistId,
    true, // Always set to true
    "Reviewing Content" as any // Use type assertion to bypass parameter type checking
  );
  
  console.log(`[processGistWithLink] Update result:`, result);
  
  // Check if the result is an error response
  if (result && typeof result === 'object' && 'success' in result && result.success === false) {
    console.log(`[processGistWithLink] Error in result: ${result.error}`);
    return res.status(result.code || 500).json({ error: result.error || 'Internal server error' });
  }
  
  // Always initiate content approval since we're putting it into production
  try {
    // Pass the link URL to the CrewAI service
    console.log(`[processGistWithLink] Initiating content approval with CrewAI service`);
    await crewAIService.initiateContentApproval(
      userId,
      gistId,
      linkUrl // Pass the link URL to the service
    );
  } catch (error) {
    console.error('[processGistWithLink] Error initiating content approval:', error);
    // Continue with the response even if content approval fails
  }
  
  console.log(`[processGistWithLink] Successfully updated gist status, returning success response`);
  return res.json({ 
    success: true, 
    linkFound: true,
    link: linkUrl, // Return the link URL string in the response
    message: 'Gist production status updated' 
  });
} 