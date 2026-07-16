import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

class Settings:
    # --- GCP CONFIG ---
    PROJECT_ID = os.getenv("PROJECT_ID", "enterprise-agentic-rag")
    LOCATION = os.getenv("LOCATION", "us-central1")
    GCP_DOC_AI_LOCATION = os.getenv("GCP_DOC_AI_LOCATION", "us")
    GCP_DOC_AI_PROCESSOR_ID = os.getenv("GCP_DOC_AI_PROCESSOR_ID")
    RAW_BUCKET = os.getenv("GCP_RAW_BUCKET", " advanced-rag-raw")
    PROCESSED_BUCKET = os.getenv("GCP_PROCESSED_BUCKET", " advanced-rag-processed")


    # --- PORTKEY CONFIG ---
    PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY")
    PORTKEY_CONFIG_ID = os.getenv("PORTKEY_CONFIG_ID", "")

    # --- VECTOR DB (QDRANT) ---
    QDRANT_URL = os.getenv("QDRANT_CLUSTER_ENDPOINT")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION = "enterprise-agentic-rag"

    # --- REASONING ENGINE (GROQ) ---
    # --- GROQ CONFIG ---
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_FALLBACK_API_KEY = os.getenv("GROQ_FALLBACK_API_KEY")
    GROQ_SLUG = os.getenv("GROQ_SLUG", "enterprise-agentic-rag-slug")
    GROQ_SLUG_FALLBACK = os.getenv("GROQ_SLUG_FALLBACK", "enterprise-agentic-rag-slug-fallback")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    GROQ_MODEL_FALLBACK = os.getenv("GROQ_MODEL_FALLBACK", "openai/gpt-oss-120b")

    # --- DATABASE & CACHE ---
    DB_USER = os.getenv("DB_USER", "rag_admin")
    DB_PASS = os.getenv("DB_PASS")
    DB_NAME = os.getenv("DB_NAME", "rag_memory")
    DB_CONNECTION_NAME = os.getenv("DB_CONNECTION_NAME")
    
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT", "6379")

    # --- ENVIRONMENT MODE ---
    # Set to "true" in your local .env to bypass Cloud SQL/Redis
    LOCAL_MODE = os.getenv("LOCAL_MODE", "false").lower() == "true"

    # --- OBSERVABILITY ---
    LOGFIRE_TOKEN = os.getenv("LOGFIRE_TOKEN")
    LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "true")
    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
    LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "")
    LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")


        # --- Evals ---
    JUDGE_GROQ = os.getenv("judge_groq")

# Apply LangChain environment variables for automatic tracing
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGSMITH_TRACING", "true")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "")
os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")


settings = Settings()