import os
import json
import sqlite3
import function.tools.everphotoAPI as everphotoAPI
import function.tools.config_io as config_io

def create_table():
    conn = sqlite3.connect('everphoto.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS shared_space    (id INTEGER PRIMARY KEY, cursor TEXT, space_id INTEGER, json_data TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS shared_member   (id INTEGER PRIMARY KEY, cursor TEXT, space_id INTEGER, json_data TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS shared_asset    (id INTEGER PRIMARY KEY, cursor TEXT, space_id INTEGER, json_data TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS shared_activity (id INTEGER PRIMARY KEY, cursor TEXT, space_id INTEGER, json_data TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS shared_tag      (id INTEGER PRIMARY KEY, cursor TEXT, space_id INTEGER, json_data TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS shared_people   (id INTEGER PRIMARY KEY, cursor TEXT, space_id INTEGER, json_data TEXT)''')
    conn.commit()
    conn.close()

def load_latest_cursor(space_id):
    conn = sqlite3.connect('everphoto.db')
    c = conn.cursor()
    c.execute("SELECT cursor FROM shared_space WHERE space_id = ? ORDER BY id DESC LIMIT 1", (space_id, ))
    cursor = c.fetchall()
    conn.close()
    if cursor == []:
        return ""
    else:
        return cursor[0][0]

def get_original_message(space_id):
    conn = sqlite3.connect('everphoto.db')
    c = conn.cursor()

    token = config_io.load("token")
    cursor = load_latest_cursor(space_id)
    space_id = space_id
    data_type = "space_data"
    
    if cursor:
        res = everphotoAPI.GetUpdates(token, cursor, space_id)
        cursor = res['pagination']['next']
        print("检测到已下载部分原始数据，将继续下载...")
    
    while True:
        res = everphotoAPI.GetUpdates(token, cursor, space_id)
        if res['pagination']['has_more'] == False:
            print("\n[成功] 本共享相册的元数据获取完成")
            break
        if res == None:
            break
        elif res['code'] != 0:
            res = everphotoAPI.GetUpdates(token, cursor, space_id)
        else:
            c.execute("INSERT INTO shared_space VALUES (?, ?, ?, ?)", (None, cursor, space_id, json.dumps(res['data'][data_type]['space']), ))
            datas = ['member', 'asset', 'activity', 'tag', 'people']
            for item in datas:
                for data in res['data'][data_type][item + '_list']:
                    c.execute("INSERT INTO shared_" + item + " VALUES (?, ?, ?, ?)", (None, cursor, space_id, json.dumps(data), ))
            conn.commit()
            cursor = res['pagination']['next']
            print(f"\r正在获取 {cursor} 页", end = '')
    conn.close()

def calc_picture_num(space_id):
    conn = sqlite3.connect('everphoto.db')
    c = conn.cursor()

    activity_num = 0
    picture_num = 0
    video_num = 0
    member_num = 0

    c.execute("SELECT json_data FROM shared_activity WHERE space_id = ?", (space_id, ))
    data = c.fetchall()
    for item in data:
        item = json.loads(item[0])
        if item['is_deleted'] == False:
            activity_num += 1
    print(f"动态数量：{activity_num}")

    c.execute("SELECT json_data FROM shared_asset WHERE space_id = ?", (space_id, ))
    data = c.fetchall()
    for item in data:
        item = json.loads(item[0])
        if item['mime'].startswith('image') and item['deleted'] == False:
            picture_num += 1
        elif item['mime'].startswith('video') and item['deleted'] == False:
            video_num += 1
        elif item['mime'] == '' and item['subType'] == 'video' and item['deleted'] == False:
            video_num += 1
    print(f"图片数量：{picture_num}")
    print(f"视频数量：{video_num}")

    c.execute("SELECT json_data FROM shared_member WHERE space_id = ?", (space_id, ))
    data = c.fetchall()
    for item in data:
        item = json.loads(item[0])
        if  ('deleted' not in item) or (item['deleted'] == False):
            member_num += 1
    print(f"成员数量：{member_num}")

    conn.close()

def interface():
    os.system('cls')
    print("时光相册下载器")
    print("当前进度：11. 下载共享相册的元数据")
    print("")
    print("注意事项：")
    print("1. 如果遇到 [失败] ，请重复下载原始数据，直到成功为止")
    print("2. [超时] 的情况系统会自动重试，无需手动操作")
    print("3. 请自行检查各数量与手机APP显示的是否一致")
    print("4. 请先执行第3步下载相册的元数据，再执行本步骤")
    print("")
    print("是否开始下载：")
    print("1. 是")
    print("2. 否")
    choice = input("请输入数字：")
    if choice == "1":
        pass
    else:
        print("已取消下载")
        return
    print("")
    print("正在加载token...")
    if config_io.load("token") == "":
        print("token为空")
        print("第1步未完成，请先完成第1步登录时光相册")
        return
    print("")
    print("正在创建数据表...")
    create_table()
    print("正在获取原始数据...")
    conn = sqlite3.connect('everphoto.db')
    c = conn.cursor()
    c.execute("SELECT json_data FROM personal_space")
    data = c.fetchall()
    conn.close()
    for space in data:
        space = json.loads(space[0])
        if 'deleted' in space and space['deleted'] == True:
            continue
        print(f"相册名称：{space['name']}")
        print(f"相册ID：{space['id']}")
        print("")
        get_original_message(space_id=space['id'])
        print("正在根据当前原始数据计算图片数量...")
        calc_picture_num(space_id=space['id'])
        print("")

if __name__ == '__main__':
    interface()