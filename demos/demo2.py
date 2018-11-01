# age1 = 21
# age2 = 18
# print(age1 == age2)

# banned_users = ['andrew', 'carolina', 'david']
# user = 'andrew'
# if user in banned_users:
#     print(user.title() + ", you can post a response if you wish.")

# age = 17
# if age >= 18:
#     print("You are old enough to vote!")
#     print("Have you registered to vote yet?")
# elif age < 16:
#     print("You are too young , too simple")
# else:
#     print("Sorry, you are too young to vote.")
#     print("Please register to vote as soon as you turn 18!")
# age = 12
# if age < 4:
#     price = 0
# elif age < 18:
#     price = 5
# elif age < 65:
#     price = 10
# elif age >= 65:
#     price = 5
# print("Your admission cost is $" + str(price) + ".")
# alien_color = 'yellow'
# if alien_color == 'green':
#     print("You have killed an alien, score added 5")
# elif alien_color == 'yellow':
#     print("score added 10")
# elif alien_color == 'blue':
#     print("score added 15")

# fruit = 'watermelon'
# favorite_fruits = ['apple', 'banana', 'orange', 'purple']
# if fruit in favorite_fruits:
#     print('You really like ' + fruit)
# elif fruit not in favorite_fruits:
#     print('You seem not like ' + fruit)

# requested_toppings = ['mushrooms', 'green peppers', 'extra cheese']
# for requested_topping in requested_toppings:
#     if requested_topping == 'green peppers':
#         print("Sorry, we are out of " + requested_topping + " right now.")
#     else:
#         print("Adding " + requested_topping + ".")
# print("\nFinished making your pizza!")

# available_toppings = ['mushrooms', 'olives', 'green peppers',
#                       'pepperoni', 'pineapple', 'extra cheese']
# requested_toppings = ['mushrooms', 'french fries', 'extra cheese']
# for requested_topping in requested_toppings:
#     if requested_topping in available_toppings:
#         print("Adding " + requested_topping + ".")
#     else:
#         print("Sorry, we don't have " + requested_topping + ".")
# print("\nFinished making your pizza!")
#
# current_user = ['John', 'Jack', 'BOb', 'Alice']
# new_users = ['Cuily', 'Jack', 'Jack Ma', 'viaha']
# for new_user in new_users:
#     if current_user:
#         if new_user in current_user:
#             print("Sorry," + new_user+" is already exist")
#         else:
#             print("Congratulation,"+new_user+" is available")
#     else:
#         print('Sorry,we need some users')

# list = list(range(1,11))
# for i in list:
#     if i == 1:
#         print('1st')
#     elif i == 2:
#         print('2nd')
#     elif i == 3:
#         print('3rd')
#     else:
#         print(str(i) + 'th')

# alien_0 = {'color': 'green', 'points': 5}
#
# print(alien_0['color'])


# def add_list(alist):
#     for i in alist:
#         yield i + 1
#
#
# alist = [1, 2, 3, 4]
# for x in add_list(alist):
#     print(x)


# 图灵机器人
from wxpy import *

turing = Tuling(api_key='dc950b4863e44dbb816e362b218f3114')
bot = Bot()
limit = bot.friends().search('星宇')
# limit = bot.groups().search('We Are 伐木累')


@bot.register(chats=limit)
def communicate(msg):
    turing.do_reply(msg)


bot.join()
