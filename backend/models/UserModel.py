from argon2 import PasswordHasher
from uuid import uuid4

from .BaseModel import BaseModel

class UserModel(BaseModel):
    def __init__(self, connection):
        self.connection = connection

    def CreateUser(self, userData):
        result = True
        try:
            cursor = self.connection.connection.cursor()
            newToken = self.GetNewToken()
            hasher = PasswordHasher()
            sql = '''
                INSERT INTO
                usuario
                (
                    username,
                    password,
                    email,
                    token
                )
                VALUES
                (
                    '{0}',
                    '{1}',
                    '{2}',
                    '{3}'
                )
                '''.format(
                    userData['username'],
                    hasher.hash(userData['password']),
                    userData['email'],
                    newToken
                )
            cursor.execute(sql)
            self.connection.connection.commit()
            result = True
        except Exception as err:
            result = False

        return result

    def GetUserByToken(self, request):
        '''
        Obtain the request, check if the token exists and if the user exists
        '''
        headers = request.headers
        bearer = headers.get('Authorization')
        token = None
        if bearer is not None:
            if len(bearer) > 0:
                token = bearer.split(' ')[1]

            cursor = self.connection.connection.cursor()
            sql = "SELECT * FROM usuario WHERE token = '{0}'".format(token)
            cursor.execute(sql)
            user = cursor.fetchone()
            result = user
        else:
            result = 'Authenticación requerida'
        
        return result

    
    def GetNewToken(self):
        tentativeToken = '{0}-{1}'.format(uuid4(), uuid4())
        cursor = self.connection.connection.cursor()
        sql = "SELECT token FROM usuario WHERE token = '{0}'"
        cursor.execute(sql.format(tentativeToken))
        tokenExists = cursor.fetchone()

        # Creamos tokens hasta que creemos uno único que no exista
        while tokenExists is not None:
            tentativeToken = '{0}-{1}'.format(uuid4(), uuid4())
            cursor.execute(sql.format(tentativeToken))
            tokenExists = cursor.fetchone()

        return tentativeToken
    
    def GetUserPublicData(self, token):
        cursor = self.connection.connection.cursor()
        sql = '''SELECT
            usuario.username,
            usuario.email,
            COUNT(nota.id) as notes
            FROM
            usuario
            INNER JOIN nota ON nota.usuario = usuario.id
            WHERE
            usuario.token = '{0}'
            GROUP BY
            usuario.id'''.format(token)
        
        cursor.execute(sql)
        return cursor.fetchone()
    
    def EmailExists(self, email):
        cursor = self.connection.connection.cursor()
        sql = "SELECT email FROM usuario WHERE email = '{0}'".format(email)
        cursor.execute(sql)
        data = cursor.fetchone()
        return data != None

    def UsernameExists(self, username):
        cursor = self.connection.connection.cursor()
        sql = "SELECT username FROM usuario WHERE username = '{0}'".format(username)
        cursor.execute(sql)
        data = cursor.fetchone()
        return data != None
    
    def TryLogin(self, username, password):
        cursor = self.connection.connection.cursor()
        hasher = PasswordHasher()
        sql = "SELECT password, token FROM usuario WHERE username = '{0}'".format(username)
        cursor.execute(sql)
        userExists = cursor.fetchone()
        if userExists is None:
            result = False
        else:
            realPassword = userExists['password']
            try:
                hasher.verify(realPassword, password)
                result = userExists['token']
            except Exception as err:
                result = False
        return result