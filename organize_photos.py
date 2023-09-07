import os
import json
import sqlite3

def organize_picture():
    dl_path = json.load(open('config.json', 'r', encoding='utf-8'))['dl_path']
    conn = sqlite3.connect('move_record.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS move_record (source text, target text)''')

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
                        c.execute("INSERT INTO move_record VALUES (?, ?)", (f"{current_filename}", f"{source_folder}/{source_filename}"))
                        conn.commit()
                        os.rename(f"{dl_path}/{current_filename}", f"{dl_path}/{source_folder}/{source_filename}")
                        print(f"[成功] {current_filename} 文件已整理到 {source_folder}/{source_filename}")
                    else:
                        print(f"[跳过] {current_filename} 当前路径已有同名文件 {source_folder}/{source_filename}")
    conn.close()

def interface():
    os.system('cls')
    print("时光相册下载器")
    print("当前进度：5. 智能整理照片（推荐）")
    print("")
    print("注意事项：")
    print("1. 将恢复文件的原始名称")
    print("2. 根据照片的原始路径，将照片整理到对应的文件夹中")
    print("3. 如果照片的上传路径中有同名文件，则会跳过")
    print("4. 从IOS端上传的照片无法获取原始路径，也将跳过")
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
    input("按回车键继续...")

if __name__ == '__main__':
    interface()