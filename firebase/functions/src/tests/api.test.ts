import axios from 'axios';
import * as path from 'path';
import * as dotenv from 'dotenv';

// Load environment variables from the correct path
dotenv.config({ path: path.resolve(__dirname, '../../.env') });

console.log('API Key from env:', process.env.FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY);

const API_BASE_URL = 'https://api-yufqiolzaa-uc.a.run.app/api';
const TEST_USER_ID = 'test-user-123';
const TEST_GIST_ID = 'test-gist-456';

async function testEndpoints() {
  try {
    // Test fetchUserGist
    console.log('\n🧪 Testing fetchUserGist...');
    const gistResponse = await axios.get(
      `${API_BASE_URL}/gists/${TEST_USER_ID}/${TEST_GIST_ID}`,
      {
        headers: {
          'X-API-Key': process.env.FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY
        }
      }
    );
    console.log('✅ fetchUserGist Response:', gistResponse.data);

    // Test updateGistProductionStatus
    console.log('\n🧪 Testing updateGistProductionStatus...');
    const updateResponse = await axios.post(
      `${API_BASE_URL}/gists/${TEST_USER_ID}/${TEST_GIST_ID}/production`,
      {},
      {
        headers: {
          'X-API-Key': process.env.FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY
        }
      }
    );
    console.log('✅ updateGistProductionStatus Response:', updateResponse.data);

  } catch (error: any) {
    console.error('❌ Test failed:', error.response?.data || error.message);
  }
}

// Run tests
testEndpoints(); 