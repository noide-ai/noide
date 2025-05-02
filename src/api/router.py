from fastapi import APIRouter, Request, Header


router = APIRouter(tags=["GitHub"])


@router.post(
    "/github/webhook"
)
async def handle_github_webhook(
    request: Request,
    x_github_event: str | None = Header(None)
):
    print(x_github_event)
    print(await request.body())
    return {
        "message": "ok"
    }
