import time

import httpx

from . import _utils


class GitHubApp:
    _app_id: str | None = None
    _jwt_token: str | None = None

    @classmethod
    def setup(cls, app_id: str, private_key: str) -> None:
        cls._app_id = app_id
        cls._private_key = private_key

    @classmethod
    async def get_installation_access_token(cls, installation_id: str) -> str:
        headers = {
            "Authorization": f"Bearer {cls._get_jwt()}",
            "Accept": "application/vnd.github+json"
        }
        url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers)
            return response.json()["token"]

    @classmethod
    def _get_jwt(cls) -> str:
        if not cls._jwt_token or _utils.jwt_is_valid(cls._jwt_token):
            cls._generate_jwt()
        return cls._jwt_token

    @classmethod
    def _generate_jwt(cls):
        payload = {
            # issued at time
            'iat': int(time.time()),
            # JWT expiration time (10 minutes max)
            'exp': int(time.time()) + (10 * 60),
            # GitHub App's identifier
            'iss': cls._app_id
        }
        cls._jwt_token = _utils.generate_jwt(payload, cls._private_key)
