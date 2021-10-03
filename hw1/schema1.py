import graphene
from graphene import ObjectType, String, Schema
from mysql.connector import MySQLConnection, Error 
from python_mysql_dbconfig import read_db_config

class Authors(graphene.ObjectType):
    id=graphene.Int()
    first_name=graphene.String()
    last_name=graphene.String()
    photo=graphene.String()

class Book_author(graphene.ObjectType):
    book_id=graphene.Int()
    author_id=graphene.Int()

class Books(graphene.ObjectType):
    id1=graphene.Int()
    title=graphene.String()
    isbn=graphene.String()

class Query(graphene.ObjectType):
    all_books=graphene.List(Books)

    def resolve_all_books(self,info):
        db_config=read_db_config()
        db=None
        db=MySQLConnection(**db_config)
        query='SELECT * FROM books'
        cursor=db.cursor()
        cursor.execute(query)
        recs=cursor.fetchall()
        cursor.close()
        db.close()
        all_books=[]
        for r in recs:
            all_books.append(Books(id1=r[0],title=r[1], isbn=r[2]))
        return all_books

schema = graphene.Schema(query=Query)




