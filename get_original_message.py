import requests
import os
import json
import time

def load_token():
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config['token']

def load_dl_path():
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config['dl_path']

def getupdates(cursor = "", token = ""):
    url = "https://openapi.everphoto.cn/sf/3/v4/GetUpdates"
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {token}",
    }

    retries = 0
    while retries < 10:
        try:
            res = requests.post(url, headers=headers, json={"cursor":cursor,"space_id":0}, timeout=5).json()
            return res
        except requests.Timeout:
            retries += 1
            print(f"\n[超时] 请求GetUpdates失败，重试中 ({retries}/10)")
            time.sleep(5)
    print("\n[失败] 请求GetUpdates失败，请重试")
    return None
        

def saveupdate(index, dat):
    if os.path.exists(f'original_response') == False:
        os.mkdir(f'original_response')
    with open(f'original_response/res-{index:0=5d}.json', "w", encoding="utf-8") as f:
        f.write(json.dumps(dat, ensure_ascii=False, indent=4))

def get_original_message(token):
    if os.path.exists('original_response') and os.listdir('original_response'):
        index = max(int(file[4:9]) for file in os.listdir('original_response') if file.startswith('res-'))
        with open(f'original_response/res-{index:0=5d}.json', 'r', encoding='utf-8') as f:
            res = json.load(f)
        if res['pagination']['has_more']:
            print("检测到已下载部分原始数据，将继续下载...")
            cursor = res['pagination']['next']
            print(f"\r正在获取第{index}页", end = '')
            res = getupdates(cursor = cursor, token = token)
            saveupdate(index, res) if res != None else None
        else:
            print("检测到已下载全部原始数据，是否要重新下载")
            print("1. 是")
            print("2. 否")
            choice = input("请输入选项：")
            if choice == '1':
                index = 1
                print(f"\r正在获取第{index}页", end = '')
                res = getupdates(cursor = "", token = token)
                saveupdate(index, res) if res != None else None
            else:
                return
    else:
        index = 1
        print(f"\r正在获取第{index}页", end = '')
        res = getupdates(cursor = "", token = token)
        saveupdate(index, res) if res != None else None
    
    try:
        while res["pagination"]["has_more"]:
            index += 1
            print(f"\r正在获取第{index}页", end = '')
            res = getupdates(res["pagination"]["next"], token)
            saveupdate(index, res) if res != None else None
        print("\n[成功] 所有原始数据获取完成")
    except:
        print("\n[失败] 获取原始数据失败，请重试")

def calc_picture_num():
    sum_image = 0
    delete_image = 0
    sum_video = 0
    delete_video = 0
    sum_other = 0
    delete_other = 0
    for file in os.listdir(f'original_response'):
        with open(f'original_response/{file}', 'r', encoding="utf-8") as f:
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
    print(f"图片总数：{sum_image}，已删除：{delete_image}，剩余：{sum_image - delete_image}")
    print(f"视频总数：{sum_video}，已删除：{delete_video}，剩余：{sum_video - delete_video}")
    print(f"其他总数：{sum_other}，已删除：{delete_other}，剩余：{sum_other - delete_other}")
    print(f"总计：{sum_image + sum_video + sum_other}，已删除：{delete_image + delete_video + delete_other}，剩余：{sum_image + sum_video + sum_other - delete_image - delete_video - delete_other}")

def interface():
    os.system('cls')
    print("时光相册下载器")
    print("当前进度：3. 下载原始数据")
    print("")
    print("注意事项：")
    print("1. 如果遇到 [失败] ，请重复下载原始数据，直到成功为止")
    print("2. [超时] 的情况系统会自动重试，无需手动操作")
    print("3. 如图片和视频的数量小于时光相册APP上显示的数量，请重试")
    print("")
    print("正在加载token...")
    TOKEN = load_token()
    print("")
    print("正在获取原始数据...")
    get_original_message(token = TOKEN)
    print("")
    print("正在根据当前原始数据计算图片数量...")
    calc_picture_num()
    print("")
    input('按下回车键继续...')

if __name__ == '__main__':
    interface()