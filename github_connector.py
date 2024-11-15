from github import Github


URL = "https://d97c-141-255-132-132.ngrok-free.app/github/webhook"


class GithubConnector:
    DEFAULT_EVENTS = [
        "pull_request",
        "pull_request_review",
        "pull_request_review_comment",
        "pull_request_review_thread",
    ]

    def __init__(self, token: str):
        self.github = Github(token)

    def create_webhook(self, repo_name: str):
        repo = self.github.get_user().get_repo(repo_name)
        repo.create_hook(
            "web", self._get_webhook_config(), self.DEFAULT_EVENTS, active=True
        )

    def _get_webhook_config(self):
        return {"url": URL, "content_type": "json"}
