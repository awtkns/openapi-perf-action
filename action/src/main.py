import json
from io import BytesIO
from os import environ
from uuid import uuid4

import requests as r
from openapi_perf import OpenAPIPerf

from firebase import firestore

OPEN_API_ENDPOINT = environ.get('INPUT_OPENAPI-ENDPOINT', "http://crudrouter:5000")
APP_ENDPOINT = 'https://api.openapi-perf.awtkns.com'

GITHUB_ACTOR = environ.get('GITHUB_ACTOR', '')
GITHUB_WORKSPACE = environ.get('GITHUB_WORKSPACE', '/out')

print(environ)
print("WORKSPACE", GITHUB_WORKSPACE)

# TODO: Place this infinite loop safeguard in action yml so we don't'
if '[bot]' in GITHUB_ACTOR:
    print("[SKIPPING] Bot cannot trigger as safeguard")
    exit(0)


with open(environ.get('GITHUB_EVENT_PATH')) as fp:
    GITHUB_EVENT = json.load(fp)


def fig_to_base64(figure):
    plt_bytes = BytesIO()
    figure.savefig(plt_bytes, format='png')
    plt_bytes.seek(0)

    return plt_bytes


def action_factory(content: str) -> dict:
    return {
        'content': content,
        'owner': GITHUB_EVENT['repository']['owner']['login'],
        'repository': GITHUB_EVENT['repository']['name'],
        'pr_number': GITHUB_EVENT['issue']['number']
    }


if __name__ == '__main__':
    res = r.post(
        url=f'{APP_ENDPOINT}/reaction',
        json=action_factory('eyes')
    )
    assert res.status_code == 200, "Could not React to action"

    op = OpenAPIPerf(OPEN_API_ENDPOINT)
    results = op.run()
    results.to_csv(GITHUB_WORKSPACE + "/results.csv")

    fig = results.plot(show=False)
    file = fig_to_base64(fig)

    url = f'charts/{uuid4().hex}'
    img = firestore.child(url).put(file)

    comment = f'<p align="center"><img src="{firestore.child(url).get_url("")}"></p>'
    res = r.post(
        url=f'{APP_ENDPOINT}/comment',
        json=action_factory(comment)
    )

    assert res.status_code == 200, "Could not upload Performance report"
