import json

from os import environ

OPEN_API_ENDPOINT = environ.get('INPUT_OPENAPI-ENDPOINT', "Could not find endpoint")
GITHUB_EVENT_PATH = environ.get('GITHUB_EVENT_PATH')

with open(GITHUB_EVENT_PATH) as fp:
    print(json.load(fp))

print(environ)
print(OPEN_API_ENDPOINT)
