from functools import reduce

# # 把用户输入的不规范的英文名字，变为首字母大写，其他小写的规范名字。输入：['adam', 'LISA', 'barT']，输出：['Adam', 'Lisa', 'Bart']
# def normalize(name):
#     return name.title()
#
#
# res = map(normalize, ['adam', 'LISA', 'barT'])
# for name in res:
#     print(name)

# # 请编写一个prod()函数，可以接受一个list并利用reduce()求积：
# L = [3, 5, 7, 9, 11]
# # def prod_test(x, y):
# #     # 查看在reduce函数调用过程中的各个值
# #     print(x, '---')
# #     print(y, '===')
# #     return x * y
# # res = reduce(prod_test, L)
# # print(res)
# def prod(L):
#     def fn(x, y):
#         return x * y
#
#     # def char2num(s):
#     #     return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
#
#     return reduce(fn, map(int, L))
# res = prod(L)
# print(res)

# # 利用map和reduce编写一个str2float函数，把字符串'123.456'转换成浮点数123.456
# def str2float(s):
#     def fn(x, y):
#         return x * 10 + y
#
#     def char2num(s):
#         return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
#
#     return reduce(fn, map(char2num, s.replace(".", "")))
#
#
# s = "1234.567"
# if s.find(".") != -1:
#     print('str2float(\'%s\') =' % s, str2float(s) / pow(10, (len(s) - s.find(".") - 1)))
# else:
#     print('str2float(\'%s\') =' % s, str2float(s))

# def _odd_iter():
#     n = 1
#     while True:
#         n = n + 2
#         yield n
#
#
# def _not_divisible(n):
#     return lambda x: x % n > 0
#
#
# def primes():
#     yield 2
#     it = _odd_iter()  # 初始序列
#     while True:
#         n = next(it)  # 返回序列的第一个数
#         yield n
#         it = filter(_not_divisible(n), it)  # 构造新序列
#         # print(it)
#
#
# # 打印1000以内的素数:
# for n in primes():
#     if n < 1000:
#         # pass
#         print(n)
#     else:
#         break

# # 请用sorted()对上述列表分别按名字 和 分数排序：
# L = [('Dob', 75), ('Adam', 92), ('Cisa', 88), ('Bart', 66)]
#
#
# def by_name(t):
#     # print(t)
#     return t[0].lower()
#
#
# L1 = sorted(L, key=by_name)
# print(L1)
#
#
# def by_scort(t):
#     return t[1]
#
#
# L1 = sorted(L, key=by_scort, reverse=True)
# print(L1)

# def is_odd(n):
#     return n % 2 == 1
#
#
# L = list(filter(is_odd, range(1, 31)))
# print(L)
# L1 = list(filter(lambda x: x % 2 == 0, range(1, 31)))
# print(L1)

import logging

logging.basicConfig(level=logging.INFO)

s = '0'
n = int(s)
logging.info('n = %d' % n)
print(10 / n)
