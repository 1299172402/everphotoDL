import os
import json
import sqlite3
import function.tools.config_io as config_io

def move_picture(dl_path, source, target):
    if os.path.exists(f"{dl_path}/{target}") == True:
        if os.path.exists(f"{dl_path}/{source}") == False:
            os.rename(f"{dl_path}/{target}", f"{dl_path}/{source}")
            print(f"[成功] {source} 已被恢复，来源 {target}")
        else:
            print(f"[失败] {source} 无法恢复，来源 {target}，目录已有同名文件")

def revert_photo_path():
    dl_path = config_io.load('dl_path')
    conn = sqlite3.connect('everphoto.db')
    c = conn.cursor()
    c.execute('SELECT source, target FROM move_record')
    record = c.fetchall()
    conn.close()
    for source, target in record:
        move_picture(dl_path, source, target)
    
    conn = sqlite3.connect('everphoto.db')
    c = conn.cursor()
    c.execute('DELETE FROM move_record')
    conn.commit()
    conn.close()

    for item in os.listdir(dl_path):
        if os.path.isdir(f"{dl_path}/{item}") == True:
            try:
                os.rmdir(f"{dl_path}/{item}")
            except:
                print(f"[跳过] {item} 目录非空，跳过删除")
                pass

def interface():
    os.system('cls')
    print("时光相册下载器")
    print("当前进度：7. 恢复照片路径到整理前")
    print("")
    print("注意事项：")
    print("1. 整理后已移动或重命名的文件无法恢复到之前的路径，将跳过")
    print("")
    print("正在检测是否整理过...")
    conn = sqlite3.connect('everphoto.db')
    c = conn.cursor()
    c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='move_record'")
    if c.fetchone()[0] == 0:
        conn.close()
        print("未检测到整理记录，无需恢复")
        input("按回车键继续...")
        return
    else:
        c.execute('SELECT source, target FROM move_record')
        record = c.fetchall()
        conn.close()
        if len(record) == 0:
            print("未检测到整理记录，无需恢复")
            input("按回车键继续...")
            return
    print("是否恢复到整理之前：")
    print("1. 是")
    print("2. 否")
    choice = input("请输入数字：")
    if choice == "1":
        revert_photo_path()
        print("恢复整理完成")
    else:
        print("已取消恢复整理")
    input("按回车键继续...")

if __name__ == '__main__':
    interface()