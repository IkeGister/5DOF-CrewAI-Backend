"""
Gista General Tools Module
=========================

Collection of tool combinations specifically designed for Gista tasks.
Each tool includes specialized website-specific research capabilities
and podcast generation tools.
"""

from crewai_tools import BaseTool
from crewai_tools import (
    SerperDevTool,
    ScrapeWebsiteTool,
    WebsiteSearchTool,
    CSVSearchTool,
    DOCXSearchTool,
    PDFSearchTool,
    DirectoryReadTool
)
from typing import List, Optional, Type, Dict, ClassVar, Any
from pydantic.v1 import BaseModel, Field

# Import Gista-specific tools
from .script_parser_tool import ScriptParserTool
from .transcription_tool import TranscriptionTool
from .elevenLabs_voiceover_tool import ElevenLabsVoiceoverTool

# Base Schema
class WebResearchSchema(BaseModel):
    """Base schema for web research tools"""
    query: str = Field(..., description="Search query")
    max_results: int = Field(default=5, description="Maximum number of results to return")
    language: str = Field(default="en", description="Language for results")

    class Config:
        orm_mode = True

# Specialized Research Tools
class WikipediaResearchTool(BaseTool):
    """Specialized tool for Wikipedia research"""
    name: str = "Wikipedia Research Tool"
    description: str = "Searches and extracts information from Wikipedia"
    args_schema: Type[BaseModel] = WebResearchSchema
    base_url: str = "https://wikipedia.org"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize with fixed URLs for Wikipedia
        self._scraper = ScrapeWebsiteTool()
        self._web_search = WebsiteSearchTool(website=self.base_url)

    def _run(self, query: str, max_results: int = 5, language: str = "en") -> dict:
        """Search Wikipedia and extract relevant information"""
        wiki_url = f"https://{language}.wikipedia.org/wiki/"
        search_results = self._web_search._run(
            search_query=f"site:wikipedia.org {query}"
        )
        
        detailed_content = {}
        for url in search_results[:max_results]:
            if wiki_url in url:
                content = self._scraper._run(website_url=url)
                detailed_content[url] = content

        return {
            "search_results": search_results,
            "detailed_content": detailed_content
        }

