import axios from 'axios';

const CREW_AI_BASE_URL = process.env.CREW_AI_BASE_URL || 'http://localhost:5000';
const API_KEY = process.env.FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY;

export const crewAIService = {
  async initiateContentApproval(gistData: any) {
    try {
      const response = await axios.post(
        `${CREW_AI_BASE_URL}/api/content/approve`,
        gistData,
        {
          headers: {
            'X-API-Key': API_KEY,
            'Content-Type': 'application/json'
          }
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error calling CrewAI service:', error);
      throw error;
    }
  }
}; 