from functools import reduce


def gcd(a, b):
    """最大公约数"""
    r = a % b
    if r:
        return gcd(b, r)
    else:
        return b


# print gcd(13, 6)

def lcm(a, b):
    """最小公倍数"""
    return a * b / gcd(a, b)


# print lcm(12, 6)

def lcmAll(seq):
    """求多个数的最小公倍数"""
    # reduce()
    # 函数会对参数序列中元素进行累积。
    #
    # 函数将一个数据集合（链表，元组等）中的所有数据进行下列操作：用传给reduce中的函数
    # function（有两个参数）先对集合中的第1、2个元素进行操作，得到的结果再与第三个数据用
    # function 函数运算，最后得到一个结果。
    return reduce(lcm, seq)


in_num = int(input("请输入一个正整数n："))

# print(in_num)
lis = range(1, in_num + 1)
# print(lis)
# print(lcmAll(lis))

out_num = in_num
while True:
    out_num += 1
    if lcmAll(range(in_num + 1, out_num + 1)) == lcmAll(range(1, out_num + 1)):
        print("符合条件的m：" + str(out_num))
        break

# in_num = 12 时
# t = lcmAll(range(1, 23))
# print(t)
# s = lcmAll(range(13, 23))
# print(s)
