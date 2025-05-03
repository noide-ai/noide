import asyncio

import config
from api import run_api
from services.github import GitHubApp
from services.ai.engine import IssueSolver
from cache import Cache


def setup_infrastructure():
    with open(config.GITHUB_APP_PRIVATE_KEY_PEM_PATH) as f:
        private_key = f.read()
    GitHubApp.setup(config.GITHUB_CLIENT_ID, private_key)

    IssueSolver.setup(config.OPENAI_API_KEY)

    if config.REDIS_URL:
        print("Cache enabled")
        Cache.setup(config.REDIS_URL)


async def main() -> None:
    setup_infrastructure()

    await run_api(
        host=config.APP_HOST,
        port=config.APP_PORT
    )


if __name__ == "__main__":
    asyncio.run(main())
