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
    """
    权限限制：
    1、对应的用户身份
    2 用户身份角色是否是接口允许的角色
    :param service:
    :return:
    """


    conversation_service.get_current_conversation()

    return

