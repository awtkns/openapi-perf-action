from os import environ

OPEN_API_ENDPOINT = environ.get('INPUT_OPEN-ENDPOINT', "Could not find endpoint")

print(OPEN_API_ENDPOINT)
