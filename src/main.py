from function.save_token import interface as save_token
from function.set_dl_path import interface as set_dl_path
from function.get_meta import interface as get_meta
from function.dl_picture import interface as dl_picture
from function.organize_photos import interface as organize_photos
from function.time_sort_photos import interface as time_sort_photos
from function.revert_photo_path import interface as revert_photo_path
from function.get_share_meta import interface as get_share_meta
from function.dl_shared_album import interface as dl_shared_album
from function.sort_shared_album import interface as sort_shared_album
from function.write_time import interface as write_time
from function.album_sort import interface as album_sort

import os
import sys
from loguru import logger
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
    print("5. 写入照片时间到文件信息")
    print("6. 按相册整理")
    print("7. 智能整理照片（推荐）")
    print("8. 按时间整理到文件夹")
    print("9. 恢复照片路径到整理前")
    print("")
    print("共享相册")
    print("10. 设置共享相册下载路径" + f" {config_io.load('share_dl_path')} ")
    print("11. 下载共享相册的元数据")
    print("12. 批量下载共享相册的图片")
    print("13. 写入照片时间到文件信息")
    print("14. 整理共享相册的信息、图片、视频、动态、评论、点赞")
    print("15. 恢复共享相册的路径到整理前")
    print("")
    print("0. 退出程序")
    print("")
    choice = input("请输入数字：")

    # 下载功能
    if choice == "1":
        save_token()
    elif choice == "2":
        set_dl_path(type = "personal")
    elif choice == "3":
        get_meta()
    elif choice == "4":
        dl_picture()

    # 整理功能
    elif choice == "5":
        write_time(type = 'personal')
    elif choice == "6":
        album_sort()
    elif choice == "7":
        organize_photos()
    elif choice == "8":
        time_sort_photos()
    elif choice == "9":
        revert_photo_path(type = "personal")

    # 共享相册
    elif choice == "10":
        set_dl_path(type = "share")
    elif choice == "11":
        get_share_meta()
    elif choice == "12":
        dl_shared_album()
    elif choice == "13":
        write_time(type = 'share')
    elif choice == "14":
        sort_shared_album()
    elif choice == "15":
        revert_photo_path(type = "share")
    
    elif choice == "0":
        return 'exit'
    else:
        print("请输入正确的数字")

if __name__ == '__main__':
    # 移除默认的控制台处理器
    logger.remove()
    # 设置控制台的日志级别为WARNING
    logger.add(sys.stderr, level="WARNING")
    # 设置文件的日志级别为INFO
    logger.add("everphotoDL.log", encoding="utf-8", level="INFO")
    logger.info("程序启动")
    config_io.init()
    while True:
        try:
            res = interface()
            if res == 'exit':
                break
        except Exception as e:
            print("程序出现异常，无法继续。出现的异常信息如下：")
            logger.exception(e)
        except KeyboardInterrupt as e:
            print("程序已手动终止")
            logger.exception(e)
            break
        input("按下回车键继续...")
    logger.info("程序退出")
