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
            m_cursor.execute("SELECT * FROM counts WHERE id=?", (q['id'],))
            r_count = m_cursor.fetchone()
            if r_count:
                m_cursor.execute(
                    "REPLACE INTO counts (id, selected_times, wrong_times) VALUES(?, ?, ?)",
                    (q['id'], r_count['selected_times']+1, r_count['wrong_times']+1 )
                    )
            else:
                m_cursor.execute("INSERT INTO counts (id, wrong_times ) VALUES(?, ?)",(q['id'], 1))
        print("正确答案是{}".format(q['answer']))
        input()
    print("练习结束，共练习{}题，总得分{}分，正确{}题，错误{}题，正确率{:.2f}%".format(
        counts, defen, rights, wrongs, rights/counts*100))


def main():
    conn = sqlite3.connect("../instance/question.sqlite")
    conn.row_factory=sqlite3.Row
    r = select_from_db(conn, '1', 2)
    practise(conn, r)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()