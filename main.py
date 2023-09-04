import requests
import time
import os
import json
import hashlib
from multiprocessing import Pool

# 下载路径
DL_PATH = r"D:\EverPhoto"
# 下载令牌
DL_TOKEN = "Bearer ABCDEFGHIJKLMNOPQRSTUVWX"
# 下载线程数
DL_THREAD = 16
# 不显示下载完成的输出
DL_SKIP_NOTICE = False
# 只校验MD5，不下载文件
DL_ONLY_CHECK_MD5 = False

def log(msg, end = "\n"):
    if msg.startswith('\r'):
        print(f'\r[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] {msg[1:]}', end = end)
    else:
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] {msg}', end = end)

# Step 1: Get original message and calculate the number of pictures

def getupdates(cursor = ""):
    url = "https://openapi.everphoto.cn/sf/3/v4/GetUpdates"
    headers = {
        "content-type": "application/json",
        "authorization": DL_TOKEN, 
    }

    from requests.exceptions import Timeout
    retries = 0
    while retries < 10:
        try:
            res = requests.post(url, headers=headers, json={"cursor":cursor,"space_id":0}, timeout=5).json()
            return res
        except Timeout:
            retries += 1
            log(f"Request timed out. Retrying... ({retries}/10)")
            time.sleep(5)
    raise Exception("Request failed after 10 retries.")

def saveupdate(index, dat):
    if os.path.exists(f'{DL_PATH}') == False:
        os.mkdir(f'{DL_PATH}')
    if os.path.exists(f'{DL_PATH}/01-original_response') == False:
        os.mkdir(f'{DL_PATH}/01-original_response')
    with open(f'{DL_PATH}/01-original_response/res-{index:0=5d}.json', "w", encoding="utf-8") as f:
        f.write(json.dumps(dat, ensure_ascii=False, indent=4))

def calc_picture_num():
    sum_image = 0
    delete_image = 0
    sum_video = 0
    delete_video = 0
    sum_other = 0
    delete_other = 0
    for file in os.listdir(f'{DL_PATH}/01-original_response'):
        with open(f'{DL_PATH}/01-original_response/{file}', 'r', encoding="utf-8") as f:
            data = json.load(f)
            for asset in data['data']['user_data']['asset_list']:
                if asset['mime'].startswith('image'):
                    sum_image += 1
                    if asset['deleted'] == True:
                        delete_image += 1
                elif asset['mime'].startswith('video'):
                    sum_video += 1
                    if asset['deleted'] == True:
                        delete_video += 1
                else:
                    sum_other += 1
                    if asset['deleted'] == True:
                        delete_other += 1
    log(f"图片总数：{sum_image}，已删除：{delete_image}，剩余：{sum_image - delete_image}")
    log(f"视频总数：{sum_video}，已删除：{delete_video}，剩余：{sum_video - delete_video}")
    log(f"其他总数：{sum_other}，已删除：{delete_other}，剩余：{sum_other - delete_other}")
    log(f"总计：{sum_image + sum_video + sum_other}，已删除：{delete_image + delete_video + delete_other}，剩余：{sum_image + sum_video + sum_other - delete_image - delete_video - delete_other}")

def get_original_message():
    index = 1
    res = getupdates()
    saveupdate(index, res)
    while res["pagination"]["has_more"] == True:
        index = index + 1
        res = getupdates(res["pagination"]["next"])
        saveupdate(index, res)
        log(f"\r正在获取第{index}页", end = "")
    log("\n获取完成")
    calc_picture_num()



def download_picture(asset):
    # check if file exists
    if asset['deleted'] == True:
        return 'deleted'
    
    # check md5
    if os.path.exists(f'{DL_PATH}/02-download_picture/{asset["id"]}.{asset["mime"].split("/")[1]}') == True:
        with open(f'{DL_PATH}/02-download_picture/{asset["id"]}.{asset["mime"].split("/")[1]}', 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
            if md5 == asset['md5']:
                log(f'[跳过] {asset["id"]} 文件已下载，校验成功') if DL_SKIP_NOTICE == True else None
                return 'check_succeed'
            else:
                log(f'[失败] {asset["id"]} 文件已下载，校验失败') if DL_ONLY_CHECK_MD5 == True else None
                return 'check_fail'
    else:
        log(f'[不在] {asset["id"]} 文件未下载')  if DL_ONLY_CHECK_MD5 == True else None

    # only check md5
    if DL_ONLY_CHECK_MD5 == True:
        return 'only_check_md5'
    
    # download
    url = f'https://media.everphoto.cn/origin/{asset["id"]}'
    headers = {
        "authorization": DL_TOKEN, 
    }
    res = requests.get(url, headers=headers)
    with open(f'{DL_PATH}/02-download_picture/{asset["id"]}.{asset["mime"].split("/")[1]}', 'wb') as f:
        f.write(res.content)
    # check md5
    with open(f'{DL_PATH}/02-download_picture/{asset["id"]}.{asset["mime"].split("/")[1]}', 'rb') as f:
        md5 = hashlib.md5(f.read()).hexdigest()
        if md5 == asset['md5']:
            log(f'[成功] {asset["id"]} 文件下载成功，校验成功')
            return 'download_succeed'
        else:
            os.remove(f'{DL_PATH}/02-download_picture/{asset["id"]}.{asset["mime"].split("/")[1]}')
            log(f'[失败] {asset["id"]} 文件下载成功，校验失败')
            return 'download_fail'

def download_picture_process():
    if os.path.exists(f'{DL_PATH}/02-download_picture') == False:
        os.mkdir(f'{DL_PATH}/02-download_picture')

    with Pool(processes=16) as pool:
        for file in os.listdir(f'{DL_PATH}/01-original_response'):
            with open(f'{DL_PATH}/01-original_response/{file}', 'r', encoding="utf-8") as f:
                data = json.load(f)
                for asset in data['data']['user_data']['asset_list']:
                    pool.apply_async(download_picture, (asset, ))
        pool.close()
        pool.join()

if __name__ == "__main__":
    get_original_message()
    calc_picture_num() # optional
    download_picture_process()