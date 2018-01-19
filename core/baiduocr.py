from aip import AipOcr

APP_ID = '10646355'
API_KEY = 'yGSQzcabg1Qb2ZHFAwVBuyMy'
SECRET_KEY = '3K0MSeFVLmWZ25FYFlVbMF5Pn52f42j1'

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def ocr(image):
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    #image = get_file_content(imagePath)
    ret = client.basicGeneral(image)
    if ret['words_result_num'] > 0:
        print('Image identify successful')
        return ret
    else:
        print('Image identify failed')


def analysis(image, four_answers=False):
    result = ocr(image)
    if result:
        ask = ''
        lines = result['words_result']
        # for line in lines:
        #     print(line['words'])

        q1, q2, q3, q4 = ('A', 'B', 'C', 'D')
        if four_answers:
            if len(lines) == 5:
                ask = lines[0]['words']
                q1 = lines[1]['words']
                q2 = lines[2]['words']
                q3 = lines[3]['words']
                q4 = lines[4]['words']
            elif len(lines) == 6:
                ask = lines[0]['words'] + lines[1]['words']
                q1 = lines[2]['words']
                q2 = lines[3]['words']
                q3 = lines[4]['words']
                q4 = lines[5]['words']
            elif len(lines) > 7:
                ask = lines[0]['words'] + lines[1]['words'] + lines[2]['words']
                q1 = lines[3]['words']
                q2 = lines[4]['words']
                q3 = lines[5]['words']
                q4 = lines[6]['words']
        else:
            if len(lines) == 4:
                ask = lines[0]['words']
                q1 = lines[1]['words']
                q2 = lines[2]['words']
                q3 = lines[3]['words']
            elif len(lines) == 5:
                ask = lines[0]['words'] + lines[1]['words']
                q1 = lines[2]['words']
                q2 = lines[3]['words']
                q3 = lines[4]['words']
            elif len(lines) > 5:
                ask = lines[0]['words'] + lines[1]['words'] + lines[2]['words']
                q1 = lines[3]['words']
                q2 = lines[4]['words']
                q3 = lines[5]['words']

        print('QUESTION:' + ask)
        if ':' in q1:
            q1 = q1[2:]
        if ':' in q2:
            q2 = q2[2:]
        if ':' in q3:
            q3 = q3[2:]
        if ':' in q4:
            q4 = q4[2:]
        print(ask)
        print(q1)
        print(q2)
        print(q3)
        return ask, q1, q2, q3, q4