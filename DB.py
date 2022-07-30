import sys
from mysql.connector import connect
import names
import random
"""
DB_HOST_IP = sys.argv[1]
DB_NAME = sys.argv[2]
USERNAME = sys.argv[3]
PASSWORD = sys.argv[4]
DB_HOST_PORT=3306
"""
#DB init
DB_HOST_IP = 'localhost'
DB_NAME = 'test1'
USERNAME = 'root'
PASSWORD = '@yq5xr19W'
DB_HOST_PORT=3306

global cursor
global conn

def db_init(host, db_name, user, password,port):
    conn = connect(
                    user=user,
                    password=password,
                    host=host,
                    db=db_name,
                     port=port,
                     )
    return conn

def db_create(db_name):
    create_db = f"CREATE DATABASE if not exists {db_name};"
    cursor = conn.cursor()  # this one returns MySQLCursor
    cursor.execute(create_db)


#sql query
def many_queries(query,iterations,):
    db_use = f"use {DB_NAME}"
    cursor.execute(db_use)
    for q in query:
        for i in range(iterations):
            cursor.execute(q)
    conn.commit()
#generate random names
def generate_names(iterations):
    firstName=[]
    lastName=[]
    for i in range(iterations):
        firstName.append(names.get_first_name())
        lastName.append(names.get_last_name())
    return  firstName ,lastName

#create tables of DB
def tbl_create():

    query_usersTbl=f"create table if not exists users (uid int not null,name varchar(20) not null , " \
                   f"lastName varchar(20) not null, primary key (uid));"
    query_moneyTbl=l=f"create table if not exists users (uid int not null, " \
                     f"currancy int check(currancy between 1 and 3) not null,sum int default 0," \
                     f"foreign key (uid) references users(uid)," \
                     f"primary key (uid,currancy));"
    many_queries([query_usersTbl,query_moneyTbl],1)

#populate the tables
def populate_names(first_name,last_name,iterations):
    query_names=[]
    for i in range(iterations):
        query_names.append(f'insert into users (uid,name,lastName) values({i},"{first_name[i]}","{last_name[i]}") ON DUPLICATE KEY UPDATE name="{first_name[i]}",lastName="{last_name[i]}";')
    many_queries(query_names,1)

def populate_money(iterations):
    query_money = []
    rand_money=[]
    for i in range(iterations):
        for j in range(3):
            rand_money.append(random.randint(-999999999, 999999999))
        query_money.append(f"insert into money (uid,currancy,sum) values({i},1,{rand_money[0]})ON DUPLICATE KEY UPDATE sum={rand_money[0]};")
        query_money.append(f"insert into money (uid,currancy,sum) values({i},2,{rand_money[1]})ON DUPLICATE KEY UPDATE sum={rand_money[1]};")
        query_money.append(f"insert into money (uid,currancy,sum) values({i},3,{rand_money[2]}) ON DUPLICATE KEY UPDATE sum={rand_money[2]};")
        rand_money = []
    many_queries(query_money, 1)

def get_fullName_by_id(id):
    cursor.execute(f"select * from {DB_NAME}.users where uid = {id};")
    for record in cursor.fetchall():
        print(f"++++++++++")
        print(f"id: {record[0]}")
        print(f"first_name: {record[1]}")
        print(f"last_name: {record[2]}")


def get_money_by_id(id):
    cursor.execute(f"select * from {DB_NAME}.money where uid = {id};")
    for record in cursor.fetchall():
        print(f"------------")
        #print(f"id: {record[0]}")
        print(f"currency: {record[1]}")
        print(f"sum: {record[2]}")
    print(f"++++++++++")


if __name__=='__main__':
    global conn
    conn = db_init(DB_HOST_IP, DB_NAME, USERNAME, PASSWORD,DB_HOST_PORT)
    global cursor
    cursor = conn.cursor()  # this one returns MySQLCursor

    #tables creation
    db_create(DB_NAME)
    tbl_create()
    #table population
    iterations=100
    first_name, last_name = generate_names(iterations)
    populate_names(first_name,last_name,iterations)
    populate_money(iterations)

    rand_id=random.randint(0, 99)
    get_fullName_by_id(rand_id)
    get_money_by_id(rand_id)






