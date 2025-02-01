# CrewAI Backend System

A modular and extensible AI system built with CrewAI that demonstrates multi-agent collaboration. This system uses teams of AI agents to perform various tasks including content generation, travel guidance, and ticket searching.

## Project Structure 

```
CrewAI/
├── agents/
│   └── agents.py         # Agent definitions
├── config/
│   ├── llm_config.py     # LLM provider configuration
│   ├── settings.py       # Global settings
│   └── topics.py         # Topic configuration
├── tasks/
│   └── crewAI_tasks.py   # Task definitions
├── tests/
│   ├── test_llm_config.py
│   ├── test_multiAgent_toolUse.py
│   └── test_travelGuide_agents.py
├── tools/
│   ├── content_gen_tools.py
│   ├── ticket_search_tool.py
│   └── travel_guide_tool.py
├── utils/
│   └── api_keys.py       # API key management
├── .env                  # Environment variables
├── .gitignore
├── crew_ai.pyi
├── directories.py
├── main.py              # Main application entry point
├── README.md            # Project documentation
└── requirements.txt     # Project dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Virtual environment (recommended)

### Installation

1. Clone the repository and navigate to the project directory:
```bash
git clone <repository-url>
cd CrewAI
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your API keys:
```
OPENAI_API_KEY=your-openai-key-here
HUGGINGFACE_API_TOKEN=your-huggingface-token
MISTRAL_API_KEY=your-mistral-key
COHERE_API_KEY=your-cohere-key
```

### Running the Application

Run the application via command line:
```bash
python main.py
```

## 🔧 Features

### 1. Multiple Tool Support

The system includes various specialized tools:
- Content Generation Tools (`tools/content_gen_tools.py`)
- Travel Guide Tool (`tools/travel_guide_tool.py`)
- Ticket Search Tool (`tools/ticket_search_tool.py`)

### 2. Multiple LLM Support (`config/llm_config.py`)

Support for various LLM providers:
- OpenAI (default)
- HuggingFace
- Mistral
- Cohere

### 3. Testing

Available test suites:
```bash
python -m unittest tests/test_llm_config.py
python -m unittest tests/test_multiAgent_toolUse.py
python -m unittest tests/test_travelGuide_agents.py
```

## 🔧 Component Overview

### 1. Agents (`agents/agents.py`)

The system uses specialized agents for different tasks:
- Travel guide agents
- Content generation agents
- Tool usage agents

### 2. Tasks (`tasks/crewAI_tasks.py`)

Tasks define the work each agent needs to perform. Each task includes:
- A detailed description
- Expected output format
- Assigned agent

### 3. Configuration (`config/`)

The config directory contains:
- `llm_config.py`: LLM provider configurations
- `settings.py`: Global settings
- `topics.py`: Topic configurations

### 4. Tools (`tools/`)

Specialized tools for different functionalities:
- Content generation
- Travel guidance
- Ticket searching

## 🔄 Workflow

1. **Initialization**:
   - Load configuration
   - Initialize agents
   - Set up tasks

2. **Execution**:
   - Agents perform assigned tasks
   - Tools are utilized as needed
   - Results are processed

3. **Output**:
   - Task-specific output
   - Execution logs (if verbose)

## 🛠️ Customization and Extension

### Adding New Tools

1. Create new tool files in `tools/`:
```python
def create_custom_tool():
    # Tool implementation
    pass
```

### Creating New Tasks

1. Add new task definitions in `tasks/crewAI_tasks.py`:
```python
def create_custom_task(agent):
    custom_task = Task(
        description="Custom task description",
        expected_output="Expected output format",
        agent=agent
    )
    return custom_task
```

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Docker Deployment

1. Create a Dockerfile:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

2. Build and run:
```bash
docker build -t crewai-backend .
docker run -e OPENAI_API_KEY=your-key crewai-backend
```

## 📝 Logging and Monitoring

Enable verbose logging in the Crew initialization:
```python
crew = Crew(
    agents=[...],
    tasks=[...],
    verbose=2  # 0=minimal, 1=basic, 2=detailed
)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 