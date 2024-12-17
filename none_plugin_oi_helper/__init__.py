from nonebot.log import logger
from nonebot.plugin import PluginMetadata
from .config import Config
from .scheduler import scheduler_constroller as s_constroller
from .utils import config
from . import query_api


__plugin_meta__ = PluginMetadata(
    name="OI_micro_helper",
    description="I-micro-helper for NoneBot2 plugin",
    usage="",
    config=Config,
)

__all__ = ["query_api"]

_config = config


def get_api_config():
    return _config.clist


api_config = get_api_config()
logger.info("username: " + api_config.username)
logger.info("user_key: " + api_config.user_key[:6]+("*" * (len(api_config.user_key) - 6)))
logger.info("request url: " + _config.clist.req_url)
task_controller = s_constroller()  # noqa: F841
logger.info("scheduler controller loaded")
