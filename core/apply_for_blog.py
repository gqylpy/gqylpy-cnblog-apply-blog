import json
import random
import requests

from .shared import gen_headers
from .shared import record_fail_reason

from tools import gen_path

from config import FE
from config import DB_DIR


def load_db(filename: str) -> list:
    with open(gen_path(DB_DIR, filename), encoding=FE) as fp:
        return json.load(fp)


_apply_reason = load_db('apply_reason.json')
_real_name = load_db('real_name.json')
_position = load_db('position.json')
_company = load_db('company.json')
_hobby = load_db('hobby.json')


def _gen_data():
    return {
        '__VIEWSTATE': 'xUYd9hvlmOBVwpbsVn4LCYLAq6940c2v0WMTXfufRc+Th3Yp19VdJ3iTbGnH2KxUPg/ikBt/9fIG1JkiKA4N4lXDMqqzQbHsk2xmfmUtfrS9ISvsRwNdmXfhjNJnxDAlhU+Yi2ND9TJ/H0k/cdBpSxLOdraI3T0ufbsx/P2b27+KzYbcbcWg2ATDsLG8353dkmUtKO5P6jwO/IozN6T0NVpYiTI=',
        '__VIEWSTATEGENERATOR': '37661959',
        '__EVENTVALIDATION': 'Tj3HXwMfHmaRDDAkfnuayLUCLE4HvPVXisSFGYllA74szhyQVxmNCPTu8+OD/h9wmGk+LTgGw4DR3eA9wS9u2FAz/y3qHDRmvY2hJ1DSkVf7xucuJOHfiXEZYVbEGmjKiv0oq44Tq80GUBYedc/xsU8iG1F9kqV6e72W3w2LBo0fhsQFHiNrYfceG0RA2NrdYNzyeQ1zeS/CCGPFSVnTY1ReYP4=',
        'ctl00$holderLeft$tbReason': random.choice(_apply_reason),
        'ctl00$holderLeft$txt_RealName': random.choice(_real_name),
        'ctl00$holderLeft$txt_Position': random.choice(_position),
        'ctl00$holderLeft$txt_Unit': random.choice(_company),
        'ctl00$holderLeft$txt_FavoriteTech': random.choice(_hobby),
        'ctl00$holderLeft$btn_submit': '提交'
    }


def sub_apply(cookies: str) -> bool:
    """提交博客开通申请"""
    response = requests.post(
        'https://passport.cnblogs.com/BlogApply.aspx',
        headers=gen_headers(cookies), data=_gen_data()
    )
    if '博客开通申请提交成功' in response.text:
        return True

    record_fail_reason(response.text)
    return False
