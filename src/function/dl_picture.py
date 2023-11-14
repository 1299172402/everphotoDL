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

def download_picture(asset, token, dl_path):
    filename = f'{asset["id"]}.{asset["mime"].split("/")[1]}' if asset['mime'] != '' else f'{asset["id"]}.{asset["subType"]}'
    filepath = f'{dl_path}/{filename}'

    if os.path.exists(filepath) == True:
        # 跳过已下载并校验正确的文件
        if check_md5(filepath, asset['md5']) == True:
            return 'check_succeed'
        # 删除曾经下载但校验失败的文件，之后将重新下载
        else:
            os.remove(filepath)
    
    if everphotoAPI.Download_Media(token, asset["id"], filepath) == True:
        pass
    else:
        print(f'[失败] {filename} 文件下载失败')
    
    if check_md5(filepath, asset['md5']) == True:
        print(f'[成功] {filename} 文件下载成功，校验成功')
        return 'download_succeed'
    else:
        print(f'[失败] {filename} 文件下载成功，校验失败')
        return 'download_fail'

def download_picture_process(token, dl_path, thread_num):
    if os.path.exists(dl_path) == False:
        os.makedirs(dl_path)
    with ThreadPoolExecutor(max_workers=thread_num) as executor:
        conn = sqlite3.connect('everphoto.db')
        c = conn.cursor()
        c.execute("SELECT json_data FROM personal_asset")
        data = c.fetchall()
        for item in data:
            item = json.loads(item[0])
            if item['deleted'] == True:
                continue
            executor.submit(download_picture, item, token, dl_path)

def interface():
    os.system('cls')
    print("时光相册下载器")
    print("当前进度：4. 批量下载图片")
    print("")
    print("注意事项：")
    print("1. 请先完成第3步，下载相册的元数据")
    print("2. 重新执行本步骤可以重新下载，支持断点续传")
    print("3. 校验失败时可以尝试调小同时下载数")
    print("4. 如果直接提示“下载完成”，说明所有照片都已经正常下载完毕")
    print("")
    print("正在加载token...")
    TOKEN = config_io.load("token")
    print("正在加载下载路径...")
    DL_PATH = config_io.load("dl_path")
    thread_num = int(input("请输入同时下载数(默认为16): ") or 16)
    print("")
    print("正在添加下载列表...")
    download_picture_process(token = TOKEN, dl_path = DL_PATH, thread_num = thread_num)
    print("")
    print("下载完成")

if __name__ == '__main__':
    interface()