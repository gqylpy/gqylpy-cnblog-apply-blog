import uuid
import time
import requests

from tools import gen_path

from config import FE
from config import LOG_DIR
from config import DATETIME_FORMAT

_ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) ' \
      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'


def show_apply_status(cookies: str) -> int:
    """查看博客开通申请"""
    return requests.get(
        'https://passport.cnblogs.com/GetBlogApplyStatus.aspx',
        headers=gen_headers(cookies)
    ).text


def gen_headers(cookies: str) -> dict:
    return {
        'User-Agent': _ua + str(uuid.uuid4()),
        'Cookie': cookies
    }


def record_fail_reason(page_text: str):
    """记录失败原因"""
    filename = gen_path(LOG_DIR, f'{time.strftime(DATETIME_FORMAT)}.html')
    with open(filename, 'w', encoding=FE) as fp:
        fp.write(page_text)
