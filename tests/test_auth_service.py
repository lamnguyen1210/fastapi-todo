def test_hash_password_is_not_plaintext():
    from app.auth.service import hash_password
    hashed = hash_password("mypassword")
    assert hashed != "mypassword"
    assert len(hashed) > 20


def test_verify_password_correct():
    from app.auth.service import hash_password, verify_password
    hashed = hash_password("mypassword")
    assert verify_password("mypassword", hashed) is True


def test_verify_password_wrong():
    from app.auth.service import hash_password, verify_password
    hashed = hash_password("mypassword")
    assert verify_password("wrongpassword", hashed) is False


def test_create_and_decode_token():
    from app.auth.service import create_access_token, decode_access_token
    token = create_access_token({"sub": "42"})
    payload = decode_access_token(token)
    assert payload["sub"] == "42"


def test_decode_token_contains_expiry():
    from app.auth.service import create_access_token, decode_access_token
    token = create_access_token({"sub": "1"})
    payload = decode_access_token(token)
    assert "exp" in payload
