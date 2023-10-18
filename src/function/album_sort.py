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

    # 获取相册列表，包括相册id和名称
    album_list = []
    c.execute('''
        SELECT DISTINCT json_data
        FROM personal_tag
    ''')
    data = c.fetchall()
    for tag in data:
        tag = json.loads(tag[0])
        # type = 100 为自建相册
        if tag['type'] != 100:
            continue
        if 'deleted' in tag and tag['deleted'] == True:
            continue
        album_list.append({'id': tag['id'], 'name': tag['name']})


    # 移动照片
    c.execute("SELECT json_data FROM personal_asset")
    data = c.fetchall()
    for asset in data:
        asset = json.loads(asset[0])
        if asset['deleted'] == True:
            continue
        
        matching_album = [item for item in album_list if item['id'] in asset['tags']]
        if matching_album == []:
            continue
        else:
            matching_album = matching_album[0]
        
        # 文件当前路径
        source_filename = f"{asset['id']}.{asset['mime'].split('/')[1]}" if asset['mime'] != '' else f"{asset['id']}.{asset['subType']}"

        # 文件目标路径
        target_folder = matching_album['name'].replace('|', '_').replace('?', '_').replace('*', '_').replace('<', '_').replace('>', '_').replace(':', '_').replace('"', '_').replace('/', '_').replace('\\', '_')
        target_filename = source_filename


        if os.path.exists(f"{dl_path}/{target_folder}") == False:
            os.mkdir(f"{dl_path}/{target_folder}")
        
        if os.path.exists(f"{dl_path}/{source_filename}") == True:
            if os.path.exists(f"{dl_path}/{target_folder}/{target_filename}") == False:
                c.execute("INSERT INTO personal_move_record VALUES (?, ?)", (f"{source_filename}", f"{target_folder}/{target_filename}"))
                os.rename(f"{dl_path}/{source_filename}", f"{dl_path}/{target_folder}/{target_filename}")
                print(f"[成功] {source_filename} 文件已整理到 {target_folder}/{target_filename}")
            else:
                print(f"[跳过] {source_filename} 当前路径已有同名文件 {target_folder}/{target_filename}")
    
    
    conn.commit()
    conn.close()

def interface():
    os.system('cls')
    print("时光相册下载器")
    print("当前进度：6.5 按相册整理")
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
    input("按回车键继续...")

if __name__ == '__main__':
    interface()