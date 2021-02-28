"""
Major creds to https://stackoverflow.com/questions/57217162/issue-with-jwt-token-authentication-in-pygithub
Spend hours trying library after library
"""

import time

import github3
import jwt

PRIVATE_KEY_PATH = 'private_key.pem'


def get_jwt(app_id):
    with open(PRIVATE_KEY_PATH, "rt") as fp:
        pem_file = fp.read()

    return jwt.encode({
        "iat": int(time.time()),
        "exp": int(time.time()) + (10 * 60),
        "iss": app_id,
    }, pem_file, algorithm="RS256").decode("utf-8")


if __name__ == '__main__':


    key_file = 'private_key.pem'

    GITHUB_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAl9q8m3n26BMjG/XN9YTDD22sTJtGAmxWGf3E5XISKjstCYIQ
NU/S2Q09XpgqaLH2G+CFpszaCWMYc/WssT8RBeSKex0GhuACq2jD6x7iq/lSv098
wDnxLvxCtfobszuUGg7PeRsMPvWsO4wGpYId+L/b6eHjsiq+yCn/g8g49MPqM7h4
i9q6B2euFeNVym2U/HOWMejMJEgrucHxhebAZi8k2UI/KdRdkFjD+L9GoTvfP35y
5+mcCE0M2B+a/WKI6lRfJraLJroK1j4INUyja8p2ZSmE2wv28jqWdPKJT2TCIYWh
pMC2We35U4Xl5kDq0a6wNVQNrIt5lOsT8bmPJwIDAQABAoIBAFPa6Ff668uP9c1U
2V0A6S414/WRsQFZjdpgdkA1064aa25aslSeNdLCKud3o8OYsk0GmQdZC/YvEKvI
OIrQRrg4UfhWOOp1/UNmYPoPXiCVV4ppfHwyAuttRfFzoaRB/DC/iPZZZ1PFGkzv
sCPpTF+2otvub2xNinjCKGU/RaRzSbFPYV15wyByCSJDPTlBgWUoiJVliG+Vp3t8
rSuNeFglDvU1Y/rM5dNJ+LXHP/7xtJtNBcSiXuUM7Wv6hbpJoOhnZpYItjPVycId
gSIXdAtS1eanCnj99kNBmMmO4o6BxMPAs1cZijp41JC5rHEPLtt3Wn/7T1vqGypg
i7h3bwECgYEAyIxbprhxcgGTCHJZRyaYHEGwJ/XTiQ2JFWj4TRQ1aQOVrYD6tuRo
/6PaG2EuB0I9QaA22RL4JvEjzCHC7BWHLOYIWsiRJBPdte2pv/R0m1g2lIFD2WM4
xSEHVCtCOyG7DylIkIXIenoAhD5HBZS6h7/wKfMiHy69DA+zdEwBfsECgYEAwdeg
XpLj81WD/qrSmGfFuIQj4/T9oweYAQsx2T29Byg3fJA7BHigmYawvax2rhalZ4dq
VvkPmFJtL52eTTmpn1EEVqsHZNzfqMMCL431Qmpd31yG1K3+Lh22ESGN7Q9JKU2f
cPU6aCDQngd21fFv+lSTZyceM0+E87E/G2OK7+cCgYBxtyys737cP0pJCtXWw2qS
8yhYsEp/Nx6Y9kl9I01Zu3+evzjqhb+H3TfqOINp+ERVtuwC0H/HTQqYUDh/t4FL
ky//kiTCiUU5SIbtYkbQYwen01hOprVlCeJm9pR6hRjVcvpDgKh50j4CvnF1F61h
FhOvJb8eYVkuwqRl+EcMwQKBgQC0sGza+43k65fosg8w5bqW7wYNnfc4GwIEJw1G
dZhYrZJbWI7K8i6yLa1egP739EAmq0Hi5LM2x87jjcdcMR3+ViT3LOHtkT4jL/Q/
o9I1ILV0WemNIstG7YcjnOWRTqhiCetP/id9nOkaBdcuQqqg7GmixAIQzlUeW+B5
hWajjQKBgQCLPQOGVV8WpB9P3bQ/UVTsOj2q+HymzX3tST3g/GJH4DYlo1YSnyBX
tko9oGZR/TdoBLLNH4ehcQKGC5F3xuBO8CmiT+U89FuCEdBbisTQPNcCL2+6s+Sg
sv1wZqBqsqNuanYED7MbRnOfJh5ybLZjfpT35yyVoso6xlOWKcvgVA==
-----END RSA PRIVATE KEY-----"""
    GITHUB_APP_IDENTIFIER = "102603"

    gh = github3.github.GitHub()

    # Login as app
    gh.login_as_app(GITHUB_PRIVATE_KEY.encode(), GITHUB_APP_IDENTIFIER)

    # This could potentially break
    installations = [installation.id for installation in gh.app_installations()]
    gh.login_as_app_installation(GITHUB_PRIVATE_KEY.encode(), GITHUB_APP_IDENTIFIER, installations[0])

    issue = gh.pull_request(owner='awtkns', repository='openapi-perf-action', number=1)
    issue.create_comment('Comment from app')
