

import json
x=[1,2,3,4,5,6]
y=json.dumps(x)
print(y)
print(type(y))
print(type(json.loads(y)))

xx='[1,2,3,4,5,6]'
print(json.loads(xx))
print(type(json.loads(xx)))













