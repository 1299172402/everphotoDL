import function.A_save_token as A_save_token
import function.B_set_dl_path as B_set_dl_path
import function.C_get_meta as C_get_meta
import function.D_dl_picture as D_dl_picture

import function.E_organize_photos as E_organize_photos
import function.F_time_sort_photos as F_time_sort_photos
import function.G_revert_photo_path as G_revert_photo_path

import function.H_get_share_meta as H_get_share_meta
import function.I_dl_shared_album as I_dl_shared_album
import function.J_sort_shared_album as J_sort_shared_album

import function.K_write_time as K_write_time

import os
import function.tools.config_io as config_io

def interface():
    os.system('cls')

    print("时光相册下载器")
    print("作者：之雨")
    print("Github开源地址: https://github.com/1299172402/everphotoDL")
    print("")
    print("请按照以下步骤一步步操作：")
    print("下载功能")
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
    print("共享相册")
    print("8. 设置共享相册下载路径" + f" {config_io.load('share_dl_path')} ")
    print("9. 下载共享相册的元数据")
    print("10. 批量下载共享相册的图片")
    print("11. 整理共享相册的信息、图片、视频、动态、评论、点赞")
    print("12. 恢复共享相册的路径到整理前")
    print("")
    print("13. 写入照片时间到文件信息")
    print("")
    print("0. 退出程序")
    print("")
    print("请输入数字：")
    choice = input()
    if choice == "1":
        A_save_token.interface()
    elif choice == "2":
        B_set_dl_path.interface(type = "personal")
    elif choice == "3":
        C_get_meta.interface()
    elif choice == "4":
        D_dl_picture.interface()
    elif choice == "5":
        E_organize_photos.interface()
    elif choice == "6":
        F_time_sort_photos.interface()
    elif choice == "7":
        G_revert_photo_path.interface(type = "personal")
    elif choice == "8":
        B_set_dl_path.interface(type = "share")
    elif choice == "9":
        H_get_share_meta.interface()
    elif choice == "10":
        I_dl_shared_album.interface()
    elif choice == "11":
        J_sort_shared_album.interface()
    elif choice == "12":
        G_revert_photo_path.interface(type = "share")
    elif choice == "13":
        K_write_time.interface()
    elif choice == "0":
        return 'exit'
    else:
        print("请输入正确的数字")
        print("按下回车键继续...")

if __name__ == '__main__':
    config_io.init()
    while True:
        res = interface()
        if res == 'exit':
            break