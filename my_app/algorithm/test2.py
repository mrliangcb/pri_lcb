


x='99999999999999999999999'
print(len(x))

y=['']
if y:
    print('ok y')

z=[[]]
if z:
    print('ok z')

k=''
if k:
    print('k ok')

def calculate_hashing_set(n_gram, Base=17, n=5):
    hashinglist = []
    hash = 0
    first_gram = n_gram[0]
    # 单独计算第一个n_gram的哈希值
    for i in range(n):  # 0到5
        hash += ord(first_gram[i]) * (Base ** (n - i - 1))# 这个才是最标准的hash计算，后面那些都是加进来
    hashinglist.append(hash)
    Base_n_1 = (Base ** (n - 1))  #不要每次for循环都计算一次次方，降低复杂度
    for i in range(1, len(n_gram)):  # 主要这里耗时  #前一个和后一个只差一个字符
        pre_gram = n_gram[i - 1]
        this_gram = n_gram[i]
        hash = (hash - ord(pre_gram[0]) * Base_n_1) * Base + ord(this_gram[n - 1])   #这里重复计算了gram_0
        hashinglist.append(hash)
    return hashinglist

x=['集体优秀奖']
result=calculate_hashing_set(x)
print(result)

x=[1,2,3,4,5,6,7,8,9,10]
print(x[1:4]+x[6:10])
