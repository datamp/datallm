import json

import requests

api_key = "8K9FEWC-8Y0MYJW-KJC25ZD-WBVE1Z4"
slug = "e0c1935b-3b7b-4c00-9ef7-711bff235393"
url = f"http://localhost:3001/api/v1/workspace/{slug}/chat"

header = {}
header['Authorization'] = f'Bearer {api_key}'
header['accept']= 'text/event-stream'
header["Content-Type"] = "application/json"
print(url)

question =  "政务网DSC?"

data = {
  "message": question,
  "mode": "chat",
  "stream":True
}

with requests.request(url =url,method="post",headers=header,json=data,stream=True) as response:
    for line in response.iter_lines():  # iter_lines()默认解码为UTF-8字符串
            if line:  # 检查是否为空行，避免空行被打印出来
                print(line.decode('utf-8'))  # 解码二进制数据为字符串（如果需要