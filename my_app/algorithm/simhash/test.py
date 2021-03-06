#!/usr/bin/python
# coding=utf-8
# https://github.com/1e0ng/simhash


class simhash:
    # 构造函数
    def __init__(self, tokens='', hashbits=128):

        self.hashbits = hashbits
        self.hash = self.simhash(tokens);
        # print('self.token_hash_list是什么？:',self.token_hash_list)

    # toString函数
    def __str__(self):
        return str(self.hash)

    # 生成simhash值
    def simhash(self, tokens):
        v = [0] * self.hashbits
        self.token_hash_list=[]
        for t in [self._string_hash(x) for x in tokens]:  # t为token的普通hash值
            self.token_hash_list.append(t)
            for i in range(self.hashbits):
                bitmask = 1 << i
                if t & bitmask:
                    v[i] += 1  # 查看当前bit位是否为1,是的话将该位+1
                else:
                    v[i] -= 1  # 否则的话,该位-1
        fingerprint = 0
        for i in range(self.hashbits):
            if v[i] >= 0:
                fingerprint += 1 << i
        return fingerprint  # 整个文档的fingerprint为最终各个位>=0的和


        # 求海明距离
    def hamming_distance(self, other):
        x = (self.hash ^ other.hash) & ((1 << self.hashbits) - 1)
        tot = 0;
        while x:
            tot += 1
            x &= x - 1
        return tot

    def dup_rate(self,other):
        other_set=set(other.token_hash_list)
        score=0
        for i,j in enumerate(self.token_hash_list):
            if j in other_set:
                score+=1
        # try:
        rate=score/len(self.token_hash_list)
        # except:
        #     rate=0
        return rate

    # 求相似度
    def similarity(self, other):
        a = float(self.hash)
        b = float(other.hash)
        if a > b:
            return b / a
        else:
            return a / b


    # 针对source生成hash值   (一个可变长度版本的Python的内置散列)
    def _string_hash(self, source):
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** self.hashbits - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
        x ^= len(source)
        if x == - 1:
            x = - 2
        return x

import jieba
if __name__ == '__main__':
    s = 'This is a test string for testing'
    s='巴西卫生部长帕祖洛当地时间20日与各州州长会晤后，宣布将购买北京科兴中维生物技术有限公司研发的新冠疫苗，并将其纳入国家免疫计划。'
    s=list(jieba.cut(s))
    print(s)
    hash1 = simhash(s)
    print('hash1完成')

    s = 'This is a test string for testing also'
    s='巴西卫生部长张三里斯当地时间20日与各州州长会晤后，宣布将购买北京科兴中维生物技术有限公司研发的新冠疫苗，并将其纳入国家免疫计划。'
    s=list(jieba.cut(s))
    print(s)
    hash2 = simhash(s)

    s = '张三里斯12394876'
    s=list(jieba.cut(s))
    print(s)
    hash3 = simhash(s)

    print(hash1.hamming_distance(hash2), "   ", hash1.similarity(hash2))

    print(hash1.hamming_distance(hash3), "   ", hash1.similarity(hash3))

    print(hash2.hamming_distance(hash2), "   ", hash2.similarity(hash2))
