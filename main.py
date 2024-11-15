from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post("/github/webhook")
def github_webhook(request: Request) :
    event = request.json()
    print(event)
    return {"message", "ok"}


