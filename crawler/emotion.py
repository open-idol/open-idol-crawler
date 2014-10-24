# coding=utf-8
from konlpy.tag import Kkma


filename = 'hys.txt'


def get_vs(line):
    korean_analyzer = Kkma()
    return [word for word, tag in korean_analyzer.pos(line) if tag in ['VA', 'VX', 'VC']]


class Builder(object):
    def __init__(self):
        self._words = []

    def append(self, line):
        self._words += get_vs(line)

    def save(self):
        unique_list = list(set(self._words))
        with open('hys.txt', 'w') as f:
            for word in unique_list:
                line = '%s\n' % word
                f.write(line.encode('utf-8'))


class Detector(object):
    def __init__(self):
        self._dict = {}
        with open(filename) as f:
            for line in f:
                line = line.decode('utf8').strip()
                splitted = line.split(' ', 1)
                if len(splitted) < 2:
                    continue
                self._dict[splitted[0]] = splitted[1]
        # print self._dict

    def get(self, line):
        score = 0
        vs = get_vs(line)
        for v in vs:
            e = self._dict.get(v, '')
            if e == '+':
                score += 1
            elif e == '-':
                score -= 1
        return score


# TODO : Builder, Detector 합치자..
class Emotion(object):
    pass