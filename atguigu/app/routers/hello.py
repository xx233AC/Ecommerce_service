"""
@Author :Axin
@Time   :16:18
@Desc   :
"""
from fastapi import FastAPI,APIRouter
from pydantic import BaseModel

router = APIRouter()


class User(BaseModel):  # 定义数据模型
    """ pydantic 自动进行类型转换以及参数类型的校验 和 过滤 """
    name: str
    age: int

@router.get("/hello", response_model=User)    # 指定数据模型
async def hello():
    return {"name":"xxx" , "age": "18"}
