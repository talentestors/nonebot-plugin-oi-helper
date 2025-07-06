import aiohttp
import re
from nonebot.log import logger
from datetime import datetime, timedelta
from .utils import leetcode_locale_to_zh, load_json, save_json, dirs
from . import api_config


async def getContest():
    apikey = f"&username={api_config.username}&api_key={api_config.user_key}"
    url = f"{str(api_config.req_url)}" + apikey
    logger.info("GET " + str(api_config.req_url))
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=12)) as resp:
            resp.raise_for_status()
            logger.info("getContest SUCCESS " + str(resp.status))
            data = await resp.json()
    contests = []
    for contest in data["objects"]:
        name = contest["event"]
        host = contest["host"]
        start_time = (
            datetime.strptime(contest["start"], "%Y-%m-%dT%H:%M:%S")
            + timedelta(hours=8)
        ).strftime("%Y-%m-%d %H:%M")
        end_time = (
            datetime.strptime(contest["end"], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=8)
        ).strftime("%Y-%m-%d %H:%M")
        new_contest = {
            "name": name,
            "host": host,
            "start_time": start_time,
            "end_time": end_time,
            "duration": contest["duration"],
            "link": contest["href"],
        }
        match host:
            case "leetcode.com":
                new_contest = leetcode_locale_to_zh(new_contest)
        contests.append(new_contest)
    save_json(dirs.contests, contests)


LeetCode_Headers = {
    "origin": "https://leetcode.cn",
    "referer": "https://leetcode.cn/problemset/all/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "content-type": "application/json",
    "accept": "application/json",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "accept-encoding": "gzip, deflate, br",
}


# check if the daily question is updated
def checkLeetcodeDailyData(_data) -> bool:
    if _data == {}:
        return False
    now = datetime.now()
    cache_time = datetime.strptime(_data["date"], "%Y-%m-%d")
    return now - cache_time < timedelta(days=1)


