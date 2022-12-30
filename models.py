import sqlite3
import json
from smtp import *

db = sqlite3.connect('serve.db', check_same_thread=False)

sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS users(
                           email TEXT,
                           password TEXT,
                           name TEXT,
                           surname TEXT,
                           address TEXT,
                           phone TEXT,
                           role_id INT
                           )
                           """)
db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS news(
                           name TEXT,
                           surname TEXT,
                           date TEXT,
                           url_photo TEXT,
                           title TEXT,
                           content TEXT)
                           """)
db.commit()
sql.execute("""CREATE TABLE IF NOT EXISTS anons(
                           name TEXT,
                           surname TEXT,
                           date TEXT,
                           url_photo TEXT,
                           title TEXT,
                           content TEXT)
                           """)
db.commit()
sql.execute("""CREATE TABLE IF NOT EXISTS events(
                           title TEXT,
                           author TEXT,
                           location TEXT,
                           data TEXT,
                           cost TEXT,
                           content TEXT)
                           """)
db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS messages(
                           name TEXT,
                           surname TEXT,
                           email TEXT,
                           date TEXT,
                           messages TEXT)
                           """)
db.commit()
sql.execute("""CREATE TABLE IF NOT EXISTS service(
                           author TEXT,
                           phone TEXT,
                           title TEXT,
                           description TEXT,
                           cost INT,
                           site TEXT)
                           """)
db.commit()


# def addServicedb(author, phone, title, description, cost, site):
#     sql.execute("INSERT INTO anons VALUES (?,?,?,?,?,?)", (author, phone, title, description, cost, site))
#     db.commit()

def sendUserEmail(data):
    sql.execute('''SELECT email FROM users ''')
    lst = []
    for email in sql.fetchall():
        lst.append(email[0])
    sendemail(lst, data)


def sendMessage(name, surname, email, date, messages):
    sql.execute("INSERT INTO messages VALUES (?,?,?,?,?)", (name, surname, email, date, messages))
    db.commit()


def getMessage():
    sql.execute('''SELECT * FROM messages ''')
    messages = sql.fetchall()
    all_messages = {"messages": []}
    # data = {
    #     "name": all_messages[0], "surname": all_messages[1], "email": all_messages[2], "date": all_messages[3],
    #     "messages": all_messages[4]
    # }

    for msg in messages:
        data = {
            "name": msg[0], "surname": msg[1], "email": msg[2], "date": msg[3],
            "messages": msg[4]
        }
        all_messages["messages"].append(data)

    return json.dumps(all_messages, ensure_ascii=False)


def getNewsdb():
    try:
        sql.execute('''SELECT * FROM news ''')
    except:
        print('please wait,  try later...')

    allNews = sql.fetchall()
    all_News = {"news": []}

    for news in allNews:
        data = {
            "name": news[0], "surname": news[1], "date": news[2], "url_photo": news[3],
            "title": news[4], "content": news[5]
        }
        all_News["news"].append(data)

    return json.dumps(all_News, ensure_ascii=False)


def getEventdb():
    sql.execute('''SELECT * FROM events ''')
    allEvent = sql.fetchall()
    print(allEvent)
    all_eventslst = {"events": []}
    # data = {
    #     "title": allEvent[0], "author": allEvent[1], "location": allEvent[2], "data": allEvent[3], "cost": allEvent[4],
    #     "content": allEvent[5]
    # }

    for events in allEvent:
        data = {
            "title": events[0], "author": events[1], "location": events[2], "date": events[3],
            "cost": events[4], "content": events[5]
        }
        all_eventslst["events"].append(data)

    return json.dumps(all_eventslst, ensure_ascii=False)


def getAnonsdb():
    sql.execute('''SELECT * FROM anons ''')
    allAnons = sql.fetchall()
    all_anons = {"anons": []}
    for anons in allAnons:
        data = {
            "name": anons[0], "surname": anons[1], "date": anons[2], "url_photo": anons[3],
            "title": anons[4], "content": anons[5]
        }
        all_anons["anons"].append(data)

    return json.dumps(all_anons, ensure_ascii=False)


#
#
def addAnonsdb(name, surname, date, url_photo, title, content):
    sql.execute("INSERT INTO anons VALUES (?,?,?,?,?,?)", (name, surname, date, url_photo, title, content))
    db.commit()


def addUsers(email, password):
    sql.execute(f'''SELECT email FROM users WHERE email =?''', (email,))
    if sql.fetchone() is None:
        sql.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?)",
                    (email, password, "None", "None", "None", "None", "None"))
        db.commit()
        return True
    else:
        return False


def updateUsers(email, password, name, surname, address, phone):
    sql.execute(f'''SELECT email FROM users WHERE email =?''', (email,))
    if sql.fetchone():
        sql.execute(
            f"UPDATE users SET name ='{name}', surname = '{surname}', address = '{address}', phone = '{phone}', role_id ='{0}' ")
        db.commit()
        return True
    else:
        return False


def check_login(email, password):
    sql.execute(f'''SELECT email FROM users WHERE email = ?''', (email,))
    user_email = sql.fetchone()
    if user_email is None:
        return False
    else:
        print(user_email)
        if user_email[0] == email:
            sql.execute('''SELECT password FROM users WHERE email = ?''', (email,))
            user_password = sql.fetchone()[0]
            if user_password == password:
                sql.execute(f'''SELECT email,password,name,surname,address,phone,role_id FROM users WHERE email = ?''',
                            (email,))
                data = sql.fetchall()[0]
                print()
                send_data = {
                    "email": data[0], "password": data[1], "name": data[2], "surname": data[3], "address": data[4],
                    "phone": data[5], "role_id": data[6]
                }
                print(send_data)
                return json.dumps(send_data, ensure_ascii=False)
                # return json.dumps(data, ensure_ascii=False)
