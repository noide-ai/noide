import asyncio

import config
from api import run_api
from services.github import GitHubApp
from services.ai.ai_logic import IssueSolver


def setup_infrastructure():
    with open(config.GITHUB_APP_PRIVATE_KEY_PEM_PATH) as f:
        private_key = f.read()
    GitHubApp.setup(config.GITHUB_CLIENT_ID, private_key)

    with open(config.OPENAI_API_KEY) as f:
        openai_api_key = f.read()
    IssueSolver.setup(openai_api_key)



async def main() -> None:
    setup_infrastructure()

    await run_api(
        host=config.APP_HOST,
        port=config.APP_PORT
    )


if __name__ == "__main__":
    asyncio.run(main())
