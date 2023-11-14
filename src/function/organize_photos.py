import os
import json
import sqlite3

import function.tools.config_io as config_io

def organize_picture():
    dl_path = config_io.load("dl_path")
    conn = sqlite3.connect('everphoto.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS personal_move_record (source TEXT, target TEXT)''')
    conn.commit()

    c.execute("SELECT json_data FROM personal_asset")
    data = c.fetchall()
    for asset in data:
        asset = json.loads(asset[0])
        if asset['deleted'] == True:
            continue
        elif 'source_path' not in asset.keys():
            continue
        elif asset['source_path'] == "":
            continue
        elif asset['source_path'].startswith('ios://'):
            continue

        source_path = asset['source_path']

        source_folder, source_filename = os.path.split(source_path)
        source_folder = os.path.split(source_folder)[-1]
        source_folder = source_folder.replace('|', '_').replace('?', '_').replace('*', '_').replace('<', '_').replace('>', '_').replace(':', '_').replace('"', '_').replace('/', '_').replace('\\', '_')
        source_filename = source_filename.replace('|', '_').replace('?', '_').replace('*', '_').replace('<', '_').replace('>', '_').replace(':', '_').replace('"', '_').replace('/', '_').replace('\\', '_')

        current_filename = f"{asset['id']}.{asset['mime'].split('/')[1]}" if asset['mime'] != '' else f"{asset['id']}.{asset['subType']}"

        if os.path.exists(f"{dl_path}/{source_folder}") == False:
            os.mkdir(f"{dl_path}/{source_folder}")
        
        if os.path.exists(f"{dl_path}/{current_filename}") == True:
            if os.path.exists(f"{dl_path}/{source_folder}/{source_filename}") == False:
                c.execute("INSERT INTO personal_move_record VALUES (?, ?)", (f"{current_filename}", f"{source_folder}/{source_filename}"))
                os.rename(f"{dl_path}/{current_filename}", f"{dl_path}/{source_folder}/{source_filename}")
                print(f"[成功] {current_filename} 文件已整理到 {source_folder}/{source_filename}")
            else:
                print(f"[跳过] {current_filename} 当前路径已有同名文件 {source_folder}/{source_filename}")
    conn.commit()
    conn.close()

def interface():
    os.system('cls')
    print("时光相册下载器")
    print("当前进度：7. 智能整理照片（推荐）")
    print("")
    print("注意事项：")
    print("1. 将恢复文件的原始名称")
    print("2. 根据照片的原始路径，将照片整理到对应的文件夹中")
    print("3. 如果照片的上传路径中有同名文件，则会跳过")
    print("4. 从IOS端上传的照片无法获取原始路径和原始文件名，也将跳过")
    print("5. 支持断点续传")
    print("")
    print("是否开始整理：")
    print("1. 是")
    print("2. 否")
    choice = input("请输入数字：")
    if choice == "1":
        organize_picture()
        print("整理完成")
    else:
        print("已取消整理")

if __name__ == '__main__':
    interface()