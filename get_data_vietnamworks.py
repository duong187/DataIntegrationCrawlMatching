import requests
import json
import codecs

# itviec_url = 'http://localhost:8080/vietnamwork'

# for page_num in range(1,89,1):
#     params = {"page_num": page_num, "limit": 50}
#     r = requests.get(url=itviec_url, params = params)
#     data = json.dumps(r.json())
#     print(data)

#     with open("data_1905/vietnamwork_data_hanoi.txt", "a") as file:
#         jobs = json.loads(str(data))["result"]
#         for job in jobs:
#             json.dump(job, file)
#             file.write('\n')

itviec_url = 'http://localhost:8081/vietnamwork'
result = []
for page_num in range(1,80,1):
    params = {"page_num": page_num, "limit": 50}
    r = requests.get(url=itviec_url, params = params)
    data = json.dumps(r.json())
    print(data)

    with open("data_1905/vietnamwork_data_hanoi.txt", "a") as file:
        jobs = json.loads(str(data))["result"]
        for job in jobs:
            result.append(job)
with open("hanoi_vietnamwork.json", "w") as f:
    json.dump(result, f)