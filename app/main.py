import json

from fastapi import FastAPI, Request
from mangum import Mangum
from jwk import generate_jwk, generate_jwt

app = FastAPI()


@app.get("/")
async def get_jwt(request: Request):
    scope = request.scope.get("aws.event")
    headers = request.headers
    print(f"{headers=}")
    print(json.dumps(scope))
    return {"status": "root"}


@app.get("/login")
async def get_jwt(request: Request):
    scope = request.scope.get("aws.event", {})
    print(json.dumps(scope))
    token = generate_jwt(scope)
    return {
        "token": token
    }


@app.get("/.well-known/jwks.json")
async def get_jwk():
    return generate_jwk()


@app.get("/random")
async def get_jwt(request: Request):
    return {"status": "random"}


handler = Mangum(app)
