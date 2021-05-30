import json
s = {"address": "S\u1ed1 82 ng\u00f5 203 Ho\u00e0ng Qu\u1ed1c Vi\u1ec7t, C\u1ea7u Gi\u1ea5y, H\u00e0 N\u1ed9i", "benefits": "Healthcare Plan", "company": "Chi Nh\u00e1nh Ph\u00e2n Ph\u1ed1i Mi\u1ec1n B\u1eafc \u2013 C\u00f4ng Ty TNHH \u0110\u1ea7u T\u01b0 & Th\u01b0\u01a1ng M\u1ea1i Thi\u00ean H\u1ea3i", "elem_id": 1377318, "title": "Nh\u00e2n Vi\u00ean H\u00e0nh Ch\u00ednh \u2013 Nh\u00e2n S\u1ef1", "url": "/nhan-vien-hanh-chinh-nhan-su-740-1377318-jv"}
json_obj = json.dumps(s, indent=4)
dict = json.loads(json_obj)

def dict_utf8_convert(dict):
    for key in dict.keys():
        dict[key] = str(dict[key]).encode('utf-8').decode('utf-8')
    return dict

print(json_obj)
print(dict_utf8_convert(dict))