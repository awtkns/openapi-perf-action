import os

from github3.github import GitHub
from github3.exceptions import NotFoundError, ForbiddenError

GITHUB_PRIVATE_KEY = os.environ.get('APP_PRIVATE_KEY', None)
GITHUB_APP_IDENTIFIER = os.environ.get('APP_IDENTIFIER', None)

if not GITHUB_PRIVATE_KEY:
    GITHUB_PRIVATE_KEY = open('private-key.pem', 'rt').read()


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
