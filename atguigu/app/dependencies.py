"""
@Author :Axin
@Time   :16:06
@Desc   :
"""
""" 依赖注入组装 """


from typing import Annotated

from fastapi import Depends

from atguigu.app.services.chat.conversation import ConversationService


def get_conversation_service():
    return ConversationService()


ConversationServiceDep = Annotated[ConversationService, Depends(get_conversation_service)]
