import os

import dotenv


dotenv.load_dotenv()


APP_HOST: str = os.getenv("APP_HOST", "localhost")
APP_PORT: int = int(os.getenv("APP_PORT", "8000"))

OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