async def getLeetcodeDaily():
    _data = load_json(dirs.leetcode_daily)
    logger.debug("LeetCode Daily Question: " + str(_data))
    if checkLeetcodeDailyData(_data):
        logger.info("LeetCode Daily Question is lastest.")
        return _data
    logger.info("LeetCode Daily Question is outdated.")

    # 重试机制
    max_retries = 3
    for attempt in range(max_retries):
        try:
            logger.info(f"GET https://leetcode.cn/graphql (attempt {attempt + 1})")
            async with aiohttp.ClientSession() as session:
                logger.debug("session created")

                # 第一个请求：获取今日题目信息
                async with session.post(
                    "https://leetcode.cn/graphql",
                    json={
                        "operationName": "questionOfToday",
                        "variables": {},
                        "query": "query questionOfToday { todayRecord {   question {     questionFrontendId     questionTitleSlug     __typename   }   lastSubmission {     id     __typename   }   date   userStatus   __typename }}",
                    },
                    headers=LeetCode_Headers,
                    timeout=aiohttp.ClientTimeout(total=15),
                ) as response:
                    logger.debug(f"Response status: {response.status}")
                    logger.debug(f"Response headers: {dict(response.headers)}")

                    if response.status != 200:
                        logger.error(f"HTTP error: {response.status}")
                        response_text = await response.text()
                        logger.error(f"Response text: {response_text[:500]}")
                        raise Exception(
                            f"HTTP {response.status}: {response_text[:200]}"
                        )

                    try:
                        response_text = await response.text()
                        logger.debug(f"Response text length: {len(response_text)}")

                        if not response_text.strip():
                            raise Exception("响应内容为空")

                        # 检查是否返回的是HTML而不是JSON
                        if response_text.strip().startswith("<"):
                            logger.error("响应似乎是HTML页面，可能被反爬虫机制拦截")
                            logger.debug(f"HTML response: {response_text[:500]}")
                            raise Exception("获取到HTML响应，可能被反爬虫机制拦截")

                        import json

                        RawData = json.loads(response_text)
                        logger.trace("response received and parsed")
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON解析错误: {e}")
                        logger.debug(f"Response text: {response_text[:500]}")
                        raise Exception(f"JSON解析错误: {e}")
                    except Exception as e:
                        logger.error(f"解析响应时出错: {e}")
                        raise e

                    # 检查返回的数据结构
                    if "data" not in RawData or not RawData["data"]:
                        logger.error("API返回的数据结构不正确")
                        logger.debug(f"RawData: {RawData}")
                        raise Exception("API返回的数据结构不正确")

                    if (
                        "todayRecord" not in RawData["data"]
                        or not RawData["data"]["todayRecord"]
                    ):
                        logger.error("没有找到今日题目记录")
                        logger.debug(f"RawData: {RawData}")
                        raise Exception("没有找到今日题目记录")

                    EnglishTitle = RawData["data"]["todayRecord"][0]["question"][
                        "questionTitleSlug"
                    ]
                    Date = RawData["data"]["todayRecord"][0]["date"]
                    QuestionUrl = f"https://leetcode.cn/problems/{EnglishTitle}"

                # 第二个请求：获取题目详细信息
                async with session.post(
                    "https://leetcode.cn/graphql",
                    json={
                        "operationName": "questionData",
                        "variables": {"titleSlug": EnglishTitle},
                        "query": "query questionData($titleSlug: String!) {  question(titleSlug: $titleSlug) {    questionId    questionFrontendId    boundTopicId    title    titleSlug    content    translatedTitle    translatedContent    isPaidOnly    difficulty    likes    dislikes    isLiked    similarQuestions    contributors {      username      profileUrl      avatarUrl      __typename    }    langToValidPlayground    topicTags {      name      slug      translatedName      __typename    }    companyTagStats    codeSnippets {      lang      langSlug      code      __typename    }    stats    hints    solution {      id      canSeeDetail      __typename    }    status    sampleTestCase    metaData    judgerAvailable    judgeType    mysqlSchemas    enableRunCode    envInfo    book {      id      bookName      pressName      source      shortDescription      fullDescription      bookImgUrl      pressImgUrl      productUrl      __typename    }    isSubscribed    isDailyQuestion    dailyRecordStatus    editorType    ugcQuestionId    style    __typename  }}",
                    },
                    headers=LeetCode_Headers,
                    timeout=aiohttp.ClientTimeout(total=15),
                ) as response:
                    if response.status != 200:
                        logger.error(f"获取题目详情时HTTP错误: {response.status}")
                        response_text = await response.text()
                        logger.error(f"Response text: {response_text[:500]}")
                        raise Exception(f"获取题目详情时HTTP错误: {response.status}")

                    logger.trace("response receiving")
                    response_text = await response.text()
                    RawData = json.loads(response_text)
                    Data = RawData["data"]["question"]
                    ID = Data["questionFrontendId"]
                    Difficulty = Data["difficulty"]
                    ChineseTitle = Data["translatedTitle"]
                    Content = (
                        re.sub(r"(<\w+>|</\w+>)", "", Data["translatedContent"])
                        .replace("&nbsp;", "")
                        .replace("&lt;", "<")
                        .replace("\t", "")
                        .replace("\n\n", "\n")
                        .replace("\n\n", "\n")
                    )
                    data = {
                        "id": ID,
                        "title": ChineseTitle,
                        "difficulty": Difficulty,
                        "content": Content,
                        "url": QuestionUrl,
                        "date": Date,
                    }
                    logger.info("getLeetcodeDaily SUCCESS " + str(response.status))
                    logger.debug("data: " + str(data))
                    save_json(dirs.leetcode_daily, data)
                    return data

        except Exception as e:
            logger.error(f"第{attempt + 1}次尝试获取力扣每日一题失败: {e}")
            if attempt < max_retries - 1:
                import asyncio

                await asyncio.sleep(2**attempt)  # 指数退避
            else:
                logger.error("所有重试均失败")
                raise e
