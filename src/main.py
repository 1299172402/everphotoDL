from function.A_save_token import interface as A_save_token
from function.B_set_dl_path import interface as B_set_dl_path
from function.C_get_meta import interface as C_get_meta
from function.D_dl_picture import interface as D_dl_picture

from function.E_organize_photos import interface as E_organize_photos
from function.F_time_sort_photos import interface as F_time_sort_photos
from function.G_revert_photo_path import interface as G_revert_photo_path

from function.H_get_share_meta import interface as H_get_share_meta
from function.I_dl_shared_album import interface as I_dl_shared_album
from function.J_sort_shared_album import interface as J_sort_shared_album

from function.K_write_time import interface as K_write_time
from function.album_sort import interface as album_sort

import os
import traceback
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
        A_save_token()
    elif choice == "2":
        B_set_dl_path(type = "personal")
    elif choice == "3":
        C_get_meta()
    elif choice == "4":
        D_dl_picture()
    elif choice == "5":
        E_organize_photos()
    elif choice == "6":
        F_time_sort_photos()
    elif choice == "7":
        G_revert_photo_path(type = "personal")
    elif choice == "8":
        B_set_dl_path(type = "share")
    elif choice == "9":
        H_get_share_meta()
    elif choice == "10":
        I_dl_shared_album()
    elif choice == "11":
        J_sort_shared_album()
    elif choice == "12":
        G_revert_photo_path(type = "share")
    elif choice == "13":
        K_write_time()
    elif choice == "6.5":
        album_sort()
    elif choice == "0":
        return 'exit'
    else:
        print("请输入正确的数字")
        input("按下回车键继续...")

if __name__ == '__main__':
    config_io.init()
    while True:
        try:
            res = interface()
            if res == 'exit':
                break
        except Exception as e:
            print("程序出现异常，无法继续。出现的异常信息如下：")
            traceback.print_exc()
            input("按下回车键继续...")
        except KeyboardInterrupt as e:
            input("程序已手动终止。按下回车键继续...")
            break