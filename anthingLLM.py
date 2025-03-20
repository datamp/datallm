import json

import requests

api_key = ""
slug = ""
url = f"http://ip:3001/api/v1/workspace/{slug}/chat"

header = {}
header['Authorization'] = f'Bearer {api_key}'
header['accept']= 'text/event-stream'
header["Content-Type"] = "application/json"
print(url)

question =  ""

data = {
  "message": question,
  "mode": "chat",
  "stream":True
}

with requests.request(url =url,method="post",headers=header,json=data,stream=True) as response:
    for line in response.iter_lines():  # iter_lines()默认解码为UTF-8字符串
            if line:  # 检查是否为空行，避免空行被打印出来
                print(line.decode('utf-8'))  # 解码二进制数据为字符串（如果需要
