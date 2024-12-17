from functools import lru_cache
import json
from nonebot import get_plugin_config
from .config import Config
import os

config = get_plugin_config(Config)


def ensure_dir_exists(file_path):
    """Ensure the directory exists, create it if it does not exist"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)


@lru_cache(maxsize=8)
def load_json(file_name) -> dict:
    path = os.path.join(os.path.dirname(__file__), file_name)
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding="utf8") as f:
            data = json.load(f)
            return data
    except IOError as e:
        print(f"Error reading file {file_name}: {e}")
        return {}
    except ValueError as e:
        print(f"Error parsing JSON from file {file_name}: {e}")
        return {}


def save_json(file_name, args):
    path = os.path.join(os.path.dirname(__file__), file_name)
    ensure_dir_exists(path)
    with open(path, "w", encoding="utf8") as f:
        json.dump(args, f, ensure_ascii=False, indent=2)


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
    text = f"""{leetcode_data['title']}
Date: {leetcode_data['date']}
Difficulty: {leetcode_data['difficulty']}
URL: {leetcode_data['url']}
"""
    return text


def json2text_for_contest(contest_data: dict) -> str:
    text = f"""Name: {contest_data['name']}
Start Time: {contest_data['start_time']}
End Time: {contest_data['end_time']}
Duration: {contest_data['duration']//60} minutes
Link: {contest_data['link']}
"""
    return text


def json2text_for_contest_zh(contest_data: dict) -> str:
    text = f"""比赛名称: {contest_data['name']}
开始时间: {contest_data['start_time']}
结束时间: {contest_data['end_time']}
时长: {contest_data['duration']//60} 分钟
链接: {contest_data['link']}
"""
    return text


def json2text_get_luogu_news_text(news: dict) -> str:
    text = f"""{news['year']}年{news['month']}月
{news['title']}
URL: {news['url']}
"""
    return text
