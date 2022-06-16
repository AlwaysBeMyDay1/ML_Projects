from collections import Counter

def get_reduplicated_num(list):
    counter = Counter(list)
    return dict(counter)