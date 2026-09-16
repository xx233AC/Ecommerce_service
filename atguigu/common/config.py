"""
@Author :Axin
@Time   :15:41
@Desc   :
"""
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ENV_FILE = Path(__file__).resolve().parents[2] / ".env"

class Settings(BaseSettings):  # 继承pydantic里面的settings ， 方便后面做数据校验和数据转换
    database_url:str = (
        "postgres+psycopg://customer_service:customer_service@192.168.200.233:5432/customer_service"
    )
    redis_url:str   # 后面写的都是默认值 ， 配置文件中写了 懒得再写了
    jwt_secret:str
    jwt_algorithm:str
    api_host:str
    api_port:int
    cors_origins:list[str]

    model_config = SettingsConfigDict(env_file=ENV_FILE,extra="ignore")  # 读取.env文件配置
     #model_config 只能这样写 不能写成model或者config 固定写法   #extra: 表示配置文件中有的配置， 但是这里没有定义 那么直接忽略


@lru_cache   # lru 是一种缓存清除算法  ， 清除最近时间没有使用的缓存内容
def get_settings() -> Settings:   #将实例对象返回 并存到缓存
    return Settings()


if __name__ == '__main__':

    settings = get_settings()