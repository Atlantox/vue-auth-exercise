from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

from helpers import *
from models.NoteModel import NoteModel
from models.UserModel import UserModel

from config import config

app = Flask(__name__)
connection = MySQL(app)
noteModel = NoteModel(connection)
userModel = UserModel(connection)

def NotFound():
    return jsonify({'success': False, 'message': 'Ruta no encontrada'}), 404


@app.route('/notes', methods=['GET'])
def GetNotesOfUser():
    response = {}
    statusCode = 200
    error = ''
    token = GetTokenOfRequest(request)
    if token == None:
        error = 'Acceso denegado. Autenticación requerida'
        statusCode = 401
    
    if error == '':
        targetUser = userModel.GetUserByToken(token)
        if targetUser == None:
            error = 'Usuario no encontrado'
            statusCode = 401
    
    if error == '':
        notes = noteModel.GetNotesOfUser(targetUser['id'])
        response = {'success': True, 'notes': notes}
    else:
        response = {'success': False, 'message': error}

    return jsonify(response), statusCode

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, NotFound)
    app.run()