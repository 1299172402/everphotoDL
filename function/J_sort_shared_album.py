import os
import json
import sqlite3
import datetime

import function.tools.config_io as config_io

SHARE_DL_PATH = config_io.load("share_dl_path")

def timestamp_format(ts, format='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.fromtimestamp(ts).strftime(format)

def get_member_name(space_id, user_id):
    conn = sqlite3.connect('everphoto.db')
    c = conn.cursor()
    c.execute("SELECT json_data FROM shared_member where space_id = ?", (space_id, ))
    data = c.fetchall()
    conn.close()
    for item in data:
        item = json.loads(item[0])
        if item['user_id'] == user_id:
            if 'deleted' in item and item['deleted'] == True:
                return f"{user_id} (用户已删除账号)"
            else:
                 return item['nickname']
    return ""

def sort_shared_album(info):
    space_id = info['id']
    name = info['name']
    if os.path.exists(f"{SHARE_DL_PATH}/{name}") == False:
        os.mkdir(f"{SHARE_DL_PATH}/{name}")
    
    data = f'''
    相册ID：{info['id']}
    相册名称：{info['name']}
    成员数量：{info['member_num']}
    照片和视频数量：{info['asset_num']}
    创建时间：{timestamp_format(info['created_at'])} ({info['created_at']})
    更新时间：{timestamp_format(info['op_time'])} ({info['op_time']})
    相册大小：{info['usage']}
    '''

    with open(f"{SHARE_DL_PATH}/{name}/{name}.txt", 'w', encoding='utf-8') as f:
        f.write(data)
    
    conn = sqlite3.connect('everphoto.db')
    c = conn.cursor()
    c.execute("SELECT json_data FROM shared_activity where space_id = ?", (space_id,))
    data = c.fetchall()
    for item in data:
        item = json.loads(item[0])

        asset_data = ""
        for asset in item['asset_list']:
            asset_data += str(asset) + '\n        '

        comment_data = ""
        for comment in item['comment_list']:
            comment_data += f'''
            评论ID：{comment['id']}
            评论内容：{comment['content']}
            评论者：{get_member_name(space_id, comment['creator_id'])} ({comment['creator_id']})
            '''
            if 'reply_to' in comment:
                comment_data += f'''
                回复给：{get_member_name(space_id, comment['reply_to'])} ({comment['reply_to']})

                '''
        
        like_data = ""
        for like in item['like_list']:
            like_data += f"{get_member_name(space_id, like)} ({like})\n        "

        data = f"""
        动态ID：{item['id']}
        内容：{item['caption'] if 'caption' in item else ''}
        发布者：{get_member_name(space_id, item['creator_id'])} ({item['creator_id']})
        创建时间：{timestamp_format(item['created_at'])} ({item['created_at']})
        是否删除：{item['is_deleted']}

        照片：
        {asset_data}

        评论：
        {comment_data}
        
        点赞：
        {like_data}
            """

        if os.path.exists(f"{SHARE_DL_PATH}/{name}/{timestamp_format(item['created_at'], '%Y-%m-%d-%H-%M-%S')}") == False:
            os.mkdir(f"{SHARE_DL_PATH}/{name}/{timestamp_format(item['created_at'], '%Y-%m-%d-%H-%M-%S')}")
        with open(f"{SHARE_DL_PATH}/{name}/{timestamp_format(item['created_at'], '%Y-%m-%d-%H-%M-%S')}/动态信息.txt", 'w', encoding='utf-8') as f:
            f.write(data)

        conn = sqlite3.connect('everphoto.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS shared_move_record (source TEXT, target TEXT)''')
        conn.commit()

        c.execute("SELECT json_data FROM shared_asset where space_id = ?", (space_id, ))
        shared_asset_list = c.fetchall()

        for asset_id in item['asset_list']:
            for shared_asset in shared_asset_list:
                shared_asset = json.loads(shared_asset[0])
                if shared_asset['id'] == asset_id:
                    filename = f'{shared_asset["id"]}.{shared_asset["mime"].split("/")[1]}'
                    if os.path.exists(f"{SHARE_DL_PATH}/{filename}") == False:
                        print(f"文件 {filename} 不存在，可能之前已移动到其他动态的文件夹中。当前目标文件夹 {name}/{timestamp_format(item['created_at'], '%Y-%m-%d-%H-%M-%S')}")
                        break
                    os.rename(f"{SHARE_DL_PATH}/{filename}", f"{SHARE_DL_PATH}/{name}/{timestamp_format(item['created_at'], '%Y-%m-%d-%H-%M-%S')}/{filename}")
                    c.execute("INSERT INTO shared_move_record VALUES (?, ?)", (f"{filename}", f"{name}/{timestamp_format(item['created_at'], '%Y-%m-%d-%H-%M-%S')}/{filename}"))
                    break
        
        conn.commit()
        conn.close()

def pick_album():
    conn = sqlite3.connect('everphoto.db')
    c = conn.cursor()
    c.execute("SELECT json_data FROM personal_space")
    data = c.fetchall()
    conn.close()
    for item in data:
        item = json.loads(item[0])
        if 'deleted' not in item or item['deleted'] == False :
            id = item['id']
            name = item['name']
            print(f"正在整理共享相册：{id} {name}")
            sort_shared_album(item)

def interface():
    os.system('cls')
    print("时光相册下载器")
    print("当前进度：11. 整理共享相册的信息、图片、视频、动态、评论、点赞")
    print("")
    print("注意事项：")
    print("1. 请自行确认第10步批量下载共享相册的图片是否完成")
    print("2. 如果第10步未完成，可能会导致处理后缺少图片")
    print("3. 因为已删除的用户、动态等情况，会有部分照片没有整理")
    print("")
    print("是否开始整理：")
    print("1. 是")
    print("2. 否")
    choice = input("请输入数字：")
    if choice == "1":
        pick_album()
        print("整理完成")
    else:
        print("已取消整理")
    input("按回车键继续...")

if __name__ == '__main__':
    interface()