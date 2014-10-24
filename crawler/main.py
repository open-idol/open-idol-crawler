# coding=utf-8
import unicodecsv as csv
import requests as req
import lxml.html as html
import time
import emotion


def get_row(gall, page=1):
    url = 'http://gall.dcinside.com/board/lists/'
    resp = req.get(url, params={
        'id': gall,
        'page': page,
    })
    tree = html.fromstring(resp.content.decode('utf-8', 'ignore'))
    rows = tree.cssselect('.list_table table tr.tb')
    for row in rows:
        tds = row.cssselect('td')
        try:
            int(tds[0].text)
        except ValueError:
            continue

        yield tds[1].cssselect('a')[0].text, tds[3].text


if __name__ == '__main__':
    n_pages = 100
    galls = {
        u'푸조': 'Peugeot',
        u'현대차': 'hyundai_motor',
        u'아이폰': 'iphone',
        u'안드로이드': 'androidphone',
    }

    emotion_detector = emotion.Detector()

    for name, id in galls.items():
        f = open('%s_records.csv' % id, 'w+')
        w = csv.writer(f, encoding='utf-8')
        total_score = 0
        for page in range(n_pages):
            time.sleep(0.025)
            for title, date in get_row(gall=id, page=page):
                score = emotion_detector.get(title)
                total_score += score
                w.writerow([id, title, date, score])
                print score, title
        print name, total_score

    # emotion_builder = emotion.Builder()
    # for name, id in galls.items():
    #     for page in range(n_pages):
    #         for title, date in get_row(gall=id, page=page):
    #             print title
    #             emotion_builder.append(title)
    #
    # emotion_builder.save()
