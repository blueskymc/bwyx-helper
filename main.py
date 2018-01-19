# -*- coding:utf-8 -*-


"""

    Xi Gua video Million Heroes

"""

import textwrap
import time
from argparse import ArgumentParser

from config import data_directory, hanwan_appcode
from config import default_answer_number
from core.android import analyze_current_screen_text, commit_answer
from core.baiduzhidao import zhidao_search
from core.baiduocr import analysis
from core.auto_match import match_words
from core.baiduzhidao_main import parse_search


def parse_args():
    parser = ArgumentParser(description="Million Hero Assistant")
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=5,
        help="default http request timeout"
    )
    return parser.parse_args()


def main(testfile):
    four_answers = False
    args = parse_args()
    timeout = args.timeout

    start = time.time()
    if testfile > -1:
        text_binary = analyze_current_screen_text(
            directory=data_directory,
            file_name=testfile + 1,
            test=True
        )
    else:
        text_binary = analyze_current_screen_text(
            directory=data_directory
        )
    end = time.time()
    print("处理图片时间 {0} 秒".format(end - start))
    keyword, q1, q2, q3, q4 = analysis(text_binary, four_answers=four_answers)
    # keyword = get_text_from_image(
    #     image_data=text_binary,
    #     appcode=hanwan_appcode
    # )
    if not keyword:
        print("text not recognize")
        return
    end = time.time()
    print("图片生成文本时间 {0} 秒".format(end - start))
    keyword = keyword.split(r".")[-1]
    keywords = keyword.split(" ")
    keyword = "".join([e.strip("\r\n") for e in keywords if e])
    print("guess keyword: ", keyword)
    # answers = zhidao_search(
    #     keyword=keyword,
    #     default_answer_select=default_answer_number,
    #     timeout=timeout
    # )
    answers = parse_search(
        keyword=keyword,
        default_answer_select=default_answer_number,
        timeout=timeout)
    end = time.time()
    print("获取答案时间 {0} 秒".format(end - start))
    answers = filter(None, answers)
    choose_answer = match_words(answers, (keyword, q1, q2, q3, q4), four_answers=four_answers)
    end = time.time()
    print("use {0} 秒".format(end - start))
    #x = input()
    # if x == 'ok':
    #     if choose_answer:
    #         commit_answer(choose_answer)


if __name__ == "__main__":
    test = False
    while test:
        for i in range(7):
            main(i)
    main(-1)
