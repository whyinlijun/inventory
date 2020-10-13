import re
q_sting = """1.专职安全生产管理人负定指经建设主管部门或者其他有关部门安全生产老考核合格取得安全生产考核合格证书,并在建筑施工企业及其项目从事(B)工作的专职人员,
A.施工管理
B.安全生产管理
C.工程技术
D.工程机械
2.建筑施工企业应当依法设置(C),在企业主要负责人的3领导下开展本企业的安全生产管理工作.
A.项目负责人
B.工程管理机构
C.安全生产管理机构
D.安全管理人员
3.
"""

def question(q_sting):
    q_list = q_sting.split('\n')
    q_dict = {}
    r_compile=re.compile('\(([a-zA-Z])\)')
    q_dict['answer'] = r_compile.search(q_list[0]).group()[1]
    q_dict['question']=re.sub(r_compile, '(   )', q_list[0])
    q_dict['amswer_list'] = q_list[1:]
    q_dict['id'] = re.match('\d+', q_list[0]).group()
    return q_dict

with open("bb.txt", 'r',encoding='utf8') as f:
    txt = f.read()
    '''
    questions = re.findall('\d.*?D\.', txt,re.S)
    for i in questions:
        print(i)
    print(len(questions))
    '''

 
    for i in range(1,559):
        #item = re.findall(r'(1.*)2\.', q_sting, re.S)
        #c_string = r'(^{}.*){}\.'.format(str(i),str(i+1))
        print(i)
        a= re.search('(' + str(i) + '.*?)' + str(i + 1) , txt, re.S).group(1)
        print(a)
      

