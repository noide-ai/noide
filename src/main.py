import asyncio

import config
from api import run_api


async def main() -> None:
    await run_api(
        host=config.APP_HOST,
        port=config.APP_PORT
    )


if __name__ == "__main__":
    asyncio.run(main())
