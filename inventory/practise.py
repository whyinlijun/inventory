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
        sql = "SELECT * FROM question WHERE q_type=? LIMIT ?"
        m_cursor.execute(sql,(q_type, int(quantity)))
    r_list = m_cursor.fetchall()
    m_cursor.close()
    return r_list

def practise(questions):
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
        if answer == q['answer'] or answer.upper()==q['answer']:
            defen += 1
            rights += 1
        else:
            if defen > 0 :
                defen -=1
            wrongs += 1
        
        print("正确答案是{}".format(q['answer']))
        input()
    print("练习结束，共练习{}题，总得分{}分，正确{}题，错误{}题，正确率{:.2f}%".format(
        counts, defen, rights, wrongs, rights/counts*100))


def main():
    conn = sqlite3.connect("../instance/question.sqlite")
    conn.row_factory=sqlite3.Row
    r = select_from_db(conn, '1', 2)
    practise(r)
    conn.close()


if __name__ == '__main__':
    main()