// Mock data for testing
const mockGists: Record<string, Record<string, any>> = {
  'test_user_1741057003': {
    'gist_1741057003': {
      id: 'gist_1741057003',
      title: 'Test Gist',
      content: 'This is a test gist',
      production_status: 'draft',
      inProduction: false,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
  }
};

const mockLinks: Record<string, string[]> = {
  'test_user_1741057003': ['link1', 'link2']
};

// Mock implementations
export const getGists = async (userId: string): Promise<any[]> => {
  console.log(`[MOCK] Getting gists for user: ${userId}`);
  const userGists = mockGists[userId];
  if (!userGists) return [];
  return Object.values(userGists);
};

export const getGist = async (userId: string, gistId: string): Promise<any> => {
  console.log(`[MOCK] Getting gist: ${gistId} for user: ${userId}`);
  const userGists = mockGists[userId];
  if (!userGists || !userGists[gistId]) return null;
  return userGists[gistId];
};

export const updateGistStatus = async (
  userId: string, 
  gistId: string, 
  inProduction: boolean, 
  production_status: "draft" | "review" | "published"
): Promise<any> => {
  console.log(`[MOCK] Updating gist status: ${gistId} for user: ${userId}`);
  console.log(`[MOCK] inProduction: ${inProduction}, production_status: ${production_status}`);
  
  if (!mockGists[userId]) mockGists[userId] = {};
  if (!mockGists[userId][gistId]) {
    mockGists[userId][gistId] = {
      id: gistId,
      title: 'New Test Gist',
      content: 'This is a new test gist',
      production_status: 'draft',
      inProduction: false,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
  }
  
  mockGists[userId][gistId].inProduction = inProduction;
  mockGists[userId][gistId].production_status = production_status;
  mockGists[userId][gistId].updatedAt = new Date().toISOString();
  
  return mockGists[userId][gistId];
};

export const batchUpdateGists = async (
  userId: string, 
  gistIds: string[], 
  inProduction: boolean, 
  production_status: "draft" | "review" | "published"
): Promise<number> => {
  console.log(`[MOCK] Batch updating gists for user: ${userId}`);
  console.log(`[MOCK] gistIds: ${gistIds.join(', ')}`);
  console.log(`[MOCK] inProduction: ${inProduction}, production_status: ${production_status}`);
  
  let updatedCount = 0;
  
  for (const gistId of gistIds) {
    if (!mockGists[userId]) mockGists[userId] = {};
    if (!mockGists[userId][gistId]) {
      mockGists[userId][gistId] = {
        id: gistId,
        title: `New Test Gist ${gistId}`,
        content: `This is a new test gist ${gistId}`,
        production_status: 'draft',
        inProduction: false,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };
    }
    
    mockGists[userId][gistId].inProduction = inProduction;
    mockGists[userId][gistId].production_status = production_status;
    mockGists[userId][gistId].updatedAt = new Date().toISOString();
    
    updatedCount++;
  }
  
  return updatedCount;
};

export const getLinks = async (userId: string): Promise<string[]> => {
  console.log(`[MOCK] Getting links for user: ${userId}`);
  return mockLinks[userId] || [];
};

export const updateGistAndLinks = async (
  userId: string, 
  gistId: string, 
  links: string[], 
  inProduction: boolean, 
  production_status: "draft" | "review" | "published"
): Promise<any> => {
  console.log(`[MOCK] Updating gist and links: ${gistId} for user: ${userId}`);
  console.log(`[MOCK] links: ${links.join(', ')}`);
  console.log(`[MOCK] inProduction: ${inProduction}, production_status: ${production_status}`);
  
  // Update gist
  if (!mockGists[userId]) mockGists[userId] = {};
  if (!mockGists[userId][gistId]) {
    mockGists[userId][gistId] = {
      id: gistId,
      title: 'New Test Gist',
      content: 'This is a new test gist',
      production_status: 'draft',
      inProduction: false,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
  }
  
  mockGists[userId][gistId].inProduction = inProduction;
  mockGists[userId][gistId].production_status = production_status;
  mockGists[userId][gistId].updatedAt = new Date().toISOString();
  
  // Update links
  mockLinks[userId] = links;
  
  return {
    gist: mockGists[userId][gistId],
    links: mockLinks[userId]
  };
}; 