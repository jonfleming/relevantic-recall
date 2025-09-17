from fastapi import APIRouter, HTTPException, Depends, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from datetime import timedelta
from typing import Optional
import httpx

from ..core.config import settings
from ..core.security import create_access_token
from ..core.deps import get_current_active_user
from ..db.database import get_session
from ..db import crud
from ..schemas.user import UserCreate, Token

router = APIRouter()

# OAuth2 configuration
config = Config(environ={
    'GOOGLE_CLIENT_ID': settings.google_client_id,
    'GOOGLE_CLIENT_SECRET': settings.google_client_secret,
    'GITHUB_CLIENT_ID': settings.github_client_id,
    'GITHUB_CLIENT_SECRET': settings.github_client_secret,
})

oauth = OAuth(config)

# Register OAuth providers
oauth.register(
    name='google',
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

oauth.register(
    name='github',
    client_id=settings.github_client_id,
    client_secret=settings.github_client_secret,
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'}
)

@router.get("/login/{provider}")
async def oauth_login(provider: str, request: Request):
    """Initiate OAuth login with the specified provider"""
    if provider not in ['google', 'github']:
        raise HTTPException(status_code=400, detail="Unsupported provider")
    
    if not getattr(settings, f"{provider}_client_id") or not getattr(settings, f"{provider}_client_secret"):
        raise HTTPException(status_code=500, detail=f"{provider.title()} OAuth not configured")
    
    redirect_uri = request.url_for('oauth_callback', provider=provider)
    client = oauth.create_client(provider)
    return await client.authorize_redirect(request, redirect_uri)

@router.get("/callback/{provider}")
async def oauth_callback(provider: str, request: Request, db: AsyncSession = Depends(get_session)):
    """Handle OAuth callback and create/login user"""
    if provider not in ['google', 'github']:
        raise HTTPException(status_code=400, detail="Unsupported provider")
    
    client = oauth.create_client(provider)
    token = await client.authorize_access_token(request)
    
    if provider == 'google':
        user_info = token.get('userinfo')
        if not user_info:
            # Fallback to userinfo endpoint
            resp = await client.get('userinfo', token=token)
            user_info = resp.json()
        
        email = user_info.get('email')
        full_name = user_info.get('name')
        provider_id = user_info.get('sub')
        avatar_url = user_info.get('picture')
        
    elif provider == 'github':
        # Get user info from GitHub API
        resp = await client.get('user', token=token)
        user_info = resp.json()
        
        # Get primary email (GitHub might not return email in user object)
        email_resp = await client.get('user/emails', token=token)
        emails = email_resp.json()
        primary_email = next((email['email'] for email in emails if email['primary']), None)
        
        email = user_info.get('email') or primary_email
        full_name = user_info.get('name') or user_info.get('login')
        provider_id = str(user_info.get('id'))
        avatar_url = user_info.get('avatar_url')
    
    if not email:
        raise HTTPException(status_code=400, detail="Email not provided by OAuth provider")
    
    # Check if user exists
    user = await crud.get_user_by_provider(db, provider, provider_id)
    
    if not user:
        # Check if user exists with same email but different provider
        user = await crud.get_user_by_email(db, email)
        if user:
            # Update existing user with new provider info
            user.provider = provider
            user.provider_id = provider_id
            if avatar_url:
                user.avatar_url = avatar_url
            await db.commit()
        else:
            # Create new user
            user_create = UserCreate(
                email=email,
                full_name=full_name,
                provider=provider,
                provider_id=provider_id,
                avatar_url=avatar_url
            )
            user = await crud.create_user(db, user_create)
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        subject=str(user.id), expires_delta=access_token_expires
    )
    
    # Redirect to frontend with token
    frontend_url = f"{settings.frontend_url}/auth/callback?token={access_token}"
    return RedirectResponse(url=frontend_url)

@router.post("/logout")
async def logout():
    """Logout endpoint (client should delete token)"""
    return {"message": "Logged out successfully"}

@router.get("/me")
async def get_current_user_info(current_user = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user