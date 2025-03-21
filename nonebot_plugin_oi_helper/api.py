import requests
import aiohttp
import re
from nonebot.log import logger
from datetime import datetime, timedelta
from .utils import leetcode_locale_to_zh, load_json, save_json, dirs
from . import api_config


async def getContest():
    apikey = f"&username={api_config.username}&api_key={api_config.user_key}"
    url = f"{str(api_config.req_url)}" + apikey
    logger.info("GET " + url)
    resp = requests.get(url, timeout=12)
    resp.raise_for_status()
    logger.info("getContest SUCCESS " + str(resp.status_code))
    data = dict(resp.json())
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
    load_json.cache_clear()


async def getLuoguDaily():
    url = "https://www.craft.do/api/share/N0l80k2gv46Psq"
    logger.info("GET " + url)
    data = requests.get(url=url, timeout=10)
    data.raise_for_status()
    logger.info("getLuoguYuebao SUCCESS " + str(data.status_code))
    data = data.json()
    tmp = {block["id"]: block for block in data["blocks"]}

    top = data["blocks"][0]["id"]

    news = {}

    for title_id in tmp[top]["blocks"]:
        title = tmp[title_id]
        if "关键词" in title["content"]:
            continue
        year = int(title["content"].strip("年").strip())

        id = ""
        url = ""
        pos = 0
        up = len(title["blocks"])
        while pos < up:
            text = tmp[title["blocks"][pos]]["content"]

            if "月" in text:
                month = int(text.strip("月").strip(""))
                pos += 1

                text = tmp[title["blocks"][pos]]["content"].replace("\u3000", " ")

                while text.startswith("#"):
                    name = text
                    id = text.split(" ")[0]
                    pos += 1
                    url = tmp[title["blocks"][pos]]["content"]
                    news[id] = {"title": name, "url": url, "year": year, "month": month}
                    pos += 1
                    if pos >= up:
                        break
                    text = tmp[title["blocks"][pos]]["content"].replace("\u3000", " ")
            else:
                pos += 1

    save_json(dirs.luogu_news, news)
    load_json.cache_clear()


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
    load_json.cache_clear()
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
                logger.info("response receiving")
                RawData = await response.json(content_type=None)
                logger.info("response received")
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
            logger.info("response receiving")
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
        load_json.cache_clear()
    return data
