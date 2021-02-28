import os

from flask import Flask, jsonify
from github3.github import GitHub


GITHUB_PRIVATE_KEY = os.environ['APP_PRIVATE_KEY']
GITHUB_APP_IDENTIFIER = "102603"
app = Flask(__name__)


@app.route('/api/')
def matrix():
    gh = GitHub()

    # Login as app
    gh.login_as_app(GITHUB_PRIVATE_KEY.encode(), GITHUB_APP_IDENTIFIER)

    # This could potentially break
    installations = [installation.id for installation in gh.app_installations()]
    gh.login_as_app_installation(GITHUB_PRIVATE_KEY.encode(), GITHUB_APP_IDENTIFIER, installations[0])

    issue = gh.pull_request(owner='awtkns', repository='openapi-perf-action', number=1)
    issue.create_comment('Comment from serverless flask')

    return jsonify("Oke")
