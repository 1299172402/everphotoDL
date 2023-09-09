import os
import json
import hashlib
import sqlite3
import function.tools.config_io as config_io
import function.tools.everphotoAPI as everphotoAPI

from concurrent.futures import ThreadPoolExecutor

def check_md5(file_path, md5):
    with open(file_path, 'rb') as f:
        calc_md5 = hashlib.md5(f.read()).hexdigest()
        if md5 == calc_md5:
            return True
        else:
            return False

def download_picture(asset, token, dl_path, output_succeed):
    filename = f'{asset["id"]}.{asset["mime"].split("/")[1]}'
    filepath = f'{dl_path}/{filename}'

    if os.path.exists(filepath) == True:
        if check_md5(filepath, asset['md5']) == True:
            print(f'[跳过] {filename} 文件已下载，校验成功') if output_succeed == True else None
            return 'check_succeed'
    
    everphotoAPI.Download_Media(token, asset["id"], filepath)
    
    if check_md5(filepath, asset['md5']) == True:
        print(f'[成功] {filename} 文件下载成功，校验成功')
        return 'download_succeed'
    else:
        os.remove(filepath)
        print(f'[失败] {filename} 文件下载成功，校验失败，文件已删除')
        return 'download_fail'

def download_picture_process(token, dl_path, thread_num, output_succeed):
    if os.path.exists(dl_path) == False:
        os.makedirs(dl_path)
    with ThreadPoolExecutor(max_workers=thread_num) as executor:
        conn = sqlite3.connect('everphoto.db')
        c = conn.cursor()
        c.execute("SELECT json_data FROM shared_asset")
        data = c.fetchall()
        for item in data:
            item = json.loads(item[0])
            if item['deleted'] == True:
                continue
            executor.submit(download_picture, item, token, dl_path, output_succeed)

def interface():
    os.system('cls')
    print("时光相册下载器")
    print("当前进度：10. 批量下载共享相册的图片")
    print("")
    print("注意事项：")
    print("1. 请自行确认第9步下载共享相册的元数据是否完成")
    print("2. 如果未完成第9步，可能会导致下载失败")
    print("")
    print("是否开始下载：")
    print("1. 是")
    print("2. 否")
    choice = input("请输入数字：")
    if choice == "1":
        pass
    else:
        print("已取消下载")
        input("按回车键继续...")
        return
    print("正在加载token...")
    TOKEN = config_io.load("token")
    print("正在加载下载路径...")
    DL_PATH = config_io.load("share_dl_path")
    print("请输入同时下载数（默认为 16 ）：")
    thread_num = int(input() or 16)
    print("是否显示 [跳过] 的信息：")
    print("1. 是（默认）")
    print("2. 否")
    choice = input("请输入数字：") or "1"
    if choice == "1":
        output_succeed = True
    else:
        output_succeed = False
    print("正在添加下载列表...")
    download_picture_process(token = TOKEN, dl_path = DL_PATH, thread_num = thread_num, output_succeed = output_succeed)
    print("")
    print("下载完成")
    input('按下回车键继续...')

if __name__ == '__main__':
    interface()