"""
@Author :Axin
@Time   :16:39
@Desc   :
"""
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends

from atguigu.app.services.chat.conversation import conversation_service

router = APIRouter(prefix="/api/v1",tags=["聊天会话路由"])



@router.post("/conversation/current")
async def get_current_conversion(service:Annotated[dict,Depends()]):
    conversation_service.get_current_conversation()

    return

