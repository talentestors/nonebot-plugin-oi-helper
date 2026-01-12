import re
import json
import httpx
from datetime import datetime
from nonebot.log import logger
from .utils import save_json, dirs
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

# Configuration
QUERY_URL = "https://leetcode.cn/graphql"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://leetcode.cn/",
    "Origin": "https://leetcode.cn",
    "Connection": "keep-alive",
    "Sec-Ch-Ua-Mobile": "?0",
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "application/json",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

QUERY_DAILY = """
query CalendarTaskSchedule($days: Int!) {
    calendarTaskSchedule(days: $days) {
        dailyQuestions {
            name
            slug
            link
        }
    }
}
""".strip()

QUERY_DAILY_DETAILS = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    questionFrontendId
    boundTopicId
    title
    titleSlug
    content
    translatedTitle
    translatedContent
    difficulty
    topicTags {
      name
      slug
      translatedName
    }
  }
}
""".strip()


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=3, min=1, max=60),
    retry=retry_if_exception_type(
        (httpx.RequestError, httpx.HTTPStatusError, json.JSONDecodeError)
    ),
    reraise=True,
)
async def request_async(url, data, timeout=15.0):
    """Async HTTP request with retry and error handling"""
    async with httpx.AsyncClient(
        http2=True, headers=HEADERS, timeout=timeout
    ) as client:
        try:
            response = await client.post(url, json=data, follow_redirects=True)
            response.raise_for_status()

            # Check if response is JSON
            content_type = response.headers.get("content-type", "")
            if "application/json" not in content_type.lower():
                raise ValueError(f"Unexpected content type: {content_type}")

            return response.json()
        except httpx.HTTPStatusError as e:
            error_detail = e.response.text[:500] if e.response else "No response body"
            raise Exception(
                f"HTTP error {e.response.status_code}: {error_detail}"
            ) from e
        except json.JSONDecodeError as e:
            raise Exception(f"JSON decode error: {e.doc[:500]}") from e


def clean_html_content(html_content: str) -> str:
    """Clean HTML content by removing tags and special characters"""
    if not html_content:
        return ""

    text = html_content
    text = re.sub(r"\n", "", text)
    text = re.sub(r"\t", "", text)
    text = (
        text.replace("&nbsp;", " ")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&amp;", "&")
        .replace("&quot;", '"')
        .replace("&apos;", "'")
    )
    return text


async def run():
    """Async main function"""

    try:
        logger.info("Fetching fresh data from LeetCode...")
        question_data = {}
        try:
            # Fetch daily question information
            daily_response = await request_async(
                QUERY_URL,
                {
                    "operationName": "CalendarTaskSchedule",
                    "variables": {"days": 0},
                    "query": QUERY_DAILY,
                },
            )

            daily_questions = (
                daily_response.get("data", {})
                .get("calendarTaskSchedule", {})
                .get("dailyQuestions", [])
            )
            if not daily_questions:
                raise ValueError("No daily questions found in response")

            daily_question = daily_questions[0]

            # Fetch question details
            question_response = await request_async(
                QUERY_URL,
                {
                    "operationName": "questionData",
                    "variables": {"titleSlug": daily_question["slug"]},
                    "query": QUERY_DAILY_DETAILS,
                },
            )

            question_data = question_response.get("data", {}).get("question", {})
            if not question_data:
                raise ValueError("No question data found in response")
            # Clean and construct final data
            cleaned_content = clean_html_content(
                question_data.get("translatedContent", "")
            )

            data = {
                "id": question_data.get("questionFrontendId", ""),
                "title": question_data.get("title", ""),
                "title_zh": question_data.get("translatedTitle", ""),
                "slug": daily_question.get("slug", ""),
                "link": daily_question.get("link", ""),
                "content": clean_html_content(question_data.get("content", "")),
                "translatedContent": cleaned_content,
                "difficulty": question_data.get("difficulty", ""),
                "topicTags": [
                    {
                        "name": tag.get("name", ""),
                        "slug": tag.get("slug", ""),
                        "translatedName": tag.get("translatedName", ""),
                    }
                    for tag in question_data.get("topicTags", [])
                ],
                "date": datetime.now().strftime("%Y-%m-%d"),
                "timestamp": datetime.now().isoformat(),
            }
        except Exception:
            logger.warning("error! Will to use rollback_request")
            data = await rollback_request()

        if save_json(dirs.leetcode_daily, data):
            logger.success(f"Successfully saved to {dirs.leetcode_daily}")
            logger.info(f"Data preview: {str(data)[:120]}\n")
            logger.debug(f"Content: {data['translatedContent']}")
        else:
            logger.error("Failed to save data")

    except Exception as e:
        logger.error(f"Error in main process: {e}")
        raise e


@retry(
    stop=stop_after_attempt(2),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(
        (httpx.RequestError, httpx.HTTPStatusError, json.JSONDecodeError)
    ),
    reraise=True,
)
async def rollback_request(timeout=20.0):
    """Async HTTP request with retry and error handling"""
    async with httpx.AsyncClient(
        http2=True, timeout=timeout
    ) as client:
        try:
            response = await client.get(
                "https://raw.githubusercontent.com/talentestors/leetcode-daily-data/refs/heads/main/data/daily.json",
                follow_redirects=True,
            )
            response.raise_for_status()

            return response.json()
        except httpx.HTTPStatusError as e:
            error_detail = e.response.text[:500] if e.response else "No response body"
            raise Exception(
                f"HTTP error {e.response.status_code}: {error_detail}"
            ) from e
        except json.JSONDecodeError as e:
            raise Exception(f"JSON decode error: {e.doc[:500]}") from e
