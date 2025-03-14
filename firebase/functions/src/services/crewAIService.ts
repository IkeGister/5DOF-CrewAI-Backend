import axios from 'axios';

// CrewAI Service for content approval and related operations
class CrewAIService {
  private apiKey: string;
  private baseUrl: string;

  constructor() {
    // Set API key and base URL from environment variables or use defaults for development
    this.apiKey = process.env.CREW_AI_API_KEY || 'AIzaSyBpyUfx_HjOdkkaVO2HnOyIPtVDHb7XI6Q'; // Default key for development
    this.baseUrl = process.env.CREW_AI_BASE_URL || 'http://localhost:5000'; // Default base URL for development
  }

  /**
   * Initialize content approval process for a gist
   * 
   * @param userId User ID
   * @param gistId Gist ID
   * @param linkUrl The URL of the link associated with this gist
   * @returns Promise with approval status
   */
  public async initiateContentApproval(userId: string, gistId: string, linkUrl?: string): Promise<any> {
    console.log(`Initiating content approval for gist: ${gistId} (user: ${userId})`);
    if (linkUrl) {
      console.log(`Using link URL: ${linkUrl}`);
    }
    
    try {
      // Make real API call to CrewAI service
      const response = await axios.post(
        `${this.baseUrl}/api/content-approval/initiate`,
        { 
          userId, 
          gistId,
          linkUrl, // Include the link URL in the API call
          timestamp: new Date().toISOString()
        },
        {
          headers: {
            'X-API-Key': this.apiKey,
            'Content-Type': 'application/json'
          }
        }
      );
      
      return response.data;
    } catch (error) {
      console.error('Error initiating content approval:', error);
      
      // Return a structured error response
      return {
        success: false,
        error: 'Failed to initiate content approval',
        details: error instanceof Error ? error.message : String(error)
      };
    }
  }
}

// Export a singleton instance
export const crewAIService = new CrewAIService(); 