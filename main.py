import function.A_save_token as A_save_token
import function.B_set_dl_path as B_set_dl_path
import function.C_get_meta as C_get_meta
import function.D_dl_picture as D_dl_picture

import function.E_organize_photos as E_organize_photos
import function.F_time_sort_photos as F_time_sort_photos
import function.G_revert_photo_path as G_revert_photo_path

import os
import function.tools.config_io as config_io

def interface():
    os.system('cls')

    print("时光相册下载器")
    print("作者：之雨")
    print("Github开源地址: https://github.com/1299172402/everphotoDL")
    print("")
    print("下载功能")
    print("请按照以下步骤一步步操作：")
    print("1. 登录时光相册" + f" {config_io.load('token')} ")
    print("2. 设置下载路径" + f" {config_io.load('dl_path')} ")
    print("3. 下载相册的元数据")
    print("4. 批量下载图片和视频")
    print("")
    print("整理功能")
    print("5. 智能整理照片（推荐）")
    print("6. 按时间整理")
    print("7. 恢复照片路径到整理前")
    print("")
    print("0. 退出程序")
    print("")
    print("请输入数字：")
    choice = input()
    if choice == "1":
        A_save_token.interface()
    elif choice == "2":
        B_set_dl_path.interface()
    elif choice == "3":
        C_get_meta.interface()
    elif choice == "4":
        D_dl_picture.interface()
    elif choice == "5":
        E_organize_photos.interface()
    elif choice == "6":
        F_time_sort_photos.interface()
    elif choice == "7":
        G_revert_photo_path.interface()
    elif choice == "0":
        return 'exit'
    else:
        print("请输入正确的数字")

if __name__ == '__main__':
    config_io.init()
    while True:
        res = interface()
        if res == 'exit':
            break