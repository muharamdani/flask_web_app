import secrets

secret = secrets.token_hex()
jwt_secret = secrets.token_hex(12)
print("Copy secret and jwt_secret value to .env file")
print({
    'secret': secret,
    'jwt_secret': jwt_secret
})
