# -*- coding: utf-8 -*-

"""

    Baidu zhidao searcher

"""

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

import requests
from lxml import html
from bs4 import BeautifulSoup


header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Connection': 'keep-alive'}

def parse_search(keyword, default_answer_select=2, timeout=2):
    """
    Parse BaiDu zhidao search

    only return the first `default_answer_select`

    :param keyword:
    :param default_answer_select:
    :return:
    """
    answerList = []
    params = {
        "lm": "0",
        "rn": "10",
        "pn": "0",
        "fr": "search",
        "ie": "gbk",
        "word": keyword.encode("gbk")
    }
    encoding = "gbk"

    url = "https://zhidao.baidu.com/search"
    resp = requests.get(url, params=params, timeout=timeout, headers=header)
    # url = 'https://zhidao.baidu.com/search?word=什么金属导电性最好'
    # resp = requests.get(url, headers=header)
    soupAll = BeautifulSoup(resp.content, 'lxml')
    bestAnswer = soupAll.select('#wgt-autoask > dd')
    if bestAnswer:
        answerList.append(bestAnswer.getText())
    otherAnswerList = soupAll.select('.list-inner > .list > .dl')
    for dl in otherAnswerList:
        soup = BeautifulSoup(str(dl), 'lxml')
        answers = soup.select('dd')
        for ddAnswer in answers:
            soupDD = BeautifulSoup(str(ddAnswer), 'lxml')
            da = soupDD.select('.i-answer-text')
            if da:
                if da[0].getText() == '答：':
                    answerList.append(ddAnswer.getText())
            else:
                text = soupDD.getText()
                if '回答者: ' not in text:
                    answerList.append(text)
    print(type(answerList))
    return answerList