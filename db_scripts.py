#Суббота 18:00
import sqlite3
db_name = 'quiz.sqlite'
conn: sqlite3.Connection
cursor: sqlite3.Cursor

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def clear_db():
    ''' удаляет все таблицы '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()

    
def create():
    open()

    do('''PRAGMA foreign_keys=on''')

    do('''CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY,
        name VARCHAR)''')

    do('''CREATE TABLE IF NOT EXISTS question (
        id INTEGER PRIMARY KEY,
        question VARCHAR,
        answer VARCHAR,
        wrong1 VARCHAR,
        wrong2 VARCHAR,
        wrong3 VARCHAR)''')

    do('''CREATE TABLE IF NOT EXISTS quiz_content (
        id INTEGER PRIMARY KEY,
        quiz_id INTEGER,
        question_id INTEGER,
        FOREIGN KEY (quiz_id) REFERENCES quiz (id),
        FOREIGN KEY (question_id) REFERENCES question (id))''')

def add_questions():
    questions = [
        ("Какой сегодня день?", "02.03.2024", "12.04.2022", "13.02.2025", "07.09.2021"),
        ("Какой завтра день?", "03.03.2024", "12.04.2022", "13.02.2025", "07.09.2021"),
        ("Какого цвета банан?", "Желтого", "Красного", "Зеленого", "Оранжевого"),
        ("Вопрос 1?", "02.03.2024", "12.04.2022", "13.02.2025", "07.09.2021"),
        ("Какой 2?", "02.03.2024", "12.04.2022", "13.02.2025", "07.09.2021"),
        ("Какой 3?", "02.03.2024", "12.04.2022", "13.02.2025", "07.09.2021"),
    ]
    open()
    query = '''INSERT INTO question (question, answer, wrong1, wrong2, wrong3)
                VALUES (?,?,?,?,?)'''
    cursor.executemany(query, questions)
    conn.commit()

def add_quizes():
    quizes = [
        ('Самый умный', ),
        ('Кто хочет стать миллионером?', ),
        ('Еще одна викторина', )
    ]
    open()
    query = '''INSERT INTO quiz (name) VALUES (?)'''
    cursor.executemany(query, quizes)
    conn.commit()

def add_links():
    links = input('Введите связи в формате викторина,вопрос "1,1 2,1 3,1":')
    links = links.split()
    result = []
    for link in links:
        quiz_id, question_id = list(map(int, link.split(',')))
        result.append((quiz_id, question_id))
    query = '''INSERT INTO quiz_content (quiz_id, question_id) VALUES (?, ?)'''
    open()
    cursor.executemany(query, result)
    conn.commit()
    close()

def get_question_after(question_id=0, quiz_id=0):
    query = '''SELECT quiz_content.id, question.question, question.answer,
    question.wrong1, question.wrong2, question.wrong3 FROM quiz_content, question
    WHERE quiz_content.question_id = question.id AND quiz_content.id > ? AND
    quiz_content.quiz_id = ? ORDER BY quiz_content.id'''
    open()
    cursor.execute(query, [question_id, quiz_id])
    result = cursor.fetchone()
    close()
    return result

def get_quizes():
    query = '''SELECT * FROM quiz ORDER BY id'''
    open()
    cursor.execute(query)
    result = cursor.fetchall()
    close()
    return result

def check_answer(question_id, answer):
    query = '''SELECT question.answer
    FROM quiz_content, question
    WHERE quiz_content.id = ?
    AND quiz_content.question_id = question.id'''
    open()
    cursor.execute(query, [str(question_id)])
    result = cursor.fetchone()
    close()
    if result is None:
        return False
    else:
        return result[0] == answer 
    
def get_questions(limit, offset):
    query = '''SELECT * FROM question ORDER BY id LIMIT ? OFFSET ?'''
    open()
    cursor.execute(query, [limit, offset])
    result = cursor.fetchall()
    close()
    return result

def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

def main():
    clear_db()
    create()
    show_tables()
    add_quizes()
    add_questions()
    add_links()

if __name__ == "__main__":
    main()


# Python ПТ 19:30
# import sqlite3
# db_name = 'quiz.sqlite'
# conn = None
# cursor = None

# def open():
#     global conn, cursor
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()

# def close():
#     cursor.close()
#     conn.close()

# def do(query):
#     cursor.execute(query)
#     conn.commit()

# def clear_db():
#     ''' удаляет все таблицы '''
#     open()
#     query = '''DROP TABLE IF EXISTS quiz_content'''
#     do(query)
#     query = '''DROP TABLE IF EXISTS question'''
#     do(query)
#     query = '''DROP TABLE IF EXISTS quiz'''
#     do(query)
#     close()

    
# def create():
#     open()
#     do('''PRAGMA foreign_keys=on''')

#     do('''CREATE TABLE IF NOT EXISTS quiz (
#         id INTEGER PRIMARY KEY,
#         name VARCHAR)''')

#     do('''CREATE TABLE IF NOT EXISTS question (
#        id INTEGER PRIMARY KEY,
#        question VARCHAR,
#        answer VARCHAR,
#        wrong1 VARCHAR,
#        wrong2 VARCHAR,
#        wrong3 VARCHAR)''')
    
#     do('''CREATE TABLE IF NOT EXISTS quiz_content (
#        id INTEGER PRIMARY KEY,
#        quiz_id INTEGER,
#        question_id INTEGER,
#        FOREIGN KEY (quiz_id) REFERENCES quiz (id),
#        FOREIGN KEY (question_id) REFERENCES question (id))''')

#     close()

# def add_questions():
#     questions = [
#         ('Сколько месяцев в году имеют 28 дней?', 'Все', 'Один', 'Ни одного', 'Два'),
#         ('Каким станет зелёный утёс, если упадёт в Красное море?', 'Мокрым', 'Красным', 'Не изменится', 'Фиолетовым'),
#         ('Какой рукой лучше размешивать чай?', 'Ложкой', 'Правой', 'Левой', 'Любой'),
#         ('Что не имеет длины, глубины, ширины, высоты, а можно измерить?', 'Время', 'Глупость', 'Море', 'Воздух'),
#         ('Когда сетью можно вытянуть воду?', 'Когда вода замёрзла', 'Когда нет рыбы', 'Когда уплыла золотая рыбка', 'Когда сеть порвалась'),
#         ('Что больше слона и ничего не весит?', 'Тень слона', 'Воздушный шар', 'Парашют', 'Облако')
#     ]
#     open()
#     query = '''INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (?, ?, ?, ?, ?)'''
#     cursor.executemany(query, questions)
#     conn.commit()
#     close()

# def add_quiz():
#     quizes = [
#         ('Своя игра', ),
#         ('Кто хочет стать миллионером?', ),
#         ('Самый умный', )
#     ]
#     open()
#     query = '''INSERT INTO quiz (name) VALUES (?)'''
#     cursor.executemany(query, quizes)
#     conn.commit()
#     close()

# def add_links():
#     links = input('Введите ссылки в формате "1,1 1,2 2,3":')
#     links = links.split()
#     for i in range(len(links)):
#         quiz_id, question_id = list(map(int, links[i].split(',')))
#         links[i] = (quiz_id, question_id)
#     open()
#     cursor.executemany('''INSERT INTO quiz_content (quiz_id, question_id) VALUES (?, ?)''', links)
#     conn.commit()
#     close()

# def get_question_after(question_id=0, quiz_id=1):
#     open()
#     query = '''SELECT quiz_content.id, question.question, question.answer, question.wrong1,
#     question.wrong2, question.wrong3 FROM question, quiz_content 
#     WHERE quiz_content.question_id = question.id AND
#     quiz_content.id > ? AND quiz_content.quiz_id = ? ORDER BY quiz_content.id'''
#     cursor.execute(query, [question_id, quiz_id])
#     result = cursor.fetchone()
#     close()
#     return result

# def show(table):
#     query = 'SELECT * FROM ' + table
#     open()
#     cursor.execute(query)
#     print(cursor.fetchall())
#     close()

# def show_tables():
#     show('question')
#     show('quiz')
#     show('quiz_content')

# def main():
#     clear_db()
#     create()
#     add_questions()
#     add_quiz()
#     add_links()
#     show_tables()
#     print(get_question_after(3, 1))

# if __name__ == "__main__":
#     main()