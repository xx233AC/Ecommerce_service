"""
@Author :Axin
@Time   :8:39
@Desc   :
"""
import jwt
from fastapi import HTTPException,status

from atguigu.app.schemas.user import CurrentUser
from atguigu.common.config import  Settings


class AuthService:
    """
    认证服务
    """
    def __init__(self):
        self.settings = Settings()


    def get_authorized_user(self,authorization:str | None,
                            *roles:str
                            )-> CurrentUser:
        """
        职责：获取当前用户信息 以及 完成角色的校验
        :return:
        """
        #1、根据令牌获取用户信息
        current_user = self._get_current_token(authorization)

        #2、校验角色 如果不是roles中的其一 就无权访问
        if current_user.role not in roles:
            
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="该用户无权访问！")
        
        return current_user

    def _get_current_token(self, authorization:str | None) -> CurrentUser:
        #1、获取令牌
        access_token = self._extract_token(authorization)

        #2、根据令牌去解密 获取用户信息
        current_user = self._decode_access_token(access_token)

        return current_user

    def _extract_token(self, authorization:str | None) -> str:
        """
        获取令牌
        :param authorization:
        :return:
        """
        if not authorization or not authorization.lower().startswith("bearer "):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="该用户未认证"
            )
        return authorization.split(sep=" ", maxsplit=1)[1]  # maxsplit表示按照sep最多切分几次，此处只切1次即可

    def _decode_access_token(self, access_token:str) -> CurrentUser:
        """
        根据令牌去解密 得到用户信息
        :param access_token:
        :return:
        """
        payload = jwt.decode(jwt=access_token,key=self.settings.jwt_secret,algorithms=self.settings.jwt_algorithm)

        return CurrentUser.model_validate(payload)  # model_validate把荷载payload校验为CurrentUser
