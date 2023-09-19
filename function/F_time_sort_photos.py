import os
import json
import sqlite3

import function.tools.config_io as config_io

def organize_picture_upload(sort, time):
    dl_path = config_io.load('dl_path')
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

        current_filename = f"{asset['id']}.{asset['mime'].split('/')[1]}" if asset['mime'] != '' else f"{asset['id']}.{asset['subType']}"
        source_path = asset['source_path']

        _, source_filename = os.path.split(source_path)
        if source_filename == "":
            source_filename = current_filename
        elif source_path.startswith('ios://'):
            source_filename = current_filename
        else:
            source_filename = source_filename.replace('|', '_').replace('?', '_').replace('*', '_').replace('<', '_').replace('>', '_').replace(':', '_').replace('"', '_').replace('/', '_').replace('\\', '_')
        
        date_string = asset[sort].split('T')[0]
        if time == "year":
            source_folder = date_string.split('-')[0]
        elif time == "month":
            source_folder = date_string.split('-')[0] + '-' + date_string.split('-')[1]
        elif time == "day":
            source_folder = date_string.split('-')[0] + '-' + date_string.split('-')[1] + '-' + date_string.split('-')[2]
            
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
    print("当前进度：6. 按时间整理")
    print("")
    print("注意事项：")
    print("1. 将恢复文件的原始名称，IOS端上传的照片除外")
    print("2. 将照片整理到对应时间的文件夹中")
    print("3. 如果照片的保存的路径中有同名文件，将会跳过")
    print("4. 此功能是整理照片到文件夹，不是将时间信息写入文件。如果需要写入时间信息，请使用第13步")
    print("")
    print("按上传时间整理还是按拍摄时间整理：")
    print("1. 按上传时间整理")
    print("2. 按拍摄时间整理")
    choice = input("请输入数字：")
    if choice == "1":
        sort = "uploadedAt"
    elif choice == "2":
        sort = "generatedAt"
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