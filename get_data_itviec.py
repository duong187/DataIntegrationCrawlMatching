import requests
import json

# itviec_url = 'http://localhost:8080/itviec'
# result = {"data":[]}
# for page_num in range(1,31,1):
#     params = {"page_num": page_num, "limit": 20}
#     r = requests.get(url=itviec_url, params = params)
#     data = json.dumps(r.json())
#     print(data)
#     with open("data_1905/itviec_data_hanoi.txt", "a") as file:
#         jobs = json.loads(str(data))["result"]
#         for job in jobs:
#             json.dump(job, file)
#             file.write('\n')
#     jobs = json.loads(str(data))["result"]
#     for job in jobs:
#         result["data"].append(job)

# with open("itviec_data_tphcm_2.json", "a") as file:
#     json.dump(result, file)

itviec_url = 'http://localhost:8081/itviec'
result = []
for page_num in range(1,33,1):
    params = {"page_num": page_num, "limit": 20}
    r = requests.get(url=itviec_url, params = params)
    data = json.dumps(r.json())
    print(data)
    with open("data_1905/itviec_data_hanoi.txt", "a") as file:
        jobs = json.loads(str(data))["result"]
        for job in jobs:
            result.append(job)
with open("./hanoi_itviec.json", "w") as f:
    json.dump(result, f)
         