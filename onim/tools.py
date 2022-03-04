def level(char):
    if char in ['p', 't', 'k', 'v', 'q', 'h', 'f', '']:
        return 8
    if char in ['s', 'x']:
        return 7
    if char in ['b', 'd', 'g', 'c']:
        return 6
    if char in ['z']:
        return 5
    if char in ['l', 'm', 'n', 'r', 'w', 'j']:
        return 4
    if char in ['u', 'o']:
        return 3
    if char in ['i', 'e', 'y']:
        return 2
    if char in ['a']:
        return 1
    return -1


def word_levels(word):
    ret = []
    for char in word:
        ret.append(level(char))  #
        # ret.append(ord(char)-ord('a'))    # an alternative option
    ret += [-1] * (12 - len(word))  # 12 is max word len
    return ret
