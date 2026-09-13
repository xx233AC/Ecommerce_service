"""
@Author :Axin
@Time   :16:02
@Desc   :
"""

import uvicorn

from atguigu.common.config import get_settings



if __name__ == '__main__':

    settings = get_settings()

    uvicorn.run(app = "app.app:app1", host=settings.api_host, port=settings.api_port)

