import os
from dotenv import load_dotenv
load_dotenv()

EURI_API_KEY = os.getenv("EURI_API_KEY")
EURI_BASE_URL = "https://api.euron.one/api/v1/euri"
EURI_API_URL = "https://api.euron.one/api/v1/euri/chat/completions"
MODEL_NAME = "gpt-4.1-mini"
DATABASE_URI = os.getenv("DATABASE_URI")
if DATABASE_URI and DATABASE_URI.startswith("postgresql://"):
    DATABASE_URI = DATABASE_URI.replace("postgresql://", "postgresql+psycopg2://", 1)