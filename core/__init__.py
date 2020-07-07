import time

from .apply_for_blog import sub_apply
from .shared import show_apply_status
from .oper_db import update_blog_path
from .oper_db import fetch_not_apply_user
from .blog_base_config import set_blog_path
from .blog_base_config import set_default_editor

from config import APPLY_WAIT_TIME
from config import WHILE_INTERVAL_TIME

dct = {}


def core():
    for uid, cookies, username in fetch_not_apply_user():
        page_text = show_apply_status(cookies)

        if '批准' in page_text:
            home_link = set_blog_path(cookies, username)
            set_default_editor(cookies)
            update_blog_path(uid, home_link)
            print(uid, username, '批准', '已设置主页和默认编辑器')

        elif '拒绝' in page_text:
            sub_apply(cookies)
            print(uid, username, '拒绝，已重新提交申请')

        elif '您还没有申请' in page_text:
            sub_apply(cookies)
            print(uid, username, '初次提交申请')

        elif '队列' in page_text:
            dct.setdefault(uid, time.time())
            print(uid, username, '等候处理')

        else:
            print('未知状态')

        if dct.get(uid) and time.time() - dct[uid] > APPLY_WAIT_TIME:
            sub_apply(cookies)
            del dct[uid]
            print(uid, username, '等候处理时间过长，已重新提交申请')


def main():
    while True:
        core()
        time.sleep(WHILE_INTERVAL_TIME)
