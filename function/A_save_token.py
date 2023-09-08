import os
import requests
import function.tools.config_io as config_io

def check_token(token):
    url = 'https://web.everphoto.cn/api/users/self/profile'
    headers = {
        'authorization': f'Bearer {token}',
    }
    try:
        res = requests.get(url, headers=headers).json()
        if res['code'] == 0:
            config_io.save("token", token)
            print(f'[用户名] {res["data"]["name"]}')
            print(f'[手机号] {res["data"]["mobile"]}')
            print(f'[性别] {res["data"]["estimate_gender"]}')
            print(f'')
            print(f'[账户创建时间] {res["data"]["created_at"]}')
            print(f'[账户创建天数] {res["data"]["days_from_created"]} 天')
            print(f'')
            print(f'[照片和视频总数量] {res["data"]["estimated_media_num"]}')
            print(f'[已使用容量] {res["data"]["usage"]}')
            print(f'[总容量大小] {res["data"]["quota"]}')
            print(f'')
            print(f'[文件最大上传大小] {res["data"]["max_file_size"]}')
            print(f'[回收站保留天数] {res["data"]["trash_show_days"]}')
            print(f'')
            print(f'[成功] token有效，已保存到everphoto.db')
        else:
            print(f'[失败] token无效，未保存，请检查token是否正确')
        input('按下回车键继续...')
    except:
        print("[失败] 请求profile失败，请重试")

def interface():
    os.system('cls')
    print("时光相册下载器")
    print("当前进度：1. 登录时光相册")
    print("")
    print("具体操作：")
    print("1. 打开 https://www.everphoto.cn/，登录时光相册")
    print("2. 登录完成后，按下F12，打开开发者工具，再打开上方的“控制台/Console”页面")
    print("3. 输入“document.cookie”并回车，将显示“access_token=XXX”")
    print("4. 其中XXX就是你的token，复制到下方")
    print("")
    token = input("请输入token：")
    check_token(token)

if __name__ == '__main__':
    interface()