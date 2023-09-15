import requests
import time

class ServiceError(Exception):
    pass

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
            time.sleep(10)
    return None

def Download_Media(token, id, path):
    url = f'https://media.everphoto.cn/origin/{id}'
    headers = {
        "authorization": f"Bearer {token}", 
    }
    res = requests.get(url, headers=headers)
    with open(path, 'wb') as f:
        f.write(res.content)

if __name__ == '__main__':
    res = GetUpdates(token = "", cursor = "", space_id = 0)
    print(res)