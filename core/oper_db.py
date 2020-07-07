from tools import db
from tools import exec_sql


def fetch_not_apply_user() -> tuple:
    """获取未开通博客的用户"""
    return exec_sql(f'''
        SELECT id, cookie, username
        FROM user_cnblog
        WHERE home IS NULL
    ''', database=db.gqylpy)


def update_blog_path(uid: int, home_link: str) -> int:
    """插入博客路径"""
    return exec_sql(f'''
        UPDATE user_cnblog
        SET home = '{home_link}'
        WHERE id = {uid}
    ''', commit=True, database=db.gqylpy)
