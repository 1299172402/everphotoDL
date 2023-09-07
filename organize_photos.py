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

def move_picture(asset, dl_path):
    source_path = asset['source_path']

    source_folder, source_filename = os.path.split(source_path)
    source_folder = os.path.split(source_folder)[-1]
    source_folder = source_folder.replace('|', '_').replace('?', '_').replace('*', '_').replace('<', '_').replace('>', '_').replace(':', '_').replace('"', '_').replace('/', '_').replace('\\', '_')
    source_filename = source_filename.replace('|', '_').replace('?', '_').replace('*', '_').replace('<', '_').replace('>', '_').replace(':', '_').replace('"', '_').replace('/', '_').replace('\\', '_')

    current_filename = f"{asset['id']}.{asset['mime'].split('/')[1]}"

    if os.path.exists(f"{dl_path}/{source_folder}") == False:
        os.mkdir(f"{dl_path}/{source_folder}")
    
    if os.path.exists(f"{dl_path}/{current_filename}") == True:
        if os.path.exists(f"{dl_path}/{source_folder}/{source_filename}") == False:
            save_move(f"{current_filename}", f"{source_folder}/{source_filename}")
            os.rename(f"{dl_path}/{current_filename}", f"{dl_path}/{source_folder}/{source_filename}")
            print(f"[成功] {current_filename} 文件已整理到 {source_folder}/{source_filename}")
        else:
            print(f"[跳过] {current_filename} 当前路径已有同名文件 {source_folder}/{source_filename}")

def organize_picture():
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
                elif asset['source_path'] == "":
                    continue
                elif asset['source_path'].startswith('ios://'):
                    continue

                with ThreadPoolExecutor(max_workers=30) as executor:
                    executor.submit(move_picture, asset, dl_path)

def interface():
    os.system('cls')
    print("时光相册下载器")
    print("当前进度：5. 智能整理照片")
    print("")
    print("注意事项：")
    print("1. 将恢复文件的原始名称")
    print("2. 根据照片的原始路径，将照片整理到对应的文件夹中")
    print("3. 如果照片的上传路径中有同名文件，则会跳过")
    print("4. 从IOS端上传的照片无法获取原始路径，也将跳过")
    print("")
    print("是否开始整理：")
    print("1. 是")
    print("2. 否")
    choice = input("请输入数字：")
    if choice == "1":
        organize_picture()

if __name__ == '__main__':
    interface()