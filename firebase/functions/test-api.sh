#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# API Key (will be redacted in logs)
API_KEY="AIzaSyBpyUfx_HjOdkkaVO2HnOyIPtVDHb7XI6Q"

# Base URL
BASE_URL="http://localhost:3000"

# Test user ID
TEST_USER="test_user_1741057003"
TEST_GIST="gist_1741057003"

# Function to make API requests
make_request() {
    local method=$1
    local endpoint=$2
    local data=$3
    
    echo -e "${YELLOW}Testing: ${method} ${endpoint}${NC}"
    
    if [ "$method" == "GET" ]; then
        response=$(curl -s -X GET -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" "${BASE_URL}${endpoint}")
    else
        response=$(curl -s -X "$method" -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" -d "$data" "${BASE_URL}${endpoint}")
    fi
    
    # Check if response is valid JSON
    if echo "$response" | jq . >/dev/null 2>&1; then
        echo -e "${GREEN}Success:${NC}"
        echo "$response" | jq .
    else
        echo -e "${RED}Error: Invalid response${NC}"
        echo "$response"
    fi
    
    echo ""
}

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo -e "${RED}Error: jq is not installed. Please install it with 'brew install jq'${NC}"
    exit 1
fi

# Check if server is running
if ! curl -s "${BASE_URL}/api/health" > /dev/null; then
    echo -e "${RED}Error: Server is not running. Please start the server with 'NODE_ENV=development npx ts-node src/index.ts'${NC}"
    exit 1
fi

echo -e "${GREEN}Starting API tests...${NC}"
echo ""

# Test health endpoint
make_request "GET" "/api/health"

# Test gists endpoints
make_request "GET" "/api/gists/${TEST_USER}"
make_request "GET" "/api/gists/${TEST_USER}/${TEST_GIST}"

# Test links endpoint
make_request "GET" "/api/links/${TEST_USER}"

# Test updating gist status
make_request "PUT" "/api/gists/${TEST_USER}/${TEST_GIST}/status" '{"production": true}'

# Test batch update
make_request "PUT" "/api/gists/${TEST_USER}/batch/status" '{"gistIds": ["gist_1741057003"], "production": true}'

# Test updating gist with links
make_request "PUT" "/api/gists/${TEST_USER}/${TEST_GIST}/with-links" '{"links": ["link1", "link2"]}'

# Test error cases
echo -e "${YELLOW}Testing error cases:${NC}"
echo ""

# Test invalid API key
echo -e "${YELLOW}Testing: Invalid API Key${NC}"
response=$(curl -s -X GET -H "X-API-Key: invalid_key" -H "Content-Type: application/json" "${BASE_URL}/api/health")
echo -e "${RED}Expected error:${NC}"
echo "$response" | jq .
echo ""

# Test non-existent user
make_request "GET" "/api/gists/non_existent_user"

# Test non-existent gist
make_request "GET" "/api/gists/${TEST_USER}/non_existent_gist"

# Test invalid JSON payload
echo -e "${YELLOW}Testing: Invalid JSON payload${NC}"
response=$(curl -s -X PUT -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" -d "invalid_json" "${BASE_URL}/api/gists/${TEST_USER}/${TEST_GIST}/status")
echo -e "${RED}Expected error:${NC}"
echo "$response" | jq .
echo ""

echo -e "${GREEN}API tests completed!${NC}"

# Save sample responses for documentation
echo -e "${YELLOW}Saving sample responses for documentation...${NC}"
mkdir -p ./test-results
make_request "GET" "/api/health" > /dev/null
curl -s -X GET -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" "${BASE_URL}/api/health" | jq . > ./test-results/health.json
curl -s -X GET -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" "${BASE_URL}/api/gists/${TEST_USER}" | jq . > ./test-results/gists.json
curl -s -X GET -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" "${BASE_URL}/api/gists/${TEST_USER}/${TEST_GIST}" | jq . > ./test-results/gist.json
curl -s -X GET -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" "${BASE_URL}/api/links/${TEST_USER}" | jq . > ./test-results/links.json
echo -e "${GREEN}Sample responses saved to ./test-results directory${NC}" 