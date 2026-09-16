"""
@Author :Axin
@Time   :8:45
@Desc   :
"""
from typing import Literal

from pydantic import BaseModel

"""
用户信息的约束的 数据模型
"""

class CurrentUser(BaseModel):
    user_id:str
    role:Literal["customer","agent","admin"] = "customer"  # Literal类型标注工具，表示这个值只能从列出的值里选

