from nonebot.log import logger
import nonebot
from nonebot import require

# 导入适配器

nonebot.init()

# 加载插件
require("nonebot_plugin_oi_helper")
logger.info("Plugin loaded")
