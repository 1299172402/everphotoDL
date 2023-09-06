import save_token
import set_dl_path
import get_original_message
import dl_picture

import os
import json

def load_token():
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config['token']

def load_dl_path():
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config['dl_path']

# a command line interface for the user to interact with the program
prev_choice = "0"
def interface():
    global prev_choice
    os.system('cls')

    print("时光相册下载器")
    print("作者：之雨")
    print("Github开源地址: https://github.com/1299172402/everphotoDL")
    print("")
    print("请按照以下步骤操作：")
    print("1. " + ("（上一次操作）" if prev_choice == "1" else "") + "登录时光相册" + f" {load_token()  } ")
    print("2. " + ("（上一次操作）" if prev_choice == "2" else "") + "设置下载路径" + f" {load_dl_path()} ")
    print("3. " + ("（上一次操作）" if prev_choice == "3" else "") + "下载原始数据")
    print("4. " + ("（上一次操作）" if prev_choice == "4" else "") + "批量下载图片和视频")
    print("0. 退出程序")
    print("请输入数字：")
    choice = input()
    prev_choice = choice
    if choice == "1":
        save_token.interface()
    elif choice == "2":
        set_dl_path.interface()
    elif choice == "3":
        get_original_message.interface()
    elif choice == "4":
        dl_picture.interface()
    elif choice == "0":
        return 'exit'
    else:
        print("请输入正确的数字")

if __name__ == '__main__':
    if not os.path.exists('config.json'):
        with open('config.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps({
                "token": "",
                "dl_path": "D:/EverPhoto"
            }, ensure_ascii=False, indent=4))
    
    res = ''
    while res != 'exit':
        res = interface()