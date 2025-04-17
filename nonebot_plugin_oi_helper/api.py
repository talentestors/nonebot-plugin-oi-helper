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
    "origin": "https://leetcode-cn.com",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
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
    logger.info("GET https://leetcode-cn.com")
    async with aiohttp.ClientSession() as session:
        logger.debug("session created")
        async with session.post(
            "https://leetcode.cn/graphql",
            json={
                "operationName": "questionOfToday",
                "variables": {},
                "query": "query questionOfToday { todayRecord {   question {     questionFrontendId     questionTitleSlug     __typename   }   lastSubmission {     id     __typename   }   date   userStatus   __typename }}",
            },
            headers=LeetCode_Headers,
            timeout=aiohttp.ClientTimeout(total=10),
        ) as response:
            try:
                logger.trace("response receiving")
                RawData = await response.json(content_type=None)
                logger.trace("response received")
            except Exception as e:
                logger.error("解析响应时出错：" + repr(e))
                raise e
            EnglishTitle = RawData["data"]["todayRecord"][0]["question"][
                "questionTitleSlug"
            ]
            Date = RawData["data"]["todayRecord"][0]["date"]
            QuestionUrl = f"https://leetcode.cn/problems/{EnglishTitle}"
        async with session.post(
            "https://leetcode.cn/graphql",
            json={
                "operationName": "questionData",
                "variables": {"titleSlug": EnglishTitle},
                "query": "query questionData($titleSlug: String!) {  question(titleSlug: $titleSlug) {    questionId    questionFrontendId    boundTopicId    title    titleSlug    content    translatedTitle    translatedContent    isPaidOnly    difficulty    likes    dislikes    isLiked    similarQuestions    contributors {      username      profileUrl      avatarUrl      __typename    }    langToValidPlayground    topicTags {      name      slug      translatedName      __typename    }    companyTagStats    codeSnippets {      lang      langSlug      code      __typename    }    stats    hints    solution {      id      canSeeDetail      __typename    }    status    sampleTestCase    metaData    judgerAvailable    judgeType    mysqlSchemas    enableRunCode    envInfo    book {      id      bookName      pressName      source      shortDescription      fullDescription      bookImgUrl      pressImgUrl      productUrl      __typename    }    isSubscribed    isDailyQuestion    dailyRecordStatus    editorType    ugcQuestionId    style    __typename  }}",
            },
            headers=LeetCode_Headers,
            timeout=aiohttp.ClientTimeout(total=10),
        ) as response:
            logger.trace("response receiving")
            RawData = await response.json(content_type=None)
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
