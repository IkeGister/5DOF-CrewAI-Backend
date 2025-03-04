import axios from 'axios';

// Get the CrewAI service URL and API key from environment variables
const CREW_AI_BASE_URL = process.env.CREW_AI_BASE_URL || 'http://localhost:5000';
const CREW_AI_API_KEY = process.env.CREW_AI_API_KEY;

/**
 * Service for interacting with the CrewAI backend
 */
export const crewAIService = {
  /**
   * Initiates the content approval process for a gist
   * 
   * @param data - The data needed for content approval
   * @returns A promise that resolves with the result of the operation
   */
  async initiateContentApproval(data: {
    userId: string;
    gistId: string;
    production_status: string;
    links?: string[];
  }) {
    try {
      console.log(`Initiating content approval for gist: ${data.gistId} (user: ${data.userId})`);
      
      // Call the CrewAI service with the necessary data
      const response = await axios.post(
        `${CREW_AI_BASE_URL}/api/content/approve`,
        data,
        {
          headers: {
            'X-API-Key': CREW_AI_API_KEY,
            'Content-Type': 'application/json'
          }
        }
      );
      
      console.log(`Content approval initiated successfully for gist: ${data.gistId}`);
      return response.data;
    } catch (error) {
      console.error('Error calling CrewAI service:', error);
      throw error;
    }
  }
}; 