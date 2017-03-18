import psycopg2 as psql
from DCube_params import *


def connect_db():
    db_conn = psql.connect("host='localhost' dbname=%s user=%s password=%s port=%d" % (PSQL_DB, PSQL_DB_USER, PSQL_DB_PWD, PSQL_DB_PORT))
    print "Connected to database"
    return db_conn


def close_db(db_conn):
    db_conn.close()
    print "Disconnected to database"


def drop_and_copy_table(db_conn, from_table, to_table, columns, copy_data=True, can_pass=False):
    if DEBUG and can_pass:
        return
    cur = db_conn.cursor()
    cur.execute("drop table if exists %s" % to_table)
    sql = "select %s into %s from %s" % (columns, to_table, from_table)
    if not copy_data:
        sql += " where 1=2"
    cur.execute(sql)
    db_conn.commit()
    cur.close()


def drop_and_create_table(db_conn, table, column_define, can_pass=False):
    if DEBUG and can_pass:
        return
    cur = db_conn.cursor()
    cur.execute("drop table if exists %s" % table)
    sql = "create table %s(%s)" % (table, column_define)
    cur.execute(sql)
    db_conn.commit()
    cur.close()


def drop_table(db_conn, table):
    cur = db_conn.cursor()
    cur.execute("drop table if exists %s" % table)
    db_conn.commit()
    cur.close()


def exec_sql(db_conn, sql):
    cur = db_conn.cursor()
    cur.execute(sql)
    db_conn.commit()
    cur.close()


def get_first_res(db_conn, sql):
    cur = db_conn.cursor()
    cur.execute(sql)
    val = cur.fetchone()[0]
    db_conn.commit()
    cur.close()
    return val


def insert(db_conn, table, values):
    cur = db_conn.cursor()
    sql = "insert into %s values(%s)" % (table, values)
    cur.execute(sql)
    db_conn.commit()
    cur.close()


def update(db_conn, table, values_and_where):
    cur = db_conn.cursor()
    sql = "update %s set %s" % (table, values_and_where)
    cur.execute(sql)
    db_conn.commit()
    cur.close()