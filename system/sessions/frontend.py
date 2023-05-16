from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters

cookie_params = CookieParameters()

# Uses UUID
cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="b410ffcb40fe3f9cd37ab32dad0af9be2b30c2f379fa60e62e5c77b821a22a44",
    cookie_params=cookie_params,
)