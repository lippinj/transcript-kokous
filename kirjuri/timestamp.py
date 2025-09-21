def hms(s):
    h = int(s // 3600)
    s -= (h * 3600)
    m = int(s // 60)
    s -= (m * 60)
    return h, m, s


def tsformat(s: int):
    h, m, s = hms(s)
    return f"{h:02d}:{m:02d}:{int(s):02d}"


def tsformatf(s: float):
    h, m, s = hms(s)
    return f"{h:02d}:{m:02d}:{s:02.3f}"