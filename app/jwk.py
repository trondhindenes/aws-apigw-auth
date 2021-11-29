from functools import lru_cache

from jwcrypto import jwk
from jwcrypto import jwt
import time


expiry_seconds = 86400


@lru_cache
def get_key():
    pub_key_file_path = "keys/server.cert"
    priv_key_file_path = "keys/server.key"
    with open(pub_key_file_path, "rb") as pemfile:
        key = jwk.JWK.from_pem(pemfile.read())
    with open(priv_key_file_path, "rb") as priv_file:
        key.import_from_pem(data=priv_file.read())
    return key


@lru_cache
def generate_jwk():
    key = get_key()
    key_jwk = key.export_public(as_dict=True)
    payload = {
        "keys": [key_jwk]
    }
    return payload


def generate_jwt(scope: dict = None):
    if scope:
        extra_claims = {
            "sub": scope["requestContext"]["identity"]["userArn"]
        }
    else:
        extra_claims = {}
    iat_val = int(time.time())
    claims = {
        "iat": iat_val,
        "exp": iat_val + expiry_seconds
    }
    key = get_key()
    token = jwt.JWT(
        header={
            "alg": "RS256",
            "kid": key.key_id,
            "typ": "JWT"
        },
        claims={**extra_claims, **claims}
    )

    token.make_signed_token(key)

    return token.serialize()
