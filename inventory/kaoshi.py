#!/usr/bin/python
#coding:utf-8
import re
import os
import time
#打开题库
with open('bb.txt','r',encoding='utf8') as f:
    st = f.read()
#打开或创建记录错题的文件
t = open('1.txt','a+')
a = 0
os.system('CLS')
for i in range(1,3):
    try:
        #匹配题目
        s = re.search('(' + str(i) + '\..*?)' + str(i + 1) + '\.', st, re.S)
        #去掉题库中括号中的答案
        kong = re.sub('\(([A-F]*)\)', '（ ）', s.group(1))
        #去掉题库中下划线中的答案
        kong = re.sub('_+([A-F]*)_', '___', kong)
        #输出题目
        print(kong)
        #输入正确答案
        n = input("请输入答案：")
        #匹配选项
        key = re.search('\(([A-F]*)\)',s.group(1))
        if key.group(1) == None :
            print('答案是：',key.group(2))
            if n == key.group(2) or n.upper==key.group(2) or n.lower()==key.group(2):
            #每做对一个题目加一分
                a += 1
            else:
            #如果题目错误将他的题号写入1.txt
                t.write(str(i)+'\n')
        else:
            if n == key.group(1):
                a += 1
            else:
                t.write(str(i)+'\n')
            print('答案是：',key.group(1))
        input()
        #清屏
        os.system('CLS')
    except:
        pass
print("得分：", a)
time.sleep(5)