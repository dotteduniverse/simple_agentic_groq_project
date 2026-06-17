import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Groq
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    # Agent
    MAX_ITERATIONS: int = int(os.getenv("MAX_ITERATIONS", "5"))
    
    # Code Tool
    CODE_TIMEOUT: int = int(os.getenv("CODE_TIMEOUT", "5"))
    
    # Optional: Fallback models, etc.
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq")  # supports 'groq' or 'openai'
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

settings = Settings()