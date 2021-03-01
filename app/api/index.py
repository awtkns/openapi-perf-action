import os

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from github3.github import GitHub
from github3.exceptions import NotFoundError, ForbiddenError

GITHUB_PRIVATE_KEY = os.environ.get('APP_PRIVATE_KEY', open('private-key.pem', 'rt').read())
GITHUB_APP_IDENTIFIER = os.environ.get('APP_IDENTIFIER')

app = FastAPI()


def login_as_installation(account: str):
    gh = GitHub()
    gh.login_as_app(GITHUB_PRIVATE_KEY.encode(), GITHUB_APP_IDENTIFIER)

    for install in gh.app_installations():
        if install.account['login'] == account:
            gh.login_as_app_installation(
                GITHUB_PRIVATE_KEY.encode(),
                GITHUB_APP_IDENTIFIER,
                install.id
            )
            return gh

    raise HTTPException(status_code=403, detail="App Installation not found")


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
    gh = login_as_installation(action.owner)

    try:
        gh.pull_request(
            owner=action.owner,
            repository=action.repository,
            number=action.pr_number
        ).create_comment(action.content)
    except ForbiddenError:
        raise HTTPException(403, f"Application not setup for the repository {action.repo}")
    except NotFoundError:
        raise HTTPException(404, f"PR #{action.pr_number} does not exist in {action.repo}")

    return "Post Success", 200
