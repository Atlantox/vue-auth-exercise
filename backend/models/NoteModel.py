from .BaseModel import BaseModel
class NoteModel(BaseModel):
    def __init__(self, connection):
        self.connection = connection

    def CreateNote(self, noteData, userId):
        result = True
        try:
            sql = '''
                INSERT INTO
                nota
                (
                    usuario,
                    titulo,
                    contenido
                )
                VALUES
                (
                    {0},
                    '{1}',
                    '{2}'
                )
                '''.format(
                    userId,
                    noteData['titulo'],
                    noteData['contenido']
                )
            cursor = self.connection.connection.cursor()
            cursor.execute(sql)
            self.connection.connection.commit()
            result = True
        except Exception as err:
            result = False

        return result

    def GetNotesOfUser(self, userId):
        cursor = self.connection.connection.cursor()
        sql = "SELECT * FROM nota WHERE usuario = {0}".format(userId)
        cursor.execute(sql)
        return cursor.fetchall()
    
    def GetNoteById(self, noteId):
        cursor = self.connection.connection.cursor()
        sql = "SELECT * FROM nota WHERE id = {0}".format(noteId)
        cursor.execute(sql)
        return cursor.fetchone()
    
    def NoteCorrespondsToUser(self, noteId, userId):
        cursor = self.connection.connection.cursor()
        sql = '''
            SELECT
            *
            FROM
            nota
            WHERE
            id = {0} AND
            usuario = {1}
            '''.format(noteId, userId)
        
        cursor.execute(sql)
        return cursor.fetchone()
    
    def UpdateNote(self, noteData, noteId):
        cursor = self.connection.connection.cursor()
        sql = 'UPDATE nota SET '

        for column, value in noteData.items():
            sql += "{0} = '{1}', ".format(column, value)
        
        sql = sql[0:-2] + " WHERE id = {0}".format(noteId)
        try:
            cursor.execute(sql)
            self.connection.connection.commit()
            result = True
        except Exception as err:
            result = False 
        
        return result
    
    def DeleteNote(self, noteId):
        result = True
        try:
            cursor = self.connection.connection.cursor()
            sql = "DELETE FROM nota WHERE id = {0}".format(noteId)
            cursor.execute(sql)
            self.connection.connection.commit()
        except Exception as err:
            result = False

        return result