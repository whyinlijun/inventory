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

def question(q_string):
    error = 0
    q_dict = {}
    q_list = q_string.split('\n')
    q_rows = len(q_list)
    q = q_list[0].strip()
    if q_rows>5:
        for i in range(1,q_rows-5):
            q += q_list[i].strip()
    r_compile=re.compile('[\(|（]([a-gA-G])[\)|）]',re.S)
    try:
        q_dict['answer'] = r_compile.search(q).group(1)
        q_dict['question']=re.sub(r_compile, '(   )', q)
        if q_rows>5:
            q_dict['answer_list'] = q_list[q_rows-5:]
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
    

    r_list = read_data_from_file(filename)
    for item in r_list:
        q = question(item)
        conn.execute(
            "INSERT INTO question (xuhao, q_type, question, answer_list, answer) VALUES(?,?,?,?,?)",
            (pre_id + q['id'], q_type, q['question'], '\n'.join(q['answer_list']), q['answer'])
            )
        conn.commit()
    


def  test(filename):
    r_list = read_data_from_file(filename)
    for item in r_list:
        question(item)

def main(init_db=None):
    conn = sqlite3.connect("../instance/question.sqlite")
    if init_db:
        db_init(conn)
    q_pre = input("请输入前缀：")
    fs = input('请输入读取文件名：')
    save_to_database(conn, fs, q_pre)
    conn.close()


if __name__ =="__main__":
    main()
    #test('onechoice-two.txt')
    


