from io import BytesIO
from os import environ
from uuid import uuid4

import numpy as np
from github import Github
from matplotlib import pyplot as plt

from firebase import firestore

OPEN_API_ENDPOINT = environ.get('INPUT_OPENAPI-ENDPOINT', "Could not find endpoint")
GITHUB_EVENT_PATH = environ.get('GITHUB_EVENT_PATH')
GITHUB_REPOSITORY = environ.get('GITHUB_REPOSITORY', 'awtkns/openapi-perf-action')
GITHUB_TOKEN = '5e08c76b14518173d67210d4838012007a1ea1fd'



def fig_to_base64():
    plt_bytes = BytesIO()
    plt.savefig(plt_bytes, format='png')
    plt_bytes.seek(0)
    plt.close()

    return plt_bytes


if __name__ == '__main__':
    x1 = np.linspace(0.0, 5.0)
    x2 = np.linspace(0.0, 2.0)

    y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
    y2 = np.cos(2 * np.pi * x2)

    plt.subplot(2, 1, 1)
    plt.plot(x1, y1, 'o-')
    plt.title('A tale of 2 subplots')
    plt.ylabel('Damped oscillation')

    plt.subplot(2, 1, 2)
    plt.plot(x2, y2, '.-')
    plt.xlabel('time (s)')
    plt.ylabel('Undamped')

    file = fig_to_base64()

    url = f'charts/{uuid4().hex}'
    img = firestore.child(url).put(file)

    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(GITHUB_REPOSITORY)
    pr = repo.get_pull(1)
    pr.create_issue_comment(
        'Performance Report\n---\n' +
        f'<p align="center"><img src="{firestore.child(url).get_url("")}"></p>'
    )




