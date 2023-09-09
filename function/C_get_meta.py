import os
import json
import sqlite3
import function.tools.everphotoAPI as everphotoAPI
import function.tools.config_io as config_io

def create_table():
    conn = sqlite3.connect('everphoto.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS personal_asset  (id INTEGER PRIMARY KEY, cursor TEXT, space_id INTEGER, json_data TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS personal_space  (id INTEGER PRIMARY KEY, cursor TEXT, space_id INTEGER, json_data TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS personal_tag    (id INTEGER PRIMARY KEY, cursor TEXT, space_id INTEGER, json_data TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS personal_people (id INTEGER PRIMARY KEY, cursor TEXT, space_id INTEGER, json_data TEXT)''')
    conn.commit()
    conn.close()

def load_latest_cursor():
    conn = sqlite3.connect('everphoto.db')
    c = conn.cursor()
    c.execute("SELECT cursor FROM personal_asset ORDER BY id DESC LIMIT 1")
    cursor = c.fetchall()
    conn.close()
    if cursor == []:
        return ""
    else:
        return cursor[0][0]

def get_original_message():
    conn = sqlite3.connect('everphoto.db')
    c = conn.cursor()

    token = config_io.load("token")
    cursor = load_latest_cursor()
    space_id = 0
    data_type = "user_data"

    if cursor:
        res = everphotoAPI.GetUpdates(token, cursor, space_id)
        cursor = res['pagination']['next']
        print("检测到已下载部分原始数据，将继续下载...")

    while True:
        res = everphotoAPI.GetUpdates(token, cursor, space_id)
        if res['pagination']['has_more'] == False:
            print("\n[成功] 相册元数据获取完成")
            break
        if res == None:
            break
        elif res['code'] != 0:
            res = everphotoAPI.GetUpdates(token, cursor, space_id)
        else:
            datas = ['asset', 'tag', 'space', 'people']
            for item in datas:
                for data in res['data'][data_type][item + '_list']:
                    c.execute("INSERT INTO personal_" + item + " VALUES (?, ?, ?, ?)", (None, cursor, space_id, json.dumps(data), ))
            conn.commit()
            cursor = res['pagination']['next']
            print(f"\r正在获取 {cursor} 页", end = '')
    
    conn.close()

def calc_picture_num():
    conn = sqlite3.connect('everphoto.db')
    c = conn.cursor()
    c.execute("SELECT json_data FROM personal_asset")
    data = c.fetchall()
    picture_num = 0
    video_num = 0
    for item in data:
        item = json.loads(item[0])
        if item['mime'].startswith('image') and item['deleted'] == False:
            picture_num += 1
        elif item['mime'].startswith('video') and item['deleted'] == False:
            video_num += 1
    print(f"图片数量：{picture_num}")
    print(f"视频数量：{video_num}")
    conn.close()

def interface():
    os.system('cls')
    print("时光相册下载器")
    print("当前进度：3. 下载相册的元数据")
    print("")
    print("注意事项：")
    print("1. 如果遇到 [失败] ，请重复下载原始数据，直到成功为止")
    print("2. [超时] 的情况系统会自动重试，无需手动操作")
    print("3. 如果图片和视频的数量小于时光相册APP上显示的数量，请删除everphoto.db后重试")
    print("4. 如果图片和视频的数量大于时光相册APP上显示的数量，表示曾重复上传某一图片，没有关系")
    print("")
    print("正在加载token...")
    if config_io.load("token") == "":
        print("token为空")
        print("第1步未完成，请先完成第1步登录时光相册")
        input('按下回车键继续...')
        return
    print("")
    print("正在创建数据库...")
    create_table()
    print("正在获取原始数据...")
    get_original_message()
    print("")
    print("正在根据当前原始数据计算图片数量...")
    calc_picture_num()
    print("")
    input('按下回车键继续...')

if __name__ == '__main__':
    interface()