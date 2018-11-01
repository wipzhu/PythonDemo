# txt = 'nothing is impossible'
# print(txt[12])
#
# txt2 = txt[13:] + ' I don\'t believe'
# print(txt2)
#
# length = len(txt)
# print(txt + '的长度是')
# print(len(txt2))
#
# letters = ['1', '2', '3', '4', '5', '6']
# letters[4:] = ['A', 'B', 'C']
# print(letters)

# a,b = 0,1
# while(b < 10):
#     print(b, sep='test', end='\n')
#     a,b = b,a+b
#
# i = 2 ** 10
# print('2^10 是：', i)
# print(156, 'test', '&')
#
# f = open('abc.txt', 'w')
# print('a', file=f)
#
# x = int(input("Please enter an integer: "))
# if (x > 10):
#     print('<10')
# elif (x < 20):
#     print('<20')
# else:
#     print('>= 10')
#
# word = ['cat', 'window', 'defenestrate']
# # for i in word:
# #     print(i, len(i))
# for w in word[:]:
#     # print(w)
#     if(len(w) > 6):
#         word.append(w)
# print(word)

#
# list = list(range(2, 16))
# for i in list[:]:
#     print(i, end=',')
#
# for i in range(2, 16):
#     for j in range(2, i):
#         if i % j == 0:
#             print(i, 'equals ', j, '*', i // j)
#             break
#     else:
#         print(i, 'is a prime number')
#
# for num in range(2, 18):
#     if num % 2 == 0:
#         print(num, 'is an even num')
#         continue
#     else:
#         print(num, 'is an odd num')

# def fib(n):
#     """Return a list containing the Fibonacci series up to n."""
#     a, b = 0, 1
#     retArr = []
#     while a < n:
#         # print(a, end=' ')
#         retArr.append(a)
#         a, b = b, a + b
#     return retArr
#
#
# print(fib(1800))

# def ask_ok(prompt, retries=4, comment='Yes or No, please!'):
#     while True:
#         ok = input(prompt)
#         if ok in ('Y', 'y', 'yes', 'Yes'):
#             return True
#         elif ok in ('N', 'No', 'Nop', 'Nope'):
#             return False
#         retries = retries - 1
#         # if (retries < 0):
#         #     raise OSError('uncooperative user')
#         print(comment)
#
#
# ask_ok('Do you really want to quit?')

# def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue'):
#     print("‐‐ This parrot wouldn't", action, end=' ')
#     print("if you put", voltage, "volts through it.")
#     print("‐‐ Lovely plumage, the", type)
#     print("‐‐ It's", state, "!")
#     
#     
# parrot(1000)                                          # 1 positional argument
# parrot(voltage=1000)                                  # 1 keyword argument
# parrot(voltage=1000000, action='VOOOOOM')             # 2 keyword arguments
# parrot(action='VOOOOOM', voltage=1000000)             # 2 keyword arguments
# parrot('a million', 'bereft of life', 'jump')         # 3 positional arguments
# parrot('a thousand', state='pushing up the daisies')  # 1 positional, 1 keyword

# def cheeseshop(kind, *arguments, **keywords):
#     # print("‐‐ Do you have any", kind, "?")
#     # print("‐‐ I'm sorry, we're all out of", kind)
#     for arg in arguments:
#         print(arg)
#     print("‐" * 40)
#     keys = sorted(keywords.keys())
#     for kw in keys:
#         print(kw, ":", keywords[kw])
# 
# cheeseshop("Limburger", "It's very runny, sir.",
#            "It's really very, VERY runny, sir.",
#            shopkeeper = "Michael Palin",
#            client = "John Cleese",
#            sketch = "Cheese Shop Sketch")

# def parrot(voltage, state='a stiff', action='voom'):
#      print("‐‐ This parrot wouldn't", action, end=' ')
#      print("if you put", voltage, "volts through it.", end=' ')
#      print("E's", state, "!")
#
# cars = ['baoma','benchi','aodi','dazhong']
# print(cars)
#
# print(sorted(cars, reverse=True))
#
# cars.sort()
# print(cars)
#
# for che in cars:
#      print(che.title() + '\'s show is so wonderful')
#      print("I can't wait to see your next trick, " + che.title() + ".\n")
#
# print("Thank you, everyone. That was a great magic show!")

# numList = range(1, 1000001)
# for num in numList:
#      print(num)
# print(sum(numList))

# numList = range(3,30,3)
# for num in numList:
#      print(num)

# numList = range(1,11)
# for num in numList:
#      print(num**2*num)

# 列表解析 值的立方
# list = [val**2*val for val in list(range(1,11))]
# print(list)
# tmp = list[1:6] #下表为1-5的元素
# tmp = list[-3:]
# s = 'usb'
# tmp = list[:]
# tmp.append(s.title())
# print(tmp)

# tuple = ('cai','mi','tang','mian')
# for i in tuple:
#      print(i.title())