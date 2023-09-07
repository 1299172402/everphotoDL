import os
import requests
import json
import hashlib

from concurrent.futures import ThreadPoolExecutor

def load_token():
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config['token']

def load_dl_path():
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config['dl_path']

def check_md5(file_path, md5):
    with open(file_path, 'rb') as f:
        calc_md5 = hashlib.md5(f.read()).hexdigest()
        if md5 == calc_md5:
            return True
        else:
            return False

def download_picture(asset, token, dl_path, output_succeed):
    if asset['deleted'] == True:
        return 'deleted'
    
    filename = f'{asset["id"]}.{asset["mime"].split("/")[1]}'
    filepath = f'{dl_path}/{filename}'

    if os.path.exists(filepath) == True:
        if check_md5(filepath, asset['md5']) == True:
            print(f'[跳过] {filename} 文件已下载，校验成功') if output_succeed == True else None
            return 'check_succeed'
        else:
            os.remove(filepath)
            print(f'[失败] {filename} 文件已下载，校验失败，文件已删除')
    
    # download
    url = f'https://media.everphoto.cn/origin/{asset["id"]}'
    headers = {
        "authorization": f"Bearer {token}", 
    }
    res = requests.get(url, headers=headers)
    with open(filepath, 'wb') as f:
        f.write(res.content)
    # check md5
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
        for file in os.listdir('original_response'):
            with open(f'original_response/{file}', 'r', encoding="utf-8") as f:
                data = json.load(f)
                for asset in data['data']['user_data']['asset_list']:
                    executor.submit(download_picture, asset, token, dl_path, output_succeed)

def interface():
    os.system('cls')
    print("时光相册下载器")
    print("当前进度：4. 批量下载图片")
    print("")
    print("正在检查第3步是否完成...")
    if os.path.exists('original_response') == False:
        print("第3步未完成，请先完成第3步下载原始数据")
        input('按下回车键继续...')
        return
    print("正在加载token...")
    TOKEN = load_token()
    print("正在加载下载路径...")
    DL_PATH = load_dl_path()
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