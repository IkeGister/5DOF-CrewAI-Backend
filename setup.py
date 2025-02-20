from setuptools import setup, find_packages

setup(
    name="crewai-backend",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "crewai==0.28.8",
        "crewai_tools==0.1.6",
        "langchain_community==0.0.29",
        "python-dotenv==1.0.0",
        "huggingface_hub==0.20.3",
        "cohere==4.47",
        "unittest2==1.1.0",
        "notebook==7.1.0",
        "openai>=1.3.0",
        "langchain>=0.1.0"
    ]
) 