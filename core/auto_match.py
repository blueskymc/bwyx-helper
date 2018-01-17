import jieba
import textwrap
import Levenshtein
from core.baiduzhidao import zhidao_search
import core.baiduzhidao_main as bd_main

def match_words(answers, paras, four_answers=False):
    ask, q1, q2, q3, q4 = paras
    q1Count = 0
    q2Count = 0
    q3Count = 0
    q4Count = 0
    str = ''
    strList = []
    for ans in answers:
        ans = ans.replace("\u3000", "")
        s = "\n".join(textwrap.wrap(ans, width=40))
        str += s
        strList.append(s)

    #print(str)
    if len(strList) > 0:
        print('*' * 20 + '下面是推荐答案' + '*' * 20)
        print(strList[0])

    q1Count += str.count(q1)
    q2Count += str.count(q2)
    q3Count += str.count(q3)
    q4Count += str.count(q4)

    if not four_answers:
        q4Count = 0
    all = q1Count + q2Count + q3Count + q4Count
    if all == 0:
        # print('尝试使用莱文斯坦模糊匹配')
        # v1 = Levenshtein.distance(q1, str)
        # v2 = Levenshtein.distance(q2, str)
        # v3 = Levenshtein.distance(q3, str)
        # v4 = Levenshtein.distance(q4, str)
        #
        # q1Count = 1 / v1
        # q2Count = 1 / v2
        # q3Count = 1 / v3
        # q4Count = 1 / v4
        # all = q1Count + q2Count + q3Count + q4Count
        # print('A:%.2f%%' % (q1Count * 100 / all))
        # print('B:%.2f%%' % (q2Count * 100 / all))
        # print('C:%.2f%%' % (q3Count * 100 / all))
        # if four_answers:
        #     print('D:%.2f%%' % (q4Count * 100 / all))
        # print('共找到%d次' % all)

        print('结巴尝试：')
        wordlist_after_jieba = jieba.cut(str, cut_all=False)
        keylist_q1 = jieba.cut(q1, cut_all=False)
        keylist_q2 = jieba.cut(q2, cut_all=False)
        keylist_q3 = jieba.cut(q3, cut_all=False)
        keylist_q4 = jieba.cut(q4, cut_all=False)
        # keylist_q1 = list(q1)
        # keylist_q2 = list(q2)
        # keylist_q3 = list(q3)
        # keylist_q4 = list(q4)
        for s in wordlist_after_jieba:
            for q in keylist_q1:
                q1Count += s.count(q)
                q1Count += q.count(s)
            for q in keylist_q2:
                q2Count += s.count(q)
                q2Count += q.count(s)
            for q in keylist_q3:
                q3Count += s.count(q)
                q3Count += q.count(s)
            for q in keylist_q4:
                q4Count += s.count(q)
                q4Count += q.count(s)
        if not four_answers:
            q4Count = 0
        all = q1Count + q2Count + q3Count + q4Count
        if all == 0:
            return
        print('A:%.2f%%' % (q1Count * 100 / all))
        print('B:%.2f%%' % (q2Count * 100 / all))
        print('C:%.2f%%' % (q3Count * 100 / all))
        if four_answers:
            print('D:%.2f%%' % (q4Count * 100 / all))
        print('共找到%d次' % all)
    else:
        print('A:%.2f%%' % (q1Count * 100 / all))
        print('B:%.2f%%' % (q2Count * 100 / all))
        print('C:%.2f%%' % (q3Count * 100 / all))
        if four_answers:
            print('D:%.2f%%' % (q4Count * 100 / all))
        print('共找到%d次' % all)

    correct_answer = max(q1Count, q2Count, q3Count, q4Count)
    if q1Count == correct_answer:
        return 1
    elif q2Count == correct_answer:
        return 2
    elif q3Count == correct_answer:
        return 3
    elif q4Count == correct_answer:
        return 4

def main():
    ask = '变态性反应疾病属于哪种疾病'
    q1 = '外科'
    q2 = '过敏'
    q3 = '心理疾病'
    q4 = ''
    # ask = '我们常说的1080P中的字母P指的是什么意思'
    # q1 = '分辨率'
    # q2 = '逐行扫描'
    # q3 = '逐列扫描'
    # answers = zhidao_search(
    #     keyword=ask,
    #     default_answer_select=5,
    #     timeout=10
    # )
    answers = bd_main.parse_search(
        keyword=ask,
        default_answer_select=5,
        timeout=10
    )
    answers = filter(None, answers)
    match_words(answers, [ask, q1, q2, q3, q4])

if __name__ == "__main__":
    main()