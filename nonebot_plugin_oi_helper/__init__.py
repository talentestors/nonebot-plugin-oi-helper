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

from nonebot.log import logger
from nonebot.plugin import PluginMetadata
from .config import Config
from .utils import config
from . import command
from . import query_api
from nonebot import require

require("nonebot_plugin_apscheduler")

from .scheduler import scheduler_constroller as s_constroller  # noqa: E402

__plugin_meta__ = PluginMetadata(
    name="none_plugin_oi_helper",
    description="none_plugin_oi_helper for NoneBot2 plugin",
    usage="This is a helper library for the none-plugin-oi. Use this library to assist with various operations related to the none-plugin-oi.",
    config=Config,
    homepage="https://github.com/talentestors/none-plugin-oi-helper",
    type="library",
    supported_adapters=None,
    extra={
        "author": "talentestors",
        "version": "0.1.0",
        "tags": ["nonebot", "plugin", "oi-helper"],
    },
)

__all__ = ["command", "query_api"]

_config = config


def get_api_config():
    return _config.clist


api_config = get_api_config()
logger.info("username: " + api_config.username)
logger.info(
    "user_key: " + api_config.user_key[:6] + ("*" * (len(api_config.user_key) - 6))
)
logger.info("request url: " + _config.clist.req_url)
task_controller = s_constroller()
logger.info("scheduler controller loaded")
