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

def dformatf(s: float):
    h, m, s = hms(s)
    if h > 0:
        return f"{h:d}h{m:02d}m{int(s):02d}s"
    elif m > 0:
        return f"{m:d}m{int(s):02d}s"
    elif s > 10:
        return f"{s:.1f}s"
    else:
        return f"{s:.2f}s"