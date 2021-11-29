# AWS-ApiGw-Auth

## TLDR
Allows an aws iam identity (user/role) to retrieve a JWT proving its identity. This jwt can be used for api-to-api authentication, user-to-api authentication, etc.

## How it's built
Uses AWS API Gateway's IAM authenticator to require a valid iam user when requesting the jwt. The current user/role is stamped in the token's `sub` attribute.
This token can then be used to authenticate against an api. The solution also includes a `/.well-known/jwks.json` endpoint where the current token can be validated.

## How to run and build
Instructions below assume that you have `pyenv` and `pipenv` available, and python 3.9.7 is available to pyenv.

cdk_app also assumes that you have the cdk-cli installed (tested with version `1.133.0`)

### app - the lambda function that runs the rest api
```
cd app
PYENV_VERSION=3.9.7 python3 -m venv .venv
PIPENV_VENV_IN_PROJECT=1 pipenv install -d
```

create certificates used for signing and verifying JWTs:
```
cd keys
# You can just hit enter to skip thru all of the prompts
openssl req -nodes -new -x509 -keyout server.key -out server.cert
```

In order to debug locally, run (in the `app` folder):
```
pipenv run python runserver.py
```
You can now browse `http://localhost:9000/docs`


### cdk_app - cdk-based stack for deploying everything
```
cd cdk_app
PYENV_VERSION=3.9.7 python3 -m venv .venv
PIPENV_VENV_IN_PROJECT=1 pipenv install -d
```

In order to deploy: ensure you have a working `AWS_PROFILE` active, and run (in the `cdk_app` folder):
```
cdk deploy
```

### Verifying that everything works
Go to the api gateway console, find the `login` resource and test the `GET` endpoint.
The generated jwt can be pasted in to the jwt debugger at `https://jwt.io/`. Verify that the `sub` field contains your aws identity. The jwt can be verified against the jwks endpoint at 
`/.well-known/jwks.json`.