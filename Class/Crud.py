import sqlite3

class ClassCrud(object):
    def __init__(self):
        self.connection = ""
        return

    def Read(self, _query):
        self.connection = self.ConnectToDb()
        self.connection.text_factory = lambda b: b.decode(errors = 'ignore')
        result = self.connection.execute(_query)
        return result

    def GetWithId(self, _query, id):
        self.connection = self.ConnectToDb()
        self.connection.text_factory = lambda b: b.decode(errors = 'ignore')
        result = self.connection.execute(_query + id).fetchone()
        return result

    def GetWithIds(self, _query):
        self.connection = self.ConnectToDb()
        self.connection.text_factory = lambda b: b.decode(errors = 'ignore')
        result = self.connection.execute(_query).fetchone()
        return result


    def Add(self, _rows, _query):
        connection = self.ConnectToDb()
        cursor = connection.cursor()
        cursor.executemany(_query, _rows)
        connection.commit()
        cursor.close()
        connection.close()
        return

    def Update(self, _rows, _query):
        try:
            connection = self.ConnectToDb()
            cursor = connection.cursor()
            cursor.execute(_query, _rows)
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            print(e)
        return

    def Delete(self, _rows, _query):
        try:
            connection = self.ConnectToDb()
            cursor = connection.cursor()
            cursor.execute(_query, _rows)
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            print(e)
        return

    def ConnectToDb(self):
        return sqlite3.connect('db.s3db')

    def DisconnectToDb(self):
        self.connection.close()
