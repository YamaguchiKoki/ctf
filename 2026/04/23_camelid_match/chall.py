import os, secrets

YES = '♡♧'
NO = '♧♡'
MID = '♡'
FLAG = os.getenv('FLAG', 'Alpaca{dummy}')

ANIMALS = [
    'alpacas',
    'llamas',
    'guanacos',
    'vicunas',
    'saiga antelopes',
    'markhors',
    'yaks',
    'reindeer',
    'musk oxen',
    'ibexes',
]


def rot(s, k):
    k %= len(s)
    return s[k:] + s[:k]


def enc(bit):
    return YES if bit else NO


def row(a, b):
    # 0なら♧♡, 1なら♡♧, MID=♡なので、♧:2個、♡:3個
    s = enc(a) + MID + enc(b)
    # a=0, b=0 ♡♧♡♧♡
    # a=0, b=1 ♡♧♡♡♧
    # a=1, b=0 ♧♡♡♧♡
    # a=1, b=1 ♧♡♡♡♧
    # 最大距離は2, a and bの時だけ距離1 rotでどこを境に入れ替えられてもこの距離は保存->距離1ならy, 2ならn
    s = s[1] + s[0] + s[2:]
    return rot(s, secrets.randbelow(5))


def main():
    for animal in ANIMALS:
        a = secrets.randbelow(2)
        b = secrets.randbelow(2)
        print(f'Do both Alice and Bob like {animal}? (y/n)')
        print("Open cards:", row(a, b))
        ans = input('> ').strip().lower()[:1]
        if ans not in {'y', 'n'}:
            print('Please answer with y or n.')
            return 1
        if ans != ('y' if (a and b) else 'n'):
            print('Wrong.')
            return 1

# aかつbならyを入力、そうでないならnを入力
    print(FLAG)
    return 0


if __name__ == '__main__':
    main()
