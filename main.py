import save_token
import set_dl_path
import get_original_message
import dl_picture

import organize_photos
import time_sort_photos
import revert_photo_path

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
def interface():
    os.system('cls')

    print("时光相册下载器")
    print("作者：之雨")
    print("Github开源地址: https://github.com/1299172402/everphotoDL")
    print("")
    print("下载功能")
    print("请按照以下步骤一步步操作：")
    print("1. 登录时光相册" + f" {load_token()  } ")
    print("2. 设置下载路径" + f" {load_dl_path()} ")
    print("3. 下载相册的元数据")
    print("4. 批量下载图片和视频")
    print("")
    print("整理功能")
    print("5. 智能整理照片")
    print("6. 按时间整理")
    print("7. 恢复照片路径到整理前")
    print("")
    print("0. 退出程序")
    print("")
    print("请输入数字：")
    choice = input()
    if choice == "1":
        save_token.interface()
    elif choice == "2":
        set_dl_path.interface()
    elif choice == "3":
        get_original_message.interface()
    elif choice == "4":
        dl_picture.interface()
    elif choice == "5":
        organize_photos.interface()
    elif choice == "6":
        time_sort_photos.interface()
    elif choice == "7":
        revert_photo_path.interface()
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
    
    while True:
        res = interface()
        if res == 'exit':
            break