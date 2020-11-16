




def gehang(s):
    s=repr(s)
    # print('传入的s',s)
    s_new = s
    y = []
    for i in range(1, len(s)):
        if (s[i - 1] == '\\') and s[i] == 'n':
            y.append(i - 1)

    for i in range(len(y) - 1, 0, -1):
        if (y[i] - y[i - 1]) == 3:
            s_new = s_new[0:y[i]] + s_new[y[i] + 2:]
    return s_new



if __name__=="__main__":
    s='这个是什么呢大\n唐\n中\n水\n集\n团'

    print(s)
    y=[]
    print(gehang(s))


# import re
# import regex as re
# x=r'12309786232\r39874\t\t6273846t:   \r  中国大\r  目    录\r  \x13 TOC \\o "1$3" \\h \\z \\u \x14\x13 HYPERLINK \\l "_Toc358121912" \x14一、投标书\x13 PAGEREF _Toc358121912 \\h \x141\r二、投标一览三、投标价格四、货物说明一览  \x13 HYPERLINK \\l "_Toc358121$16" \x14五、日程安排表\x13 PAGEREF _Toc3581'
# # r就是不转义，保留这个样子
# print('原文:\n',x)
# x = [re.sub(r"((\\+[a-zA-Z0-9]+)+([\d]*$)?)?(_Toc[0-9]+)*",'',x)]
# # print('原文:',repr(x))
# print('处理后:\n',x)
# # print(repr(''.join(x)))
#
# y='\\h' #算是\h
# print(y)
# y=r'\\h' # 就是本来的\\h
# print(y)
# z='''九、由（银行名称）出具的投标保证十、法人代表授权   HYPERLINK \l "_Toc358121922" 十一、资格证明文件 PAGEREF _Toc358121922 \h 12'''
# zz=[re.sub(r"(|)",'',z)]
# print('处理z:',zz)
#
# yy=[re.sub(r"\\\\[a-z]+",'',y)]  # \\\\ 第一个\是告诉第二个\是非匹配
# print(yy)



















