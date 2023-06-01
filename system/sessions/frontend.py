from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters

from config import SECRET_KEY

cookie_params = CookieParameters()

# Uses UUID
cookie = SessionCookie(
    cookie_name="cb_token",
    identifier="general_verifier",
    auto_error=True,
    secret_key=SECRET_KEY,
    cookie_params=cookie_params,
)
