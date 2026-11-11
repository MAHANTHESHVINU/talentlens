import os

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, HTTPException, Request
from starlette.responses import RedirectResponse

router = APIRouter()
oauth = OAuth()

AUTH_REQUIRED = os.getenv("AUTH_REQUIRED", "false").strip().lower() == "true"
SESSION_SECRET = os.getenv("SESSION_SECRET", "")
SESSION_COOKIE_SECURE = os.getenv(
    "SESSION_COOKIE_SECURE",
    "true" if AUTH_REQUIRED else "false",
).strip().lower() == "true"

PROVIDER_SETTINGS = {
    "google": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "server_metadata_url": "https://accounts.google.com/.well-known/openid-configuration",
        "client_kwargs": {"scope": "openid email profile"},
    },
    "microsoft": {
        "client_id": os.getenv("MICROSOFT_CLIENT_ID"),
        "client_secret": os.getenv("MICROSOFT_CLIENT_SECRET"),
        "server_metadata_url": (
            "https://login.microsoftonline.com/common/v2.0/"
            ".well-known/openid-configuration"
        ),
        "client_kwargs": {"scope": "openid email profile"},
    },
}

for provider, settings in PROVIDER_SETTINGS.items():
    if settings["client_id"] and settings["client_secret"]:
        oauth.register(name=provider, **settings)


def validate_auth_configuration() -> None:
    if not AUTH_REQUIRED:
        return

    if not SESSION_SECRET:
        raise RuntimeError("SESSION_SECRET must be set when AUTH_REQUIRED=true.")


async def require_authenticated_user(request: Request) -> dict:
    if not AUTH_REQUIRED:
        return {"authenticated": False, "mode": "local"}

    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Sign-in is required.")
    return user


@router.get("/config")
def auth_config(request: Request):
    user = request.session.get("user") if AUTH_REQUIRED else None
    return {
        "auth_required": AUTH_REQUIRED,
        "user": user,
        "providers": [
            provider
            for provider, settings in PROVIDER_SETTINGS.items()
            if settings["client_id"] and settings["client_secret"]
        ],
    }


@router.get("/login/{provider}")
async def login(provider: str, request: Request):
    if provider not in PROVIDER_SETTINGS:
        raise HTTPException(status_code=404, detail="Unsupported sign-in provider.")

    client = oauth.create_client(provider)
    if client is None:
        raise HTTPException(
            status_code=503,
            detail=f"{provider.title()} sign-in is not configured.",
        )

    redirect_uri = request.url_for("oauth_callback", provider=provider)
    return await client.authorize_redirect(request, redirect_uri)


@router.get("/callback/{provider}", name="oauth_callback")
async def oauth_callback(provider: str, request: Request):
    if provider not in PROVIDER_SETTINGS:
        raise HTTPException(status_code=404, detail="Unsupported sign-in provider.")

    client = oauth.create_client(provider)
    if client is None:
        raise HTTPException(
            status_code=503,
            detail=f"{provider.title()} sign-in is not configured.",
        )

    token = await client.authorize_access_token(request)
    userinfo = token.get("userinfo")
    if not userinfo:
        userinfo = await client.userinfo(token=token)

    subject = userinfo.get("sub") or userinfo.get("oid")
    email = userinfo.get("email") or userinfo.get("preferred_username")
    if not subject or not email:
        raise HTTPException(
            status_code=400,
            detail="The identity provider did not return a user ID and email.",
        )

    request.session.clear()
    request.session["user"] = {
        "id": str(subject),
        "email": str(email),
        "name": str(userinfo.get("name") or email),
        "provider": provider,
    }
    return RedirectResponse(url=request.url_for("dashboard"), status_code=303)


@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return {"success": True}
