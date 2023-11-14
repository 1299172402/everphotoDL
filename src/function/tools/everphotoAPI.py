import requests
import time

class ServiceError(Exception):
    pass

def get_profile(token):
    url = 'https://web.everphoto.cn/api/users/self/profile'
    headers = {
        'authorization': f'Bearer {token}',
    }
    try:
        res = requests.get(url, headers=headers).json()
        return res
    except:
        return {'code': -1}

def GetUpdates(token = "", cursor = "", space_id = 0):
    url = "https://openapi.everphoto.cn/sf/3/v4/GetUpdates"
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {token}",
    }

    retries = 0
    while retries < 10:
        try:
            res = requests.post(url, headers=headers, json={"cursor":cursor,"space_id":space_id}, timeout=5).json()
            if res["code"] == 0:
                return res
            else:
                raise ServiceError(res)
        except requests.Timeout:
            retries += 1
            time.sleep(5)
        except ServiceError as e:
            retries += 1
            time.sleep(5)
    return {'code': -2}

def Download_Media(token, id, path):
    url = f'https://media.everphoto.cn/origin/{id}'
    headers = {
        "authorization": f"Bearer {token}", 
    }
    try:
        res = requests.get(url, headers=headers)
        with open(path, 'wb') as f:
            f.write(res.content)
        return True
    except:
        return False

if __name__ == '__main__':
    res = GetUpdates(token = "", cursor = "", space_id = 0)
    print(res)
