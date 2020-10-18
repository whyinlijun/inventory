import re
import sqlite3

def read_data_from_file(filename):
    r_list = []
    error = 0
    with open(filename, 'r',encoding='utf8') as f:
        content = f.read()
        #提取题目前的序号，以数字开头以点结尾
        num = re.findall('(^\d+)[./,]',content,re.M)
        #确定有多少题，最后一个减前一个，并且最后一个与总数相差不大于10
        if int(num[-1])  - int(num[-2]) == 1 and len(num) - int(num[-1])<10:
            rows = int(num[-1])
        else:
            rows = len(num)
        for i in range(1,rows):
            #print(i)
            try:
                a= re.search(
                    '(' + str(i) + '[\.|,].*?)' + str(i + 1)+'[\.|,]' , content, re.S
                    ).group(1)
                r_list.append(a)
            except:
                print(i)
                error += 1
        print('试题分段错误{}'.format(error,))
    return r_list

def question(q_string, answer_linst_num=4):
    """
    answer_list_num答案列表数量
    一般单选为4，多选为5
    """
    error = 0
    q_dict = {}
    q_list = q_string.split('\n')
    q_rows = len(q_list)
    q = q_list[0].strip()
    if q_rows>answer_linst_num+1:
        for i in range(1,q_rows-(answer_linst_num+1)):
            q += q_list[i].strip()
    r_compile=re.compile('[\(|（]\s*([a-gA-G]+|正确|错误)\s*[\)|）]',re.S)
    try:
        q_dict['answer'] = r_compile.search(q).group(1)
        #判断题答案变更
        if answer_linst_num == 0:
            if q_dict['answer']=='正确':
                q_dict['answer'] = 'Y'
            else:
                q_dict['answer'] = 'N'
        q_dict['question']=re.sub(r_compile, '(   )', q)
        if q_rows>answer_linst_num+1:
            q_dict['answer_list'] = q_list[q_rows-(answer_linst_num+1):]
        else:
            q_dict['answer_list'] = q_list[1:]
        q_dict['id'] = re.match('\d+', q).group()
        #print(q_dict)
    except:
        print(q_string)
    return q_dict

def db_init(db_conn):
    db_conn.execute("DROP TABLE  IF EXISTS question")
    db_conn.execute(
        """CREATE TABLE IF NOT EXISTS question (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            xuhao TEXT,
            q_type TEXT,
            question TEXT NOT NULL,
            answer_list TEXT NOT NULL,
            answer text NOT NULL) """
        )
    db_conn.execute("DROP TABLE  IF EXISTS wrongs")
    db_conn.execute(
        """CREATE TABLE IF NOT EXISTS wrongs(
            id INTEGER PRIMARY KEY NOT NULL,
            count INTEGER DEFAULT 1)"""
        )
    db_conn.execute("DROP TABLE  IF EXISTS counts")
    db_conn.execute(
        """CREATE TABLE IF NOT EXISTS counts(
            id INTEGER PRIMARY KEY NOT NULL,
            selected_times INTEGER DEFAULT 1,
            right_times INTEGER ,
            wrong_times INTEGER)"""
        )
    db_conn.commit()

def save_to_database(conn, filename, pre_id='_', q_type='1'):
    '''
    qtype:1为单选，2为多选，3为判断
    '''
    if q_type == '1':
        answer_list_num = 4
    elif q_type == '2':
        answer_list_num = 5
    elif q_type == '3':
        answer_list_num = 0

    r_list = read_data_from_file(filename)
    for item in r_list:
        q = question(item, answer_list_num)
        conn.execute(
            "INSERT INTO question (xuhao, q_type, question, answer_list, answer) VALUES(?,?,?,?,?)",
            (pre_id + q['id'], q_type, q['question'], '\n'.join(q['answer_list']), q['answer'])
            )
        conn.commit()
    


def  test(filename, num):
    r_list = read_data_from_file(filename)
    for item in r_list:
        s=question(item,num)
    for key in s:
        print("{}:{}".format(key,s[key]))

def main(init_db=None):
    conn = sqlite3.connect("../instance/question.sqlite")
    if init_db:
        db_init(conn)
    q_type =input("请输入题型,1为单选，2为多选，3为判断:  ")
    q_pre = input("请输入前缀：")
    fs = input('请输入读取文件名：')
    save_to_database(conn, fs, q_pre, q_type)
    conn.close()

def test_all():
    fs_dict = {'choice':4,'mchoice':5,'true_or_false':0}
    for item in fs_dict:
        for i in range(1,4):
            s = '{}-{}.txt'.format(item, i)
            print("正在测试{}".format(s))
            test(s, fs_dict[item])

if __name__ =="__main__":
    main()
    #test_all()


