import json
some_str = '{"T1":0,"T2":1}'
res = json.loads(some_str)
print(res)