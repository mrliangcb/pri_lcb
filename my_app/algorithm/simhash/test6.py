
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

x=''





