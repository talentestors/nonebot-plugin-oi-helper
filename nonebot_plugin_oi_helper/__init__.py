# none_plugin_oi_helper for NoneBot2 plugin
# Copyright (C) 2024  talentestors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import nonebot
from nonebot import require, get_plugin_config
from nonebot.log import logger
from nonebot.plugin import PluginMetadata
from .config import Config

require("nonebot_plugin_localstore")
require("nonebot_plugin_apscheduler")

__plugin_meta__ = PluginMetadata(
    name="none_plugin_oi_helper",
    description="A NoneBot2 plugin for querying OI/ACM related information, including LeetCode daily question and Luogu daily report.",
    usage="Provides commands to query OI/ACM-related information, including LeetCode daily challenges and Luogu daily reports.",
    config=Config,
    homepage="https://github.com/talentestors/none-plugin-oi-helper",
    type="application",
    supported_adapters=None,
    extra={
        "author": "talentestors",
        "version": "0.5.0",
        "tags": ["nonebot", "plugin", "OI", "ACM", "LeetCode", "Luogu"],
    },
)


config = get_plugin_config(Config)

api_config = config.clist

logger.info("api_config loaded")
logger.info("username: " + api_config.username)
logger.info(
    "user_key: " + api_config.user_key[:6] + ("*" * (len(api_config.user_key) - 6))
)
logger.info("request url: " + config.clist.req_url)

__all__ = ["api_config", "config"]

from .command import *  # noqa: E402, F403
from .scheduler import *  # noqa: E402, F403

drivers = nonebot.get_driver()
# ruff: noqa F405
@drivers.on_startup
def scheduler_constroller():
    """
    scheduler controller
    """
    logger.info("Message data loading...")
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # 没有运行中的事件循环，新建并运行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(init())
    else:
        # 已存在运行中的事件循环，创建任务执行
        loop.create_task(init())
    logger.info("Message data loaded.\n")
    return scheduler

logger.info("scheduler first controller loaded")
