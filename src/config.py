import os

import dotenv


dotenv.load_dotenv()


APP_HOST: str = os.getenv("APP_HOST", "localhost")
APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
