# 记录所有的名片字典
card_list = []


def show_menu():
    """显示菜单"""
    print("*" * 50)
    print("欢迎使用【名片管理系统】 V1.0 \n")
    print("1:新增名片")
    print("2:显示全部")
    print("3:搜索名片")
    print("")
    print("0:退出程序")
    print("*" * 50)


def new_card():
    """新增一张名片"""
    print("-" * 50)
    print("功能:新增名片")
    # 提示用户输入名片的详细信息
    name_str = input("请输入姓名:")
    mobile = input("请输入电话号码:")
    qq_num = input("请输入QQ号:")
    email = input("请输入邮箱:")
    # 使用用户输入的信息建立一个名片字典
    card_dict = {
        "name": name_str,
        "mobile": mobile,
        "qq": qq_num,
        "email": email,
    }
    # 将名片字典添加到列表中
    card_list.append(card_dict)
    print(card_list)
    # 提示用户添加成功
    print("添加 %s 的名片成功!" % name_str)


def show_all():
    """显示全部名片"""
    print("功能:显示全部名片")
    # 判断名片列表中是否含有数据,没有的话则提示用户新增
    if len(card_list) == 0:
        print("当前没有名片，请选择新增功能进行新增！")
        return
    print("-" * 50)
    # 打印表头
    i = 0
    for name in ["姓名", "手机号码", "QQ", "邮箱"]:
        if i <= 3:
            print(name, end="\t\t\t")
        else:
            print(name)
    print("")
    print("+" * 50)
    # 遍历输出名片字典信息
    for card_dict in card_list:
        print("%s\t\t%s\t\t%s\t\t%s" % (card_dict['name'], card_dict['mobile'],
                                        card_dict['qq'], card_dict['email']))


def search_card():
    """搜索名片"""
    print("-" * 50)
    print("功能:搜索名片")

    # 提示用户要输如的姓名
    find_name = input("请输入要搜索的姓名:")

    # 查找用户，没查到则提示用户
    for card_dict in card_list:
        if card_dict['name'] == find_name:
            print("姓名\t\t电话号码\t\tQQ\t\t邮箱")
            print("=" * 50)
            print("%s\t\t%s\t\t%s\t\t%s" % (card_dict['name'], card_dict['mobile'],
                                            card_dict['qq'], card_dict['email']))
            # 针对找到的名片进行修改删除操作
            deal_card(card_dict)
            break
    else:
        print("对不起，没又找到" + find_name + "的名片信息")


def deal_card(find_dict):
    """
    处理名片信息
    :param find_dict:
    :return:
    """
    ac_str = input("请输入对该用户的操作:"
                   "[1] 修改/ [2] 删除/ [0] 返回上级菜单")
    if ac_str == "1":
        # 修改名片
        find_dict['name'] = input_cart_info(find_dict['name'], "修改姓名:")
        find_dict['mobile'] = input_cart_info(find_dict['mobile'], "修改手机号码:")
        find_dict['qq'] = input_cart_info(find_dict['qq'], "修改QQ:")
        find_dict['email'] = input_cart_info(find_dict['email'], "修改邮箱:")
    elif ac_str == "2":
        # 删除名片
        card_list.remove(find_dict)
    else:
        return


def input_cart_info(dict_value, tips):
    """
    输入名片信息
    :param dict_value:
    :param tips:
    :return:
    """
    # 提示输入内容
    result = input(tips)
    # 根据输入内容判断
    # 没有输入内容,返回`字典中原有内容`
    if len(result) <= 0:
        return dict_value
    else:
        return result
