# https://www.rosettacode.org/wiki/Maze_generation#Python

from random import shuffle, randrange, randint
import math


class MazeMaker:
    START = '*'
    END = 'x'

    def __init__(self, w=16, h=8):
        self.w = w
        self.h = h
        self.hasLineBreaks = True

    def make_maze(self):
        w = self.w
        h = self.h
        vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
        ver = [["#  "] * w + ['#'] for _ in range(h)] + [[]]
        hor = [["###"] * w + ['#'] for _ in range(h + 1)]

        def walk(x, y):
            vis[y][x] = 1

            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(d)
            for (xx, yy) in d:
                if vis[yy][xx]:
                    continue
                if xx == x:
                    hor[max(y, yy)][x] = "#  "
                if yy == y:
                    ver[y][max(x, xx)] = "   "
                walk(xx, yy)

        walk(randrange(w), randrange(h))

        s = ""
        for (a, b) in zip(hor, ver):
            if self.hasLineBreaks:
                s += ''.join(a + ['\n'] + b + ['\n'])
            else:
                s += ''.join(a + b)
        return s

    def add_exits(self, map_str):
        w = 3 * self.w + 1
        h = 2 * self.h + 1
        start_point = 1
        map_str = map_str[:start_point] + self.START + map_str[start_point+1:]
        if self.hasLineBreaks:
            exit_point = w * h + h - 2
        else:
            exit_point = w * h - 1
        map_str = map_str[:exit_point-1] + self.END + map_str[exit_point:]
        return map_str

    def add_charas(self, map_str, e=0, b=1):
        if e > 0:
            map_str = self.replace_chara_space(map_str, 'e', e)
        else:
            map_str = self.replace_chara_space(map_str, 'b', b)
        return map_str

    def replace_chara_space(self, map_str, chara_type, chara_number):
        w = 3 * self.w + 1
        last_point = len(map_str) - (w * 2)
        buffer = w * 5 # 5 bricks is the minimum distance from start
        replacement_type = ' ' if chara_type == 'e' else '#'
        while chara_number > 0:
            replacement = randint(buffer, last_point)
            if map_str[replacement:replacement+1] == replacement_type:
                map_str = map_str[:replacement] + \
                    chara_type + map_str[replacement+1:]
            else:
                continue
            chara_number -= 1
        return map_str

    def replace_empty(self, map_str):
        return map_str.replace(' ', '.')


if __name__ == '__main__':
    m = MazeMaker(w=8, h=7)
    m.hasLineBreaks = True
    map_str = m.make_maze()
    map_str = m.add_exits(map_str)
    map_str = m.add_charas(map_str, n=3)
    map_str = m.replace_empty(map_str)
    print(len(map_str))
    print(map_str)
