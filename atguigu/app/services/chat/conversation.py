"""
@Author :Axin
@Time   :16:48
@Desc   :
"""
from typing import Any


class ConversationService:


    async def get_current_conversation(self) ->dict[str, Any]:
        """ 获取当前会话 """

        return {"id":"--"}



conversation_service = ConversationService()