class DictionaryTool(BaseTool):
    """Tool for dictionary lookups using multiple sources"""
    name: str = "Dictionary Tool"
    description: str = "Looks up terms in various dictionaries"
    args_schema: Type[BaseModel] = WebResearchSchema
    
    DICTIONARY_SOURCES: ClassVar[Dict[str, str]] = {
        "merriam_webster": "https://www.merriam-webster.com/dictionary/",
        "oxford": "https://www.lexico.com/definition/",
        "cambridge": "https://dictionary.cambridge.org/dictionary/english/"
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._scraper = ScrapeWebsiteTool()
        self._web_search = WebsiteSearchTool()

    def _run(self, query: str, max_results: int = 3, language: str = "en") -> dict:
        """
        Look up terms in multiple dictionaries
        """
        definitions = {}
        for source, base_url in self.DICTIONARY_SOURCES.items():
            try:
                url = f"{base_url}{query.lower().replace(' ', '-')}"
                content = self._scraper._run(website_url=url)
                definitions[source] = content
            except Exception as e:
                definitions[source] = f"Error: {str(e)}"

        return {"definitions": definitions}

class AcademicSearchTool(BaseTool):
    """Tool for academic and scholarly research"""
    name: str = "Academic Search Tool"
    description: str = "Searches academic sources and research papers"
    args_schema: Type[BaseModel] = WebResearchSchema
    
    ACADEMIC_SOURCES: ClassVar[Dict[str, str]] = {
        "google_scholar": "https://scholar.google.com",
        "semantic_scholar": "https://www.semanticscholar.org",
        "arxiv": "https://arxiv.org/search/"
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._serper_tool = SerperDevTool()
        self._web_search = WebsiteSearchTool()

    def _run(self, query: str, max_results: int = 5, language: str = "en") -> dict:
        """
        Search academic sources for scholarly content
        """
        results = {}
        for source in self.ACADEMIC_SOURCES:
            search_query = f"site:{self.ACADEMIC_SOURCES[source]} {query}"
            results[source] = self._serper_tool._run(search_query=search_query)

        return {"academic_results": results}

class TechnicalDocsTool(BaseTool):
    """Tool for searching technical documentation"""
    name: str = "Technical Documentation Tool"
    description: str = "Searches technical documentation and references"
    args_schema: Type[BaseModel] = WebResearchSchema
    
    TECH_SOURCES: ClassVar[Dict[str, str]] = {
        "stack_overflow": "https://stackoverflow.com/search?q=",
        "developer_mozilla": "https://developer.mozilla.org/en-US/search?q=",
        "github": "https://github.com/search?q=",
        "readthedocs": "https://readthedocs.org/search/?q="
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._web_search = WebsiteSearchTool()
        self._scraper = ScrapeWebsiteTool()

    def _run(self, query: str, max_results: int = 5, language: str = "en") -> dict:
        """
        Search technical documentation sources
        """
        tech_results = {}
        for source, base_url in self.TECH_SOURCES.items():
            search_results = self._web_search._run(
                search_query=f"site:{base_url} {query}"
            )
            tech_results[source] = search_results

        return {"technical_results": tech_results}

class NewsResearchTool(BaseTool):
    """Tool for news and current events research"""
    name: str = "News Research Tool"
    description: str = "Searches news sources for current information"
    args_schema: Type[BaseModel] = WebResearchSchema
    
    NEWS_SOURCES: ClassVar[Dict[str, str]] = {
        "reuters": "https://www.reuters.com",
        "ap_news": "https://apnews.com",
        "bbc": "https://www.bbc.com/news",
        "bloomberg": "https://www.bloomberg.com"
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._serper_tool = SerperDevTool()

    def _run(self, query: str, max_results: int = 5, language: str = "en") -> dict:
        """
        Search reputable news sources
        """
        news_results = {}
        for source in self.NEWS_SOURCES:
            search_query = f"site:{self.NEWS_SOURCES[source]} {query}"
            news_results[source] = self._serper_tool._run(search_query=search_query)

        return {"news_results": news_results}

class EnhancedWebSearchTool(BaseTool):
    """Enhanced web search tool with better error handling and formatting"""
    name: str = "Enhanced Web Search"
    description: str = "An advanced tool that searches the internet using Google Search API to find relevant information about any topic, with improved error handling and result formatting."
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._serper_tool = SerperDevTool()

    def _run(
        self,
        query: str,
        max_results: int = 5,
        **kwargs: Any,
    ) -> str:
        """
        Execute the web search with enhanced error handling and formatting
        
        Args:
            query: The search query
            max_results: Maximum number of results to return
            
        Returns:
            Formatted string containing search results or error message
        """
        try:
            # Use the base SerperDevTool to perform the search
            raw_results = self._serper_tool._run(search_query=query)
            
            # If we got an error message back
            if isinstance(raw_results, str) and "error" in raw_results.lower():
                return raw_results
                
            # Extract and format the results
            formatted_results = []
            result_lines = raw_results.split('\n')
            
            current_result = []
            for line in result_lines:
                if line.strip() == "---":
                    if current_result:
                        formatted_results.append('\n'.join(current_result))
                        current_result = []
                    if len(formatted_results) >= max_results:
                        break
                elif line.strip():
                    current_result.append(line)
            
            if not formatted_results:
                return f"No results found for query: {query}"
            
            return (
                f"\nTop {len(formatted_results)} search results for '{query}':\n\n" +
                "\n\n".join(formatted_results)
            )
            
        except Exception as e:
            return f"Error performing enhanced web search: {str(e)}"

# Updated GistaToolbox
class GistaToolbox:
    """Collection of all Gista research and podcast generation tools"""
    
    def __init__(self):
        # Research Tools
        self.wikipedia = WikipediaResearchTool()
        self.dictionary = DictionaryTool()
        self.academic = AcademicSearchTool()
        self.technical = TechnicalDocsTool()
        self.news = NewsResearchTool()
        self.web_search = EnhancedWebSearchTool()
        
        # Podcast Generation Tools
        self.script_parser = ScriptParserTool()
        self.transcription = TranscriptionTool()
        self.voiceover = ElevenLabsVoiceoverTool()
        
        # Content Extraction Tools
        self.web_scraper = ScrapeWebsiteTool()
        self.csv_reader = CSVSearchTool()
        self.docx_reader = DOCXSearchTool()
        self.pdf_reader = PDFSearchTool()
        self.directory_reader = DirectoryReadTool()

    def get_tool_by_task(self, task_type: str) -> Optional[BaseTool]:
        """Returns appropriate tool based on task type"""
        tool_mapping = {
            # Research tools
            "wikipedia": self.wikipedia,
            "dictionary": self.dictionary,
            "academic": self.academic,
            "technical": self.technical,
            "news": self.news,
            "web_search": self.web_search,
            
            # Podcast generation tools
            "script_parsing": self.script_parser,
            "transcription": self.transcription,
            "voiceover": self.voiceover,
            
            # Content Extraction Tools
            "web_scraper": self.web_scraper,
            "csv_reader": self.csv_reader,
            "docx_reader": self.docx_reader,
            "pdf_reader": self.pdf_reader,
            "directory_reader": self.directory_reader
        }
        return tool_mapping.get(task_type)

    def list_available_tools(self) -> Dict[str, List[str]]:
        """Returns list of available tools by category"""
        return {
            "research_tools": [
                "Wikipedia Research Tool",
                "Dictionary Tool",
                "Academic Search Tool",
                "Technical Documentation Tool",
                "News Research Tool",
                "Enhanced Web Search Tool"
            ],
            "podcast_tools": [
                "Script Parser Tool",
                "Transcription Tool",
                "ElevenLabs Voiceover Tool"
            ],
            "content_extraction_tools": [
                "Web Scraper Tool",
                "CSV Reader Tool",
                "DOCX Reader Tool",
                "PDF Reader Tool",
                "Directory Reader Tool"
            ]
        }

    def get_all_research_results(self, query: str, max_results: int = 3) -> Dict:
        """
        Perform research across all available research tools
        
        Args:
            query: Search query
            max_results: Maximum results per source
        """
        results = {}
        for tool_name, tool in {
            "wikipedia": self.wikipedia,
            "dictionary": self.dictionary,
            "academic": self.academic,
            "technical": self.technical,
            "news": self.news
        }.items():
            try:
                results[tool_name] = tool._run(query, max_results)
            except Exception as e:
                results[tool_name] = f"Error: {str(e)}"
        
        return results

    def process_podcast_script(
        self,
        script_content: str,
        generate_audio: bool = True,
        generate_transcript: bool = True
    ) -> Dict:
        """
        Process a podcast script through the available podcast tools
        
        Args:
            script_content: The markdown formatted podcast script
            generate_audio: Whether to generate audio using ElevenLabs
            generate_transcript: Whether to generate a transcript
            
        Returns:
            Dictionary containing processing results
        """
        results = {}
        
        try:
            # Parse script
            parsed_result = self.script_parser._run(script_content)
            results["parsed_script"] = parsed_result
            
            # Generate audio if requested
            if generate_audio:
                audio_segments = []
                for segment in parsed_result["segments"]:
                    audio = self.voiceover._run(
                        text=segment.text,
                        voice_role=segment.voice_role,
                        segment_type=segment.segment_type
                    )
                    audio_segments.append(audio)
                results["audio_segments"] = audio_segments
            
            # Generate transcript if requested
            if generate_transcript:
                transcript = self.transcription._run(
                    segments=parsed_result["segments"],
                    metadata={"segments": parsed_result["segments"]},
                    format_type="clean"
                )
                results["transcript"] = transcript
            
            return {
                "status": "success",
                "results": results
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
