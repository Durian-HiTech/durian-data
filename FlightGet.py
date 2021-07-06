import requests
import time

# 设置headers参数
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
# 爬取前五页的评论

# 第一次lasthotcommentid为空
lasthotcommentid = ''
# 请求与网站的连接
res = requests.post('https://www.umetrip.com/gateway/api/web/umeflightstatus-live/live/getchartstatistics', headers=headers)
# 解析JSON
data = res.json()

print(data)

for x in data['arrCivil']:
    print(x)

# for state in data:
#     print(state)
    # print(data[state])