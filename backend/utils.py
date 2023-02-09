


def win_rate(victories, played):
    return victories / played
    

def win_lose_ratio(func, victories, defeats):
    win_lose_ratio = 0
    if defeats == 0:
        win_lose_ratio = victories
    elif victories == 0:
        win_lose_ratio = 0.5 / defeats
    elif defeats == 1:
        win_lose_ratio = victories * (3 / 4)
    else:
        win_lose_ratio = victories / defeats
    return func(win_lose_ratio)


def beating_factor(victories, played):
    beating_factor = 0
    if victories == 0:
        beating_factor = (1 / played) / 2
    else:
        beating_factor = victories / played
    return beating_factor