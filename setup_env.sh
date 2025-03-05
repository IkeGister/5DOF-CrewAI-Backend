#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}CrewAI Backend Environment Setup${NC}"
echo "This script will help you set up your environment for local development and deployment."

# Check if .env file exists
if [ -f ".env" ]; then
    echo -e "${YELLOW}Existing .env file found.${NC}"
    read -p "Do you want to overwrite it? (y/n): " overwrite_env
    if [ "$overwrite_env" != "y" ]; then
        echo "Keeping existing .env file."
    else
        create_env=true
    fi
else
    create_env=true
fi

# Create .env file if needed
if [ "$create_env" = true ]; then
    echo -e "${GREEN}Creating .env file...${NC}"
    echo "Please enter your API keys:"
    
    read -p "Service API Key: " service_api_key
    read -p "OpenAI API Key: " openai_api_key
    read -p "OpenAI Base URL (default: https://api.openai.com/v1): " openai_base_url
    openai_base_url=${openai_base_url:-"https://api.openai.com/v1"}
    
    echo "SERVICE_API_KEY=$service_api_key" > .env
    echo "CREW_AI_API_KEY=$openai_api_key" >> .env
    echo "CREW_AI_BASE_URL=$openai_base_url" >> .env
    
    echo -e "${GREEN}.env file created successfully!${NC}"
fi

# Check if firebase directory exists
if [ ! -d "firebase" ]; then
    echo -e "${RED}Firebase directory not found. Make sure you're in the project root.${NC}"
    exit 1
fi

# Check if firebase.json.template exists
if [ ! -f "firebase/firebase.json.template" ]; then
    echo -e "${RED}firebase.json.template not found. Creating it...${NC}"
    
    # Create template file
    cat > firebase/firebase.json.template << EOL
{
  "functions": {
    "source": "functions",
    "codebase": "default",
    "ignore": [
      "node_modules",
      ".git",
      "firebase-debug.log",
      "firebase-debug.*.log"
    ],
    "predeploy": [
      "npm --prefix \"\$RESOURCE_DIR\" run lint",
      "npm --prefix \"\$RESOURCE_DIR\" run build"
    ],
    "gen": 2,
    "environmentVariables": {
      "SERVICE_API_KEY": "your_service_api_key",
      "CREW_AI_API_KEY": "your_openai_api_key",
      "CREW_AI_BASE_URL": "https://api.openai.com/v1"
    }
  }
}
EOL
    echo -e "${GREEN}firebase.json.template created successfully!${NC}"
fi

# Check if firebase.json exists
if [ -f "firebase/firebase.json" ]; then
    echo -e "${YELLOW}Existing firebase.json file found.${NC}"
    read -p "Do you want to overwrite it with values from .env? (y/n): " overwrite_firebase
    if [ "$overwrite_firebase" != "y" ]; then
        echo "Keeping existing firebase.json file."
    else
        create_firebase=true
    fi
else
    create_firebase=true
fi

# Create firebase.json if needed
if [ "$create_firebase" = true ]; then
    echo -e "${GREEN}Creating firebase.json from template and .env values...${NC}"
    
    # Read values from .env
    if [ -f ".env" ]; then
        source .env
    else
        echo -e "${RED}.env file not found. Please create it first.${NC}"
        exit 1
    fi
    
    # Create firebase.json from template with actual values
    cp firebase/firebase.json.template firebase/firebase.json
    
    # Replace placeholder values with actual values
    sed -i '' "s/your_service_api_key/$SERVICE_API_KEY/g" firebase/firebase.json
    sed -i '' "s/your_openai_api_key/$CREW_AI_API_KEY/g" firebase/firebase.json
    sed -i '' "s|https://api.openai.com/v1|$CREW_AI_BASE_URL|g" firebase/firebase.json
    
    echo -e "${GREEN}firebase.json created successfully with values from .env!${NC}"
fi

echo -e "${GREEN}Environment setup complete!${NC}"
echo -e "To deploy to Firebase, run: ${YELLOW}cd firebase && npm --prefix functions run build && firebase deploy --only functions${NC}"
echo -e "Remember that both .env and firebase/firebase.json contain sensitive information and should not be committed to version control." 