from collections import deque


def prettify_number(num: str) -> str:
    arr = list(num)
    result = deque([])
    count = 0
    for el in reversed(arr):
        if count == 3:
            count = 0
            result.appendleft(" ")
        count += 1
        result.appendleft(el)
    return "".join(result)
