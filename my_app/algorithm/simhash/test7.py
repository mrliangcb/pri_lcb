



# a=set()
# a.add(1)
# a.add(2)
# b=set()
# print(len(b))
# print(a|b)

x='123456789'
y='123456789'
# y='123abcdefgsfd'

def pari_check(x,y):
    i=0
    while i<len(x) and x[i]==y[i]:
        i+=1
    if i==len(x) and i==len(y):
        return True
    return False

res=pari_check(x,y)
print(res)

print(len(8))







