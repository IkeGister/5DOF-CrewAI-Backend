# CrewAI Backend System

A sophisticated AI system that works like a well-coordinated team, handling tasks from content analysis to podcast creation, now with Firebase Functions integration for production workflows.

## 🌟 What Makes This Special

- **Smart Content Processing**: Turns complex documents into engaging podcast content
- **Research Power**: Uses multiple specialized tools to gather and verify information
- **Voice Generation**: Creates natural-sounding conversations using ElevenLabs technology
- **Flexible & Expandable**: Easy to add new capabilities as needed

## 🏗️ Project Structure

```
CrewAI-Backend/
├── firebase/                    # Firebase Functions
│   └── functions/
│       ├── src/
│       │   ├── config/         # Firebase configuration
│       │   │   ├── firebase.ts
│       │   │   └── serviceAccount.json
│       │   ├── controllers/    # Request handlers
│       │   │   └── contentApproval.ts
│       │   ├── middleware/     # Auth & validation
│       │   │   └── auth.ts
│       │   ├── routes/        # API routes
│       │   │   └── api.ts
│       │   ├── services/      # External services
│       │   │   ├── crewAIService.ts
│       │   │   └── firestore_service.ts
│       │   └── index.ts       # Main entry
│       ├── package.json
│       └── tsconfig.json
├── src/
│   └── CrewAI/                # CrewAI Backend
│       ├── agents/
│       │   ├── agents.py
│       │   └── gistaApp_agents/
│       │       ├── content_analysis_team/
│       │       ├── content_approval_team/
│       │       ├── script_writing_team/
│       │       └── voice_production_team/
│       ├── config/
│       │   ├── llm_config.py
│       │   ├── settings.py
│       │   ├── topics.py
│       │   └── voice_config.yaml
│       ├── tasks/
│       ├── tools/
│       ├── tests/
│       └── main.py            # API server entry
├── db/                        # Database files
├── requirements.txt           # Python dependencies
└── setup.py                   # Package configuration
```

## 🏗️ Architecture

### Service Integration
```
Client App → Firebase Functions → CrewAI Backend
     ↑              ↓
     └──── Firestore DB
```

### API Endpoints
- **Content Approval Flow**
  ```
  POST /api/content/approve
  {
    "userId": "string",
    "gistId": "string",
    "gistData": {
      "link": "string",
      // other gist properties
    }
  }
  ```

### Production Workflow
1. Firebase Functions receives gist update request
2. Updates gist status in Firestore
3. Triggers CrewAI content approval workflow
4. CrewAI processes content and returns results
5. Status updates reflected in Firestore

## 🚀 Getting Started

### What You'll Need

- Python 3.11 or newer
- API keys for:
  - OpenAI (for AI processing)
  - ElevenLabs (for voice generation)
  - SerperDev (for research capabilities)

### Quick Setup

1. Clone and enter the project:
```bash
git clone <repository-url>
cd CrewAI
```

2. Set up your environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create your `.env` file:
```env
OPENAI_API_KEY=your-key-here
ELEVENLABS_API_KEY=your-key-here
SERPER_API_KEY=your-key-here
```

### Additional Requirements
- Flask server for API endpoints
- Network access for Firebase Functions

### Environment Setup
```env
# Add to existing .env
CREW_AI_BASE_URL=http://localhost:5000  # For local development
```

### Running the API Server
```bash
python main.py  # Starts Flask server on port 5000
```

## 🔧 Main Features

### 1. Smart Research System
- Searches multiple sources (Wikipedia, academic papers, news)
- Verifies information across different sources
- Handles technical documentation and dictionary lookups

### 2. Content Processing
- Analyzes documents and extracts key points
- Structures content for podcast format
- Creates natural Q&A segments

### 3. Voice Generation
- Creates natural-sounding conversations
- Supports multiple voice roles (host, expert)
- Maintains consistent voice quality across segments

### 4. Content Approval API
- Receives requests from Firebase Functions
- Processes content through AI teams
- Returns approval status and results

## 🎯 Use Cases

1. **Content Transformation**
   - Turn research papers into engaging podcasts
   - Convert technical documents into educational content
   - Transform articles into interview-style discussions

2. **Research and Verification**
   - Gather comprehensive information on topics
   - Fact-check and verify claims
   - Compile technical documentation

3. **Audio Content Creation**
   - Generate professional voiceovers
   - Create interview-style content
   - Produce educational podcasts

## 🛠️ Customization

### Adding New Capabilities
The system is designed to be easily extended. You can add:
- New research sources
- Custom processing tools
- Specialized voice configurations

### Firebase Integration
- Configurable endpoints
- Custom status updates
- Flexible workflow triggers

## 📈 Future Plans

- Additional voice customization options
- More research sources integration
- Enhanced content processing capabilities
- Improved audio production features

## 🤝 Contributing

We welcome contributions! Whether it's:
- Adding new features
- Improving documentation
- Fixing bugs
- Suggesting enhancements

Please feel free to submit pull requests or open issues.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- CrewAI framework
- ElevenLabs for voice generation
- SerperDev for research capabilities
- OpenAI for AI processing 