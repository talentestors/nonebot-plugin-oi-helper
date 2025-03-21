from functools import lru_cache
import json
from nonebot.log import logger
from pathlib import Path
import nonebot_plugin_localstore as store

plugin_cache_dir: Path = store.get_cache_dir("nonebot_plugin_oi_helper")


class Dirs:
    CONTESTS = "contests.json"
    LUOGU_NEWS = "luogu_news.json"
    LEETCODE_DAILY = "leetcode_daily.json"

    def __init__(self, path: Path):
        self.contests: Path = path / Dirs.CONTESTS
        self.luogu_news: Path = path / Dirs.LUOGU_NEWS
        self.leetcode_daily: Path = path / Dirs.LEETCODE_DAILY
        logger.info(f"Dirs: {self}")

    def __str__(self) -> str:
        return self.__dict__.__str__()

    @staticmethod
    def get_dirs(path: Path):
        if path is not None:
            return Dirs(path)
        else:
            return Dirs(store.get_plugin_cache_dir())


dirs: Dirs = Dirs.get_dirs(plugin_cache_dir)


@lru_cache(maxsize=8)
def load_json(cache_file: Path):
    logger.debug(f"load_json: {cache_file}")
    if cache_file.exists():
        data = cache_file.read_text(encoding="utf8")
        # logger.debug(f"load_json: {data}")
        return json.loads(data)
    return {}


def save_json(cache_file: Path, args):
    logger.debug(f"save_json: {cache_file}")
    cache_file.write_text(
        json.dumps(args, ensure_ascii=False, indent=2), encoding="utf8"
    )


# Convert LeetCode to local Chinese version
def leetcode_locale_to_zh(object: dict) -> dict:
    link = object["link"]
    # leetcode.com -> leetcode.cn
    link = link.replace("leetcode.com", "leetcode.cn")
    # replace the contest name
    object["link"] = link
    return object


# Data format
def json2json(object, formatter=None) -> dict:
    """For consistency in the architecture"""
    return object


def json2xml(formatter=None):
    """TODO: JSON to XML"""
    assert False, "Not implemented yet"


def json2text(formatter=None):
    """Convert JSON to text

    Args:
        object (list): JSON object.
        formatter (function): Format function for each item. Must be a function and not None.
    """

    def format_text(data):
        if formatter is None or not callable(formatter):
            raise ValueError("for_item must be a function and not None")
        result = ""
        for item in data:
            text = formatter(item)
            if not isinstance(text, str):
                raise ValueError("for_item must return a string")
            result += text + "\n"
        return result.strip()

    return format_text


def json2text_for_leetcode_daily_info(leetcode_data: dict) -> str:
    text = f"""{leetcode_data["title"]}
Date: {leetcode_data["date"]}
Difficulty: {leetcode_data["difficulty"]}
URL: {leetcode_data["url"]}
"""
    return text


def json2text_for_contest(contest_data: dict) -> str:
    text = f"""Name: {contest_data["name"]}
Start Time: {contest_data["start_time"]}
End Time: {contest_data["end_time"]}
Duration: {contest_data["duration"] // 60} minutes
Link: {contest_data["link"]}
"""
    return text


def json2text_for_contest_zh(contest_data: dict) -> str:
    text = f"""比赛名称: {contest_data["name"]}
开始时间: {contest_data["start_time"]}
结束时间: {contest_data["end_time"]}
时长: {contest_data["duration"] // 60} 分钟
链接: {contest_data["link"]}
"""
    return text


def json2text_get_luogu_news_text(news: dict) -> str:
    text = f"""{news["year"]}年{news["month"]}月
{news["title"]}
URL: {news["url"]}
"""
    return text
