import json



x=json.dumps([['123'],{1:1}])
print(type(x))
print(json.loads(x))