from fastapi import APIRouter

router = APIRouter()

from . import chat, context, entity, auth

router.include_router(chat.router, prefix="/chat", tags=["chat"]) 
router.include_router(context.router, prefix="/context", tags=["context"]) 
router.include_router(entity.router, prefix="/entity", tags=["entity"]) 
router.include_router(auth.router, prefix="/auth", tags=["auth"]) 
