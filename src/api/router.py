from fastapi import APIRouter, Request, Header, HTTPException

from api.schemas import OkResponse
from . import _utils


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

    print(x_github_event)

    body = await request.json()
    action = body.get("action")
    if x_github_event == "issues" and action == "opened":
        await _utils.solve_issue(body)

    elif x_github_event == "issue_comment" and (action == "created" or body.get("action") == "edited"):
        comment = body.get("comment", {}).get("body", "")
        if comment.startswith("aisolve"):
            await _utils.solve_issue(body)
        elif comment.startswith("aisuggest"):
            pass

    return OkResponse()
