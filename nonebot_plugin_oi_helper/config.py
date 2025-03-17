from pydantic import BaseModel, field_validator
from nonebot.log import logger


class ScopedConfig(BaseModel):
    user_key: str
    username: str
    req_url: str = "https://clist.by:443/api/v4/contest/?upcoming=true&filtered=true&order_by=start&format=json"


class Config(BaseModel):
    clist: ScopedConfig

    @field_validator("clist")
    @classmethod
    def check_priority(cls, v: ScopedConfig) -> ScopedConfig:
        if v.user_key is None or v.username is None:
            logger.error("nonebot-plugin-oi-helper: api_key or username is None", v)
            raise ValueError("nonebot-plugin-oi-helper: api_key or username is None")
        if v.user_key == "" or v.username == "":
            logger.error("nonebot-plugin-oi-helper: api_key or username is empty", v)
            raise ValueError("nonebot-plugin-oi-helper: api_key or username is empty")
        return v
