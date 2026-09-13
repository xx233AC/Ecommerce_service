"""
@Author :Axin
@Time   :16:07
@Desc   :
"""
""" 应用实例 """

from fastapi import FastAPI
from atguigu.app.routers import hello

app1 = FastAPI(description="FastAPI集成的客服服务")
app1.include_router(hello.router)


