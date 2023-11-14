import os
import time
import json
import sqlite3
from loguru import logger

import function.tools.config_io as config_io

def modify_time(path, timestamp):
    os.utime(path, (timestamp, timestamp))

def is_sorted(style):
    sorted = False
    conn = sqlite3.connect('everphoto.db')
    c = conn.cursor()
    if style == "personal":
        c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='personal_move_record'")
    elif style == "share":
        c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='shared_move_record'")
    if c.fetchone()[0] != 0:
        if style == "personal":
            c.execute('SELECT source, target FROM personal_move_record')
        elif style == "share":
            c.execute('SELECT source, target FROM shared_move_record')
        record = c.fetchall()
        if len(record) != 0:
            sorted = True
    conn.close()

    return sorted

def modify_picture_time(type):
    style = type
    if style == "personal":
        path = config_io.load("dl_path")
    elif style == "share":
        path = config_io.load("share_dl_path")

    sorted = is_sorted(style)

    conn = sqlite3.connect('everphoto.db')
    c = conn.cursor()
    if style == "personal":
        c.execute('SELECT json_data FROM personal_asset')
    elif style == "share":
        c.execute('SELECT json_data FROM shared_asset')
    data = c.fetchall()
    for asset in data:
        asset = json.loads(asset[0])
        if asset["deleted"] == True:
            continue
        generatedAt = asset["generatedAt"]
        generatedAt = generatedAt.replace('T', ' ')
        if '.' in generatedAt:
            generatedAt = generatedAt.split('.')[0]
        if '+' in generatedAt:
            generatedAt = generatedAt.split('+')[0]
        generatedAt = int(time.mktime(time.strptime(generatedAt, "%Y-%m-%d %H:%M:%S")))
        filename = f'{asset["id"]}.{asset["mime"].split("/")[1]}' if asset['mime'] != '' else f'{asset["id"]}.{asset["subType"]}'
        if sorted == True:
            if style == "personal":
                c.execute('SELECT source, target FROM personal_move_record WHERE source = ?', (filename,))
            elif style == "share":
                c.execute('SELECT source, target FROM shared_move_record WHERE source = ?', (filename,))
            record = c.fetchone()
            if record != None:
                filename = record[1]
        if os.path.exists(f'{path}/{filename}') == True:
            modify_time(f'{path}/{filename}', generatedAt)
            logger.info("[成功] 写入", filename, "时间为", asset["generatedAt"], "(", generatedAt, ")")
        else:
            logger.warning("[失败] 文件", filename, "不存在，无法写入时间")
    conn.close()


def interface(type):
    os.system('cls')
    print("时光相册下载器")
    if type == "personal":
        print("当前进度：5. 写入照片时间到文件信息")
        logger.info("当前进度：5. 写入照片时间到文件信息")
    elif type == "share":
        print("当前进度：13. 写入照片时间到文件信息")
        logger.info("当前进度：13. 写入照片时间到文件信息")
    print("")
    print("注意事项：")
    print("1. 本功能不是将信息写入EXIF，而是将拍摄时间信息写入文件修改时间")
    print("2. 本功能不会修改文件的原始数据本身，也就不会更改md5校验值")
    print("3. 本功能写入的是时光相册中的拍摄时间，不是上传时间")
    print("4. 请确认已经下载好元数据和照片后再使用此功能")
    print("5. 只显示出错信息，所有处理日志在everphotoDL.log中")
    print("")
    print("正在写入照片时间到文件信息，请稍后...")
    modify_picture_time(type)
    print("")
    print("写入完成！")

if __name__ == "__main__":
    interface()