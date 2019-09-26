#!
import cards_tools as tools

while True:
    # TODO 显示功能菜单
    tools.show_menu()

    input_str = input("请选择希望执行的操作：")
    print("您选择的操作是：【%s】" % input_str)

    if input_str in ['1', '2', '3']:
        # 新增
        if input_str == "1":
            tools.new_card()
        # 显示全部
        elif input_str == "2":
            tools.show_all()
        # 查询
        else:
            tools.search_card()
    elif input_str == "0":
        print("欢迎再次使用【名片管理系统】")
        break
    else:
        print("您输入的操作不正确，请重新输入！")