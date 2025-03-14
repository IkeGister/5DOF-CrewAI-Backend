import * as firebaseService from './firebase_service';

/**
 * GistOperations Service
 * 
 * This service handles direct database operations related to gists,
 * separate from API endpoint handlers. These functions can be called
 * directly from other services within the application.
 */
class GistOperations {
  private service: typeof firebaseService;

  constructor() {
    // Always use real database service
    this.service = firebaseService;
  }

  /**
   * Get all gists for a user
   * 
   * @param userId User ID
   * @returns Promise with gists or error
   */
  public async getGists(userId: string): Promise<any> {
    try {
      if (!userId) {
        console.error('Error: userId is required');
        return { 
          success: false, 
          error: 'User ID is required' 
        };
      }
      
      const gists = await this.service.getGists(userId);
      
      return { 
        success: true, 
        gists 
      };
    } catch (error) {
      console.error('Error fetching gists:', error);
      return { 
        success: false, 
        error: 'Failed to fetch gists',
        details: error instanceof Error ? error.message : String(error)
      };
    }
  }

  /**
   * Get a specific gist for a user
   * 
   * @param userId User ID 
   * @param gistId Gist ID
   * @returns Promise with gist or error
   */
  public async getGist(userId: string, gistId: string): Promise<any> {
    try {
      if (!userId || !gistId) {
        console.error('Error: userId and gistId are required');
        return { 
          success: false, 
          error: 'User ID and Gist ID are required' 
        };
      }
      
      const gist = await this.service.getGist(userId, gistId);
      
      if (!gist) {
        console.error(`Error: Gist ${gistId} not found for user ${userId}`);
        return { 
          success: false, 
          error: 'Gist not found',
          code: 404
        };
      }
      
      return { 
        success: true, 
        data: gist 
      };
    } catch (error) {
      console.error('Error fetching gist:', error);
      return { 
        success: false, 
        error: 'Failed to fetch gist',
        details: error instanceof Error ? error.message : String(error)
      };
    }
  }

  /**
   * Update gist workflow status
   * 
   * This function updates a gist's production status with a custom status message
   * as it moves through the CrewAI production workflow.
   * 
   * @param userId User ID
   * @param gistId Gist ID
   * @param statusMessage Custom status message (e.g. "Processing Audio", "Generating Transcript")
   * @returns Result of the update operation
   */
  public async updateGistWorkflowStatus(
    userId: string, 
    gistId: string, 
    statusMessage: string
  ): Promise<any> {
    try {
      console.log(`Updating workflow status for gist ${gistId} to: ${statusMessage}`);
      
      if (!userId || !gistId) {
        console.error('Error: userId and gistId are required');
        return { 
          success: false, 
          error: 'User ID and Gist ID are required' 
        };
      }
      
      if (!statusMessage) {
        console.error('Error: statusMessage is required');
        return { 
          success: false, 
          error: 'Status message is required' 
        };
      }
      
      // Verify the gist exists first
      const gist = await this.service.getGist(userId, gistId);
      
      if (!gist) {
        console.error(`Error: Gist ${gistId} not found for user ${userId}`);
        return { 
          success: false, 
          error: 'Gist not found',
          code: 404
        };
      }
      
      // Update the gist status - always keep inProduction=true
      const result = await this.service.updateGistStatus(
        userId,
        gistId,
        true, // Keep in production mode
        statusMessage as any // Use type assertion to bypass parameter type checking
      );
      
      // Check if the result is an error response
      if (result && !result.success) {
        console.error(`Error updating gist status: ${result.error}`);
        return result;
      }
      
      console.log(`Successfully updated gist ${gistId} status to: ${statusMessage}`);
      return { 
        success: true, 
        message: `Gist workflow status updated to: ${statusMessage}` 
      };
    } catch (error) {
      console.error('Error in updateGistWorkflowStatus:', error);
      return { 
        success: false, 
        error: 'Failed to update gist workflow status',
        details: error instanceof Error ? error.message : String(error)
      };
    }
  }
}

// Export a singleton instance
export const gistOperations = new GistOperations(); 