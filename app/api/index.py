import os

from fastapi import FastAPI, HTTPException
from github3.exceptions import NotFoundError, ForbiddenError
from github3.github import GitHub
from github3.pulls import PullRequest
from pydantic import BaseModel

GITHUB_PRIVATE_KEY = os.environ.get('APP_PRIVATE_KEY', None)
GITHUB_APP_IDENTIFIER = os.environ.get('APP_IDENTIFIER', None)

if not GITHUB_PRIVATE_KEY:
    GITHUB_PRIVATE_KEY = open('private-key.pem', 'rt').read()

app = FastAPI()


class ActionIn(BaseModel):
    content: str
    owner: str
    repository: str
    pr_number: int

    @property
    def repo(self) -> str:
        return f'{self.owner}/{self.repository}'


@app.post('/api/')
def matrix(action: ActionIn):
    gh = login_as_installation(action)
    get_pr(gh, action).create_comment(action.content)
    return "Post Success", 200


@app.post('/api/reaction')
def matrix(action: ActionIn):
    gh = login_as_installation(action)
    issue = get_pr(gh, action).issue()

    issue._post(
        issue._api + '/reactions',
        data={"content": 'eyes'},
        headers={'Accept': 'application/vnd.github.squirrel-girl-preview+json'}
    )

    return "Post Success", 200


def login_as_installation(action: ActionIn):
    try:
        gh = GitHub()
        gh.login_as_app(GITHUB_PRIVATE_KEY.encode(), GITHUB_APP_IDENTIFIER)

        install = gh.app_installation_for_repository(action.owner, action.repository)
        gh.login_as_app_installation(
            GITHUB_PRIVATE_KEY.encode(),
            GITHUB_APP_IDENTIFIER,
            install.id
        )

        return gh
    except NotFoundError:
        raise HTTPException(404, f"OpeAPI Perf App not installed to {action.repo}")


def get_pr(gh, action: ActionIn) -> PullRequest:
    try:
        return gh.pull_request(
            owner=action.owner,
            repository=action.repository,
            number=action.pr_number
        )
    except ForbiddenError:
        raise HTTPException(403, f"Application not setup for the repository {action.repo}")
    except NotFoundError:
        raise HTTPException(404, f"PR #{action.pr_number} does not exist in {action.repo}")
