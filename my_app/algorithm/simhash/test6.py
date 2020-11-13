
# 文本预处理去除垃圾符号
x=10
x*=10
print(x)

class preprocess():
    def doc2str(self,path):
        doc_list=self.get_docx(path)
        str_=self.doc_process(doc_list)
        return str_

    def get_docx(self,path):
        d = docx.opendocx(path)
        doc = docx.getdocumenttext(d)
        return doc
    def doc_process(self,doc_list):  # 将list装着的一句一句话变成一个长文本str
        x = [re.sub('\t([\d]*$)?', '', i) for i in doc_list]  # 去掉 \t \t386等格式
        # for i in range(len(x)):
        #     if '\t' in x[i]:
        # print('第一个#############', repr(x[i]))
        # print('第二个#############', repr(x_[i]))
        x = [i.replace(' ', '') for i in x]  # 去掉空行
        x = ''.join(x)
        return x
import re
import regex as re
x=r'12309786232\r39874\t\t6273846t:   \r  中国大\r  目    录\r  \x13 TOC \\o "1$3" \\h \\z \\u \x14\x13 HYPERLINK \\l "_Toc358121912" \x14一、投标书\x13 PAGEREF _Toc358121912 \\h \x141\r二、投标一览三、投标价格四、货物说明一览  \x13 HYPERLINK \\l "_Toc358121$16" \x14五、日程安排表\x13 PAGEREF _Toc3581'
# r就是不转义，保留这个样子
x = [re.sub(r"((\\+[a-zA-Z0-9]+)+([\d]*$)?)?(_Toc[0-9]+)*",'',x)]
print(repr(x))
print(x)
# print(repr(''.join(x)))

y='\\h' #算是\h
print(y)
y=r'\\h' # 就是本来的\\h
print(y)
z='''九、由（银行名称）出具的投标保证十、法人代表授权   HYPERLINK \l "_Toc358121922" 十一、资格证明文件 PAGEREF _Toc358121922 \h 12'''
zz=[re.sub(r"(|)",'',z)]
print('处理z:',zz)

yy=[re.sub(r"\\\\[a-z]+",'',y)]  # \\\\ 第一个\是告诉第二个\是非匹配
print(yy)
