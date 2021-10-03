import graphene
import mysql.connector as mysql

class Login(graphene.ObjectType):
    # username = graphene.String()
    # password = graphene.String()
    # dbname = graphene.String()
    # conn = graphene.String()
    table = graphene.String()

class Params(graphene.ObjectType):
    columns = graphene.String()

class Authors(graphene.ObjectType):
    a_id = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()

class Book_author(graphene.ObjectType):
    author_id = graphene.String()
    book_id = graphene.String()

class Books(graphene.ObjectType):
    b_id = graphene.String()
    title = graphene.String()
    isbn = graphene.String()

class Queries(graphene.ObjectType):
    authors = graphene.List(Authors)
    books = graphene.List(Books)
    login = graphene.List(Login, username=graphene.String(),password=graphene.String(),dbname=graphene.String())
    params = graphene.List(Params, username=graphene.String(),password=graphene.String(),dbname=graphene.String(),tbname=graphene.String())
    print("hi")
    def resolve_login(self,info,username,password,dbname):
        text = "hi"
        print("Hi")
        db = mysql.connect(
            host="localhost",
            database=dbname,
            user=username,
            passwd=password,
            auth_plugin='mysql_native_password'
        )
        if db.is_connected():
            text= "Connected to mysql"
        else:
            text= "Connection error"
        
        print(text)
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = \'{}\'".format(dbname)
        # print("SELECT table_name FROM information_schema.tables WHERE table_schema = \'{}\'".format(dbname))
        cursor = db.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        login = []
        # text=Login(conn=text)
        for i in records:
            print(i[0])
            login.append(Login(table=i[0]))
        print(login)
        return login

    def resolve_params(self, info, username,password,dbname,tbname):
        db = mysql.connect(
            host="localhost",
            database=dbname,
            user=username,
            passwd=password,
            auth_plugin='mysql_native_password'
        )
        query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = \'{}\' AND TABLE_NAME = \'{}\'".format(dbname,tbname)
        cursor = db.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        columns = []
        for i in records:
            print(i[0])
            columns.append(Params(columns=i[0]))
        print(columns)
        return columns


    def resolve_authors(self, info):
        db = mysql.connect(
            host="localhost",
            database="python_mysql",
            user="varchala",
            passwd="Budankai_123",
            auth_plugin='mysql_native_password'
        )
        print("hi")
        query = "select first_name,last_name from authors"
        cursor = db.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        #if len(records) == 0:
        #  return ??
        authors = []
        for record in records:
            authors.append(Authors(first_name=record[0],last_name=record[1]))
        print(authors)
        return authors

    def resolve_books(self, info):
        db = mysql.connect(
           host="localhost",
            database="python_mysql",
            user="varchala",
            passwd="Budankai_123",
            auth_plugin='mysql_native_password'
        )
        query = "select title,isbn from books"
        cursor = db.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        #if len(records) == 0:
        #  return ??
        books = []
        for record in records:
            books.append(Books(title=record[0],isbn=record[1]))
        return books

# def main():
schema = graphene.Schema(query=Queries)

# if __name__ == '__main__':
#     main()