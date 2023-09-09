import os
import function.tools.config_io as config_io

style = "personal"

def display_dl_path(setting):
    path = config_io.load(setting)
    if path == "":
        print("当前下载路径：未设置")
    else:
        print("当前下载路径：", path)

def save_path(setting, path):
    if path == "":
        print("[跳过] 下载路径未更改")
    else:
        config_io.save(setting, path)
        print("[成功] 下载路径已更改为：", path)

def interface(type):
    global style
    style = type
    os.system('cls')
    print("时光相册下载器")
    if style == "personal":
        print("当前进度：2. 设置下载路径")
    elif style == "share":
        print("当前进度：8. 设置共享相册下载路径")
    print("")
    if style == "personal":
        display_dl_path('dl_path')
    elif style == "share":
        display_dl_path('share_dl_path')
    print("")
    print("注意事项：")
    print("1. 输入的下载路径为空时，下载路径保持不变")
    print("2. 下载路径请使用正斜杠“/”而不是反斜杠“\”")
    print("3. 请使用完整的下载路径")
    print("")
    path = input("请输入下载路径：")
    if style == "personal":
        save_path('dl_path', path)
    elif style == "share":
        save_path('share_dl_path', path)
    input("按回车键继续...")

if __name__ == '__main__':
    interface()