# OAuth2 Implementation for Relevantic Recall

This document describes the OAuth2 authentication implementation for the Relevantic Recall application.

## Overview

The application now supports OAuth2 authentication with Google and GitHub providers. All API endpoints that handle user data require authentication.

## Features

- **OAuth2 Providers**: Google and GitHub
- **JWT Tokens**: Secure token-based authentication
- **User Management**: Automatic user creation and management
- **Protected Endpoints**: All chat, context, and entity endpoints require authentication
- **Session Management**: Per-user data isolation

## Setup

### 1. Environment Configuration

Copy the example environment file and configure OAuth2 providers:

```bash
cp .env.example .env
```

Edit `.env` with your OAuth2 credentials:

```env
# OAuth2 Google Configuration
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# OAuth2 GitHub Configuration  
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

### 2. OAuth2 Provider Setup

#### Google OAuth2 Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
5. Set authorized redirect URIs:
   - `http://localhost:8000/api/auth/callback/google` (development)
   - `https://your-domain.com/api/auth/callback/google` (production)

#### GitHub OAuth2 Setup

1. Go to GitHub Settings → Developer settings → OAuth Apps
2. Click "New OAuth App"
3. Set Authorization callback URL:
   - `http://localhost:8000/api/auth/callback/github` (development)
   - `https://your-domain.com/api/auth/callback/github` (production)

### 3. Database Migration

Run the database migration to create user tables:

```bash
alembic upgrade head
```

## API Endpoints

### Authentication Endpoints

- `GET /api/auth/login/{provider}` - Initiate OAuth login (provider: google, github)
- `GET /api/auth/callback/{provider}` - OAuth callback handler
- `POST /api/auth/logout` - Logout (client should delete token)
- `GET /api/auth/me` - Get current user information (requires authentication)

### Protected Endpoints

All these endpoints now require authentication via Bearer token:

- `POST /api/chat/` - Send chat message
- `GET /api/context/{session_id}` - Get session context
- `POST /api/entity/resolve` - Resolve entity mention

## Authentication Flow

### 1. Frontend OAuth Flow

```javascript
// Redirect user to OAuth login
window.location.href = '/api/auth/login/google';

// After successful authentication, user will be redirected to:
// http://localhost:3000/auth/callback?token=jwt_token_here

// Store the token and use it for API calls
localStorage.setItem('auth_token', token);
```

### 2. API Authentication

Include the JWT token in API requests:

```javascript
fetch('/api/chat/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    session_id: 'uuid',
    message: 'Hello world',
    role: 'user'
  })
})
```

## User Data Model

```python
class User:
    id: UUID              # Primary key
    email: str            # User email from OAuth provider
    full_name: str        # User's full name
    provider: str         # "google" or "github"
    provider_id: str      # Provider's user ID
    avatar_url: str       # User's avatar URL
    is_active: bool       # Account status
    created_at: datetime  # Account creation time
    updated_at: datetime  # Last update time
```

## Security Features

- **JWT Tokens**: Secure token-based authentication with configurable expiration
- **User Isolation**: All user data is scoped to the authenticated user
- **Provider Security**: Uses official OAuth2 flows for Google and GitHub
- **CORS Configuration**: Proper CORS setup for frontend integration

## Testing

The implementation includes basic tests to verify:
- Unauthenticated requests are properly rejected
- OAuth endpoints are accessible
- Protected endpoints require authentication

Run tests with:
```bash
python /tmp/test_oauth.py
```

## Development

### Adding New OAuth Providers

To add a new OAuth provider:

1. Add provider configuration to `app/core/config.py`
2. Register the provider in `app/api/auth.py`
3. Add provider-specific user info extraction logic
4. Update environment variables documentation

### Customizing Authentication

- Modify token expiration in `app/core/config.py`
- Add custom user fields in `app/db/models.py`
- Implement additional authentication middleware in `app/core/deps.py`

## Troubleshooting

### Common Issues

1. **"OAuth not configured" error**: Check that client ID and secret are set in environment variables
2. **Token validation errors**: Verify SECRET_KEY is set and consistent
3. **Database errors**: Ensure migrations are applied with `alembic upgrade head`
4. **CORS issues**: Check that FRONTEND_URL is correctly configured

### Debug Mode

Enable debug logging by setting:
```env
DEBUG=true
```