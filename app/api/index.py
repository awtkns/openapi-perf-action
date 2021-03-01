from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

from _github import login_as_installation

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
