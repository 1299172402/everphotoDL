import os
import json

from concurrent.futures import ThreadPoolExecutor

import threading

lock = threading.Lock()

def save_move(source, target):
    with lock:
        with open('move_record.json', 'r', encoding='utf-8') as f:
            record = json.load(f)
        record.append({
            'source': source,
            'target': target
        })
        with open('move_record.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False, indent=4))

def move_picture(asset, sort, time, dl_path):
    current_filename = f"{asset['id']}.{asset['mime'].split('/')[1]}"

    _, source_filename = os.path.split(asset['source_path'])
    if source_filename == "":
        source_filename = current_filename
    elif asset['source_path'].startswith('ios://'):
        source_filename = current_filename
    else:
        source_filename = source_filename.replace('|', '_').replace('?', '_').replace('*', '_').replace('<', '_').replace('>', '_').replace(':', '_').replace('"', '_').replace('/', '_').replace('\\', '_')
    
    date_string = asset[sort]
    if time == "year":
        year = date_string.split('T')[0].split('-')[0]
        source_folder = year
    elif time == "month":
        year = date_string.split('T')[0].split('-')[0]
        month = date_string.split('T')[0].split('-')[1]
        source_folder = year + '-' + month
    elif time == "day":
        year = date_string.split('T')[0].split('-')[0]
        month = date_string.split('T')[0].split('-')[1]
        day = date_string.split('T')[0].split('-')[2]
        source_folder = year + '-' + month + '-' + day
        
    if os.path.exists(f"{dl_path}/{source_folder}") == False:
        os.mkdir(f"{dl_path}/{source_folder}")
    
    if os.path.exists(f"{dl_path}/{current_filename}") == True:
        if os.path.exists(f"{dl_path}/{source_folder}/{source_filename}") == False:
            save_move(f"{current_filename}", f"{source_folder}/{source_filename}")
            os.rename(f"{dl_path}/{current_filename}", f"{dl_path}/{source_folder}/{source_filename}")
            print(f"[成功] {current_filename} 文件已整理到 {source_folder}/{source_filename}")
        else:
            print(f"[跳过] {current_filename} 当前路径已有同名文件 {source_folder}/{source_filename}")

def organize_picture_upload(sort, time):
    dl_path = json.load(open('config.json', 'r', encoding='utf-8'))['dl_path']
    if os.path.exists('move_record.json') == False:
        with open('move_record.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps([], ensure_ascii=False, indent=4))

    for file in os.listdir('original_response'):
        with open(f'original_response/{file}', 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
            for asset in data["data"]["user_data"]["asset_list"]:
                if asset['deleted'] == True:
                    continue

                with ThreadPoolExecutor(max_workers=30) as executor:
                    executor.submit(move_picture, asset, sort, time, dl_path)

def interface():
    os.system('cls')
    print("时光相册下载器")
    print("当前进度：6. 按时间整理")
    print("")
    print("注意事项：")
    print("1. 将恢复文件的原始名称，IOS端上传的照片除外")
    print("2. 将照片整理到对应时间的文件夹中")
    print("3. 如果照片的保存的路径中有同名文件，将会跳过")
    print("")
    # print("正在检测是否整理过...")
    # if os.path.exists('move_record.json') == True:
    #     print("检测到move_record.json，已整理过")
    #     print("请先恢复照片路径到整理前，再进行整理")
    #     input("按回车键继续...")
    # print("")
    print("按上传时间整理还是按拍摄时间整理：")
    print("1. 按上传时间整理")
    print("2. 按拍摄时间整理")
    choice = input("请输入数字：")
    if choice == "1":
        sort = "uploadedAt"
    elif choice == "2":
        sort = "taken"
    else:
        print("请输入正确的数字")
        input("按回车键继续...")
        return
    print("")

    print("时间粒度：")
    print("1. 按年整理")
    print("2. 按月整理")
    print("3. 按日整理")
    choice = input("请输入数字：")
    if choice == "1":
        time = "year"
    elif choice == "2":
        time = "month"
    elif choice == "3":
        time = "day"
    else:
        print("请输入正确的数字")
        input("按回车键继续...")
        return
    print("")

    print("是否开始整理：")
    print("1. 是")
    print("2. 否")
    choice = input("请输入数字：")
    if choice == "1":
        organize_picture_upload(sort = sort, time = time)
        print("整理完成")
    else:
        print("已取消整理")
    input("按回车键继续...")

if __name__ == '__main__':
    interface()