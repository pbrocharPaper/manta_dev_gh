from typing import Annotated
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse, Response
from github_connector import GithubConnector
from settings import get_settings, Settings
from github.GithubException import GithubException

app = FastAPI()


# Create healthcheck endpoint
@app.get("/healthcheck")
async def healthcheck():
    return {"message": "ok"}


@app.post("/webhook/{repo_name}")
async def webhook(repo_name: str, settings: Annotated[Settings, Depends(get_settings)]):
    try:
        GithubConnector(settings.GITHUB_API_KEY).create_webhook(repo_name)
        return JSONResponse(content={"message": "Webhook created"}, status_code=201)
    except GithubException as e:
        return JSONResponse(
            content={"message": f"Error creating webhook: {e.data}"}, status_code=500
        )


@app.post("/github/webhook")
async def github_webhook(request: Request) -> Response:
    event = await request.json()
    header = request.headers
    event_type = header.get("x-github-event")
    if event_type != "pull_request":
        return Response(status_code=200)

    pull_request = event.get("pull_request")
    action = event.get("action")
    url = pull_request.get("_links").get("html").get("href")
    login = pull_request.get("user").get("login")
    pr_title = pull_request.get("title")
    pr_body = pull_request.get("body")
    state = pull_request.get("state")
    requested_reviewers = pull_request.get("requested_reviewers")
    base = pull_request.get("base").get("ref")
    head = pull_request.get("head").get("ref")
    print(f"PR is {action}")
    print(f"PR url: {url}")
    print(f"PR {head} -> {base}")
    print(f"PR title: {pr_title}")
    print(f"PR body: {pr_body}")
    print(f"PR user: {login}")
    print(f"PR status: {state}")
    print(f"PR reviewers: {requested_reviewers}")

    return Response(status_code=200)
