import configparser
import os
import psycopg2
from psycopg2.extras import execute_values



configuartion_path = "D:\PDS\PDS API\Database Connection\config\config.ini"
config = configparser.ConfigParser()
config.read(configuartion_path);

host     = config['cred']['host'];
db_name  = config['cred']['db_name'];
user     = config['cred']['user'];
password = config['cred']['password'];

class Student():

    conn = psycopg2.connect(database=db_name,host=host,user=user,password=password);
    conn.autocommit = True

    cur = conn.cursor();

    @classmethod
    def create_table(cls):

        cls.cur.execute("select * from information_schema.tables where table_name= 'STUDENT' ");
        x = bool(cls.cur.rowcount);

        if(x):
            pass;
        else:
         cls.cur.execute("CREATE TABLE STUDENT (std_id varchar(50),std_name VARCHAR(100))");

         cls.conn.commit();

    @classmethod
    def get_data(cls,name):

        cls.cur.execute("SELECT * FROM STUDENT WHERE std_name=%s",(name,));

        rows = cls.cur.fetchall();

        return rows

    @classmethod
    def insert_data(cls,tup):

        try:
         #execute_values(cls.cur,"INSERT INTO STUDENT (std_id,std_name) VALUES %s",tup);
         cls.cur.executemany("INSERT INTO STUDENT (std_id,std_name) VALUES (%s,%s)", tup);
         cls.conn.commit();
         return dict(tup);
        except Exception as e:
         print(e);
         cls.conn.rollback();


    @classmethod
    def delete_data(cls,id):

        cls.cur.execute("DELETE FROM STUDENT WHERE std_id =%s",(id,))







