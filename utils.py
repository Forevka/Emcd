import itertools

def grouper(n, iterable):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk

def format_rate(rate: int) -> str:
    power = 1000
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T', 5: 'P', 6: 'E', 7: 'Z'}
    while rate > power:
        rate /= power
        n += 1
    return f'{round(rate, 2)} {power_labels[n]}h/s'