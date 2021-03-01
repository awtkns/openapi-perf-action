import json
from io import BytesIO
from os import environ
from uuid import uuid4

import numpy as np
import requests as r
from matplotlib import pyplot as plt

from firebase import firestore

OPEN_API_ENDPOINT = environ.get('INPUT_OPENAPI-ENDPOINT', "Could not find endpoint")
APP_ENDPOINT = 'https://api.openapi-perf.awtkns.com'

GITHUB_EVENT_PATH = environ.get('GITHUB_EVENT_PATH')
GITHUB_REPOSITORY = environ.get('GITHUB_REPOSITORY', 'awtkns/openapi-perf-action')
GITHUB_ACTOR = environ.get('GITHUB_ACTOR', '')

# TODO: Place this infinite loop safeguard in action yml so we don't'
if '[bot]' in GITHUB_ACTOR:
    print("skipping as bot")


print(environ)
import json
with open(GITHUB_EVENT_PATH) as fp:
    print(json.load(fp))


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

    comment = f'Performance Report\n---\nFrom a serverless function!\n<p align="center"><img src="{firestore.child(url).get_url("")}"></p>'

    res = r.post(
        url=f'{APP_ENDPOINT}/comment',
        json=action_factory(comment)
    )

    assert res.status_code == 200, "Could not upload Performance report"
