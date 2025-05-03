from fastapi import APIRouter, Request, Header, HTTPException

from api.schemas import OkResponse
from services.github import GitHubApp

router = APIRouter(tags=["GitHub"])


@router.post(
    "/github/webhook",
    response_model=OkResponse
)
async def handle_github_webhook(
    request: Request,
    x_github_event: str | None = Header(None)
):
    if not x_github_event:
        raise HTTPException(status_code=400, detail="Missing X-GitHub-Event header")

    body = await request.json()
    installation_id = body.get("installation", {}).get("id")

    if not installation_id:
        raise HTTPException(status_code=400, detail="Missing installation.id in payload")

    gh_access_token = await GitHubApp.get_installation_access_token(installation_id)
    print(gh_access_token)

    return OkResponse()
