from os import environ

OPEN_API_ENDPOINT = environ.get('INPUT_OPENAPI-ENDPOINT', "Could not find endpoint")

if __name__ == '__main__':
    print(environ)
    print(OPEN_API_ENDPOINT)
