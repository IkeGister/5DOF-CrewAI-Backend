Gista: Your AI Podcast Creation Assistant 🎙️

Turn any document into an engaging podcast with our AI-powered system! Gista works like having a full podcast production team at your fingertips.

✨ What It Does
Imagine having:
A research team that digs deep into your topic
A content writer that turns complex info into engaging scripts
Professional voice actors ready to bring your content to life
All working together automatically!

🎯 Perfect For
Content Creators wanting to turn articles into podcasts
Educators making learning materials more engaging
Researchers sharing findings in an accessible way
Anyone looking to transform written content into audio format

🔥 Cool Features
Smart Research: Automatically checks Wikipedia, news, and academic sources
Natural Conversations: Creates engaging Q&A segments
Professional Voices: Uses ElevenLabs for realistic voice generation
Quality Control: Fact-checks and verifies all information

🚀 Quick Start
Get your API keys (OpenAI, ElevenLabs, SerperDev)
Install Python 3.11+
Set up the project
Start creating podcasts!

🔧 Environment Setup & Deployment
1. **Local Environment Setup**
   - Create a `.env` file in the root directory with your API keys:
     ```
     SERVICE_API_KEY=your_service_api_key
     CREW_AI_API_KEY=your_openai_api_key
     CREW_AI_BASE_URL=https://api.openai.com/v1
     ```

2. **Firebase Deployment**
   - Navigate to the `firebase` directory
   - Copy `firebase.json.template` to `firebase.json` and add your actual API keys:
     ```
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
           "npm --prefix \"$RESOURCE_DIR\" run lint",
           "npm --prefix \"$RESOURCE_DIR\" run build"
         ],
         "gen": 2,
         "environmentVariables": {
           "SERVICE_API_KEY": "your_service_api_key",
           "CREW_AI_API_KEY": "your_openai_api_key",
           "CREW_AI_BASE_URL": "https://api.openai.com/v1"
         }
       }
     }
     ```
   - Build and deploy: `npm --prefix functions run build && firebase deploy --only functions`
   - Access your API at the provided URL with the header `X-API-Key: your_service_api_key`

3. **Security Note**
   - Both `.env` and `firebase.json` contain sensitive API keys
   - These files are added to `.gitignore` to prevent committing sensitive information
   - Always use the template files for version control and add actual keys only in your local environment

🎉 The Result

Get professional-quality podcasts featuring:

A host asking insightful questions
An expert giving detailed answers
Natural-sounding conversations
Well-researched, accurate content
Want to learn more? Check out our detailed documentation in the project repository!
---
Built with ❤️ using CrewAI, ElevenLabs, and OpenAI
