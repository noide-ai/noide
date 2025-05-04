import os

import dotenv


dotenv.load_dotenv()


APP_HOST: str = os.getenv("APP_HOST", "localhost")
APP_PORT: int = int(os.getenv("APP_PORT", "8000"))

GITHUB_CLIENT_ID: str = os.getenv("GITHUB_CLIENT_ID")
GITHUB_APP_PRIVATE_KEY_PEM_PATH: str = os.getenv("GITHUB_APP_PRIVATE_KEY_PEM_PATH")

OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

AI_MODEL = "o4-mini-high"

REDIS_URL: str | None = os.getenv("REDIS_URL")
