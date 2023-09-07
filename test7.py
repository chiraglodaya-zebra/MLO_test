import json
some_str = '{"T1":0,"T2":1}'
print(some_str.remove("T2"))
res = json.loads(some_str)
print(res)