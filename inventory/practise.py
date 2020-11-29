import sqlite3
import os

#选择练习类型
#选择练习数量
#开始练习
#评分

def select_from_db(conn, q_type, quantity=None):
    m_cursor = conn.cursor()
    if quantity == None:
        sql = "SELECT * FROM question WHERE q_type=?"
        m_cursor.execute(sql,(q_type,))
       
    else:
        sql = "SELECT * FROM question WHERE q_type=? ORDER BY random() LIMIT ?"
        m_cursor.execute(sql,(q_type, int(quantity)))
    r_list = m_cursor.fetchall()
    m_cursor.close()
    return r_list

def practise(conn, questions):
    defen = 0
    rights = 0
    wrongs = 0
    counts = 0
    for q in questions:
        counts += 1
        os.system("CLS")
        print("第{}题，目前得分{}分，正确{}题，错误{}题。".format(counts, defen, rights, wrongs))
        print()
        print(q['question'])
        print()
        print(q['answer_list'])
        answer = input("请输入答案：")
        m_cursor = conn.cursor()
        if answer == q['answer'] or answer.upper()==q['answer']:
            defen += 1
            rights += 1
        else:
            if defen > 0 :
                defen -=1
            wrongs += 1
            m_cursor.execute("SELECT * FROM wrongs WHERE id=?", (q['id'],))
            r_wrong = m_cursor.fetchone()
            if r_wrong:
                m_cursor.execute("REPLACE INTO wrongs VALUES (?, ?)",(q['id'], r_wrong['count']+1 ))
            else:
                m_cursor.execute("INSERT INTO wrongs (id) VALUES (?)",(q['id'],))
        
        print("正确答案是{}".format(q['answer']))
        input()
    print("练习结束，共练习{}题，总得分{}分，正确{}题，错误{}题，正确率{:.2f}%".format(
        counts, defen, rights, wrongs, rights/counts*100))

def select_from_sql(sql, conn):
    m_cursor = conn.cursor()
    m_cursor.execute(sql)
    r = m_cursor.fetchall()
    m_cursor.close()
    return r

def main(sql_s=None):
    conn = sqlite3.connect("../instance/question.sqlite")
    conn.row_factory=sqlite3.Row
    if not sql_s :
        print("请输入练习模式，1为自由练习，2为错题练习")
        choice = input("：")
        if choice == '1':    
            sql_s = input("请输入sql语句:  ")
            
        else:
            sql_s = "SELECT * FROM question INNER JOIN wrongs ON question.id = wrongs.id"
    r = select_from_sql(sql_s, conn)
    practise(conn, r)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    sql = "SELECT * FROM question WHERE q_type='1' AND xuhao like 'sw%' ORDER BY random() limit 30"
    main(sql)