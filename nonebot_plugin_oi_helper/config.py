from pydantic import BaseModel, Field


class ScopedConfig(BaseModel):
    user_key: str = Field(..., min_length=0, description="API key for clist.by")
    username: str = Field(..., min_length=0, description="Username for clist.by")
    req_url: str = Field(
        default="https://clist.by:443/api/v4/contest/?upcoming=true&filtered=true&order_by=start&format=json",
        description="Request URL for clist.by",
    )


class Config(BaseModel):
    clist: ScopedConfig
