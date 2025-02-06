# CrewAI Backend System

A sophisticated AI system that works like a well-coordinated team, handling tasks from content analysis to podcast creation. Think of it as having a group of AI specialists working together, each bringing their unique skills to the table.

## 🌟 What Makes This Special

- **Smart Content Processing**: Turns complex documents into engaging podcast content
- **Research Power**: Uses multiple specialized tools to gather and verify information
- **Voice Generation**: Creates natural-sounding conversations using ElevenLabs technology
- **Flexible & Expandable**: Easy to add new capabilities as needed

## 🏗️ Project Structure

```
CrewAI/
├── agents/              # The AI team members
├── tasks/              # What each team member does
├── tools/              # Tools the team uses
│   ├── gista_tools/    # Specialized podcast creation tools
│   └── content_tools/  # General content handling tools
└── config/             # System settings
```

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
 ok
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

### Running the System

```bash
python main.py
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