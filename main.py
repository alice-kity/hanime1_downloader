from hanime_xf_info  import get_hanime_xfyg_info
from download_nfo_img  import sc_nfo_jpg
from download_move  import db_get_lfid
from download_move  import download_html
import os

def option1_1():
    print("\033[34m#\033[0m" * 40)
    user_input = input("请输入年月如（202504）: ") or 202504
    get_hanime_xfyg_info(user_input)
    



 
def option1_2():
    print("\033[34m#\033[0m" * 40)
    user_input = input("请输入年月如（202504）: ") or 202504
    if not os.path.exists(str(user_input)):
        os.mkdir(str(user_input))
        print(f"目录 '{str(user_input)}' 已创建。")
    else:
        print(f"目录 '{str(user_input)}' 已存在。")
    sc_nfo_jpg(str(user_input))
 
def option1_3():
    print("\033[34m#\033[0m" * 40)
    user_input = input("请输入年月如（202504）: ") or 202504
    if not os.path.exists(str(user_input)):
        os.mkdir(str(user_input))
        print(f"目录 '{str(user_input)}' 已创建。")
    else:
        print(f"目录 '{str(user_input)}' 已存在。")
    lf_data=db_get_lfid(str(user_input))
    if lf_data:
        for row in lf_data:
            #里番id
            LF_ID = row[0]
            #里番日文名
            LF_NAME_CN=row[1]
            #print(tags)
            print(LF_ID,LF_NAME_CN) 
            download_html (LF_ID,str(user_input))  




def option1_4():
    global state
    state = False




 
options1 = {
    '1': option1_1,
    '2': option1_2,
    '3': option1_3,
    '4': option1_4,


}

#合集过滤条件

state = True
# 主程序
while state:
    # 显示菜单
    print("\033[34m#\033[0m" * 40)
    print("\033[33m欢迎使用hanime1里番下载器\033[0m")
    print("\033[34m#\033[0m" * 40)
    print("\033[33m1. 获取里番信息并写入SQLite3数据库\033[0m")
    print("\033[33m2. 生成nfo和图片\033[0m")
    print("\033[33m3. 下载SQLite3数据库中的里番\033[0m")
    print("\033[33m4. 退出\033[0m")
    print("\033[34m#\033[0m" * 40)
    
    # 获取用户输入
    user_input = input("请输入数字: ").strip()
    
    if user_input in options1:
        # 调用对应的函数
        options1[user_input]()  # 假设options1是一个字典，键是字符串，值是函数
    else:
        print("\033[31m无效的输入，请重新输入！\033[0m")



