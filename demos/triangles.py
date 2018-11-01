def triangles():
    """杨辉三角"""
    ret = [1]
    while True:
        yield ret
        pre = ret[:]
        for i in range(1, len(ret)):
            ret[i] = pre[i] + pre[i - 1]
        ret.append(1)
        if len(ret) >= 10:
            break
    return ret


for i in triangles():
    print(i)
