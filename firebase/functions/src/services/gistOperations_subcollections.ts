import * as firebaseServiceSubcollections from './firebase_service_subcollections';

/**
 * GistOperations Service (Subcollection Structure)
 * 
 * This service handles direct database operations related to gists using the subcollection structure,
 * separate from API endpoint handlers. These functions can be called
 * directly from other services within the application.
 */
class GistOperationsSubcollections {
  private service: typeof firebaseServiceSubcollections;

  constructor() {
    // Use the subcollection-based service
    this.service = firebaseServiceSubcollections;
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
        console.error('[GistOperationsSubcollections] Error: userId is required');
        return { 
          success: false, 
          error: 'User ID is required' 
        };
      }
      
      const gists = await this.service.getUserGists(userId);
      
      return { 
        success: true, 
        gists 
      };
    } catch (error) {
      console.error('[GistOperationsSubcollections] Error fetching gists:', error);
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
        console.error('[GistOperationsSubcollections] Error: userId and gistId are required');
        return { 
          success: false, 
          error: 'User ID and Gist ID are required' 
        };
      }
      
      const gist = await this.service.getGist(userId, gistId);
      
      if (!gist) {
        console.error(`[GistOperationsSubcollections] Error: Gist ${gistId} not found for user ${userId}`);
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
      console.error('[GistOperationsSubcollections] Error fetching gist:', error);
      return { 
        success: false, 
        error: 'Failed to fetch gist',
        details: error instanceof Error ? error.message : String(error)
      };
    }
  }

  /**
   * Create a new gist for a user
   * 
   * @param userId User ID
   * @param gistData Gist data
   * @returns Promise with created gist or error
   */
  public async createGist(userId: string, gistData: any): Promise<any> {
    try {
      if (!userId) {
        console.error('[GistOperationsSubcollections] Error: userId is required');
        return { 
          success: false, 
          error: 'User ID is required' 
        };
      }
      
      if (!gistData) {
        console.error('[GistOperationsSubcollections] Error: gistData is required');
        return { 
          success: false, 
          error: 'Gist data is required' 
        };
      }
      
      const newGist = await this.service.createGist(userId, gistData);
      
      if (!newGist) {
        console.error(`[GistOperationsSubcollections] Error: Failed to create gist for user ${userId}`);
        return { 
          success: false, 
          error: 'Failed to create gist',
          code: 500
        };
      }
      
      return { 
        success: true, 
        data: newGist 
      };
    } catch (error) {
      console.error('[GistOperationsSubcollections] Error creating gist:', error);
      return { 
        success: false, 
        error: 'Failed to create gist',
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
      console.log(`[GistOperationsSubcollections] Updating workflow status for gist ${gistId} to: ${statusMessage}`);
      
      if (!userId || !gistId) {
        console.error('[GistOperationsSubcollections] Error: userId and gistId are required');
        return { 
          success: false, 
          error: 'User ID and Gist ID are required' 
        };
      }
      
      if (!statusMessage) {
        console.error('[GistOperationsSubcollections] Error: statusMessage is required');
        return { 
          success: false, 
          error: 'Status message is required' 
        };
      }
      
      // Verify the gist exists first
      const gist = await this.service.getGist(userId, gistId);
      
      if (!gist) {
        console.error(`[GistOperationsSubcollections] Error: Gist ${gistId} not found for user ${userId}`);
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
      if (result && typeof result === 'object' && 'success' in result && result.success === false) {
        console.error(`[GistOperationsSubcollections] Error updating gist status: ${result.error}`);
        return result;
      }
      
      console.log(`[GistOperationsSubcollections] Successfully updated gist ${gistId} status to: ${statusMessage}`);
      return { 
        success: true, 
        message: `Gist workflow status updated to: ${statusMessage}` 
      };
    } catch (error) {
      console.error('[GistOperationsSubcollections] Error in updateGistWorkflowStatus:', error);
      return { 
        success: false, 
        error: 'Failed to update gist workflow status',
        details: error instanceof Error ? error.message : String(error)
      };
    }
  }

  /**
   * Get all links for a gist
   * 
   * @param userId User ID
   * @param gistId Gist ID
   * @returns Promise with links or error
   */
  public async getGistLinks(userId: string, gistId: string): Promise<any> {
    try {
      if (!userId || !gistId) {
        console.error('[GistOperationsSubcollections] Error: userId and gistId are required');
        return { 
          success: false, 
          error: 'User ID and Gist ID are required' 
        };
      }
      
      const links = await this.service.getLinksByGistId(userId, gistId);
      
      return { 
        success: true, 
        links 
      };
    } catch (error) {
      console.error('[GistOperationsSubcollections] Error fetching gist links:', error);
      return { 
        success: false, 
        error: 'Failed to fetch gist links',
        details: error instanceof Error ? error.message : String(error)
      };
    }
  }

  /**
   * Update gist and all its links
   * 
   * @param userId User ID
   * @param gistId Gist ID
   * @param inProduction Production status
   * @param status Production status message
   * @returns Result of the update operation
   */
  public async updateGistAndLinks(
    userId: string,
    gistId: string,
    inProduction: boolean,
    status: 'draft' | 'review' | 'published'
  ): Promise<any> {
    try {
      if (!userId || !gistId) {
        console.error('[GistOperationsSubcollections] Error: userId and gistId are required');
        return { 
          success: false, 
          error: 'User ID and Gist ID are required' 
        };
      }
      
      const result = await this.service.updateGistAndLinks(userId, gistId, inProduction, status);
      
      // Check if the result is an error response
      if (result && typeof result === 'object' && 'success' in result && result.success === false) {
        console.error(`[GistOperationsSubcollections] Error updating gist and links: ${result.error}`);
        return result;
      }
      
      return { 
        success: true, 
        data: result
      };
    } catch (error) {
      console.error('[GistOperationsSubcollections] Error in updateGistAndLinks:', error);
      return { 
        success: false, 
        error: 'Failed to update gist and links',
        details: error instanceof Error ? error.message : String(error)
      };
    }
  }
}

// Export a singleton instance
export const gistOperationsSubcollections = new GistOperationsSubcollections(); 