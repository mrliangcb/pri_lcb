


x=['123123','0213487。0192834','01298347。10293874。102387']
def extract_sen(x):
    sent=[]
    for i in range(len(x)):# 先遍历段
        j=0
        length=len(x[i])
        while j<len(x[i]):
            k=j
            while k<length and x[i][k]!='。':
                print('k为',k,'x[0]长度为:',len(x[i]))
                k+=1
            sent.append(x[i][j:k+1])
            j=k+1
    return sent

sent=extract_sen(x)
print(sent)

































