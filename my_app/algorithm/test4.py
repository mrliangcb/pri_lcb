


x1=0
x2=0
print(x1==x2==1)

result_01=[[1,1,1,1,1,1,1,1,1,1,1]]
doc1_str=[['s','.','.','.','.','.','.','e','f','.','.']]
doc1_str=[[]]
result_01=[[]]
i=0

length_duan=len(result_01[0])
if len(result_01[i]) > 1:
    while i < length_duan:
        j = i
        while j < length_duan and doc1_str[0][i] == doc1_str[0][j] == '.':
            j += 1
        # 检查是不是收集足够的..
        print('i和j',i,j)
        if j - i > 1:
            # 识别为目录...
            for m in range(i, j):
                result_01[0][m] = 0
                doc1_str[0][m] = ''
                # doc1_posi[0][m] = ''

        i = j+1
print(result_01)
print(doc1_str)


