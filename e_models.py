def e_conventional(n):
    en = 0
    for i in range(1, n + 1):
        en = en + (2 ** (n + 1 - 2 * i) * (2 ** i - 1))
    return en


def e_monotonic(n):
    en = 0
    for i in range(1, n):
        en = en + (2 ** (n - 2 - i))
    return en


def e_mcs(n):
    en = 0
    for i in range(1, n):
        en = en + (2 ** (n - 2 - 2 * i) * (2 ** i - 1))
    return en


def e_cs(n):
    en = 2.0 ** (n - 1) - 1
    return en
