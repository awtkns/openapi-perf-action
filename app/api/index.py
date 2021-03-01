import os

from flask import Flask, jsonify, request
from github3.github import GitHub


GITHUB_PRIVATE_KEY = os.environ.get('APP_PRIVATE_KEY', '')
GITHUB_APP_IDENTIFIER = os.environ.get('APP_IDENTIFIER', '')
app = Flask(__name__)


@app.route('/api/', methods=['POST'])
def matrix():
    data = request.get_json()
    content = data['content']
    owner = data['owner']
    repository = data['repository']
    pr_number = data['pr_number']

    gh = GitHub()

    # Login as app
    gh.login_as_app(GITHUB_PRIVATE_KEY.encode(), GITHUB_APP_IDENTIFIER)

    # TODO: Make sure this is valid.
    installations = [installation.id for installation in gh.app_installations()]
    gh.login_as_app_installation(GITHUB_PRIVATE_KEY.encode(), GITHUB_APP_IDENTIFIER, installations[0])

    issue = gh.pull_request(owner=owner, repository=repository, number=pr_number)
    issue.create_comment(content)

    return jsonify("Post Success"), 200


if __name__ == '__main__':
    gh = GitHub()
    print(gh.meta())
