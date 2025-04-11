# none_plugin_oi_helper.filter for NoneBot2 plugin
# Copyright (C) 2025  talentestors
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

from .filter import Filter
from .strategy import ReplaceStrategyReplaceWithRegex

def replace_func(match):
    header = match.group(1) or ""
    host = match.group(2)
    host = host.rstrip("_").replace(".", "_")
    port = match.group(3) or ""
    path = match.group(4) or ""
    return f"{header}{host}{port}{path}"

replace_strategy = ReplaceStrategyReplaceWithRegex(
    r"^(https?://)?([a-zA-Z0-9._-]+)(:[0-9]+)?(/.*)?",
    replace_func
)

filter = Filter(strategy_of_replace=replace_strategy)
