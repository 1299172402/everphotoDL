import os
import json

def show_current_download_path():
    with open("config.json", "r") as f:
        config = json.load(f)
    if config["dl_path"] == "":
        print("当前下载路径：未设置")
    else:
        print("当前下载路径：", config["dl_path"])

def save_path(path):
    with open("config.json", "r") as f:
        config = json.load(f)
    if path == "":
        print("[跳过] 下载路径未更改")
    else:
        config["dl_path"] = path
        with open("config.json", "w") as f:
            f.write(json.dumps(config, ensure_ascii=False, indent=4))
        print("[成功] 下载路径已更改为：", path)

def interface():
    os.system('cls')
    print("时光相册下载器")
    print("当前进度：2. 设置下载路径")
    print("")
    show_current_download_path()
    print("")
    print("注意事项：")
    print("1. 输入的下载路径为空时，下载路径保持不变")
    print("2. 下载路径请使用正斜杠“/”而不是反斜杠“\”")
    print("3. 请使用完整的下载路径")
    print("")
    path = input("请输入下载路径：")
    save_path(path)
    input("按回车键继续...")

if __name__ == '__main__':
    interface()