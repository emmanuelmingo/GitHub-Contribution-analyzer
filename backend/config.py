from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).parent.parent / ".env")

BaseUrl = os.getenv("BaseURL")

FRONTEND_ORIGINS = [url for url in [
    os.getenv("DEV_FRONTEND_URL"),
    os.getenv("FRONTEND_URL"),
] if url]

CACHE_CONFIG = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 3600,
}
