import json
some_str = "{'T1':0,'T2':1}"
# print(some_str.remove("T2"))
print(some_str)
some_str = some_str.replace("'",'"')
res = json.loads(some_str)
print(res)