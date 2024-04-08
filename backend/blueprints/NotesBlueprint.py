from flask import Blueprint, request, jsonify

from models.NoteModel import NoteModel
from models.UserModel import UserModel
from helpers import *

notesBlueprint = Blueprint('notes', __name__)

def initModels():
    connection = getattr(notesBlueprint, 'connection', None)
    if connection is None:
        raise Exception('No se pudo obtener la conexión desde el Blueprint Notes')
    
    return NoteModel(connection), UserModel(connection)


@notesBlueprint.route('/notes', methods=['GET'])
def GetNotesOfUser():
    noteModel, userModel = initModels()
    statusCode = 200
    error = ''
    if error == '':
        targetUser = userModel.GetUserByToken(request)
        if type(targetUser) is str:
            error = targetUser
            statusCode = 400
    
    if error == '':
        notes = noteModel.GetNotesOfUser(targetUser['id'])
        response = {'success': True, 'notes': notes}
    else:
        response = {'success': False, 'message': error}    

    return jsonify(response), statusCode


@notesBlueprint.route('/notes/<int:noteId>', methods=['GET'])
def GetNoteById(noteId):
    statusCode = 200
    result = ValidateNoteAndUser(request, noteId)
    if type(result) is str:
        response = {'success': False, 'message': result}    
        statusCode = 400
    else:
        response = {'success': True, 'note': result}

    return jsonify(response), statusCode


@notesBlueprint.route('/notes', methods=['POST'])
def CreateNote():
    noteModel, userModel = initModels()
    recievedData, error, statusCode = JsonExists(request)

    if error == '':
        targetUser = userModel.GetUserByToken(request)
        if type(targetUser) is str:
            error = targetUser
            statusCode = 400
    
    if error == '':
        filteredData = ValidateNoteData(recievedData)
        if type(filteredData) is str :
            error = filteredData
            statusCode = 400
    print(error, '<- errorcito')
    if error == '':
        created = noteModel.CreateNote(recievedData, targetUser['id'])
        if created is False:
            error = 'Hubo un error al crear la nota en la base de datos'
            statusCode = 500
    
    
    success = error == ''
    response = {'success': success}
    if error != '':
        response['message'] = error
    
    return response, statusCode



@notesBlueprint.route('/notes/<int:noteId>', methods=['PUT'])
def UpdateNote(noteId):
    recievedData, error, statusCode = JsonExists(request)

    if error == '':
        targetNote = ValidateNoteAndUser(request, noteId)
        if type(targetNote) is str:
            error = targetNote
            statusCode = 400

    if error == '':
        cleanData = ValidateNoteData(recievedData)
        if type(cleanData) is str:
            error = cleanData
            statusCode = 400

    if error == '':
        noteModel, userModel = initModels()
        updated = noteModel.UpdateNote(cleanData, targetNote['id'])
        if updated == True:
            message = 'Nota editaca correctamente'
        else:
            error = 'Hubo un error al actualizar la nota'
            statusCode = 500
    
    success = error == ''
    if error != '':
        message = error

    response = {'success': success, 'message': message}    


    return jsonify(response), statusCode

@notesBlueprint.route('/notes/<int:noteId>', methods=['DELETE'])
def DeleteNote(noteId):
    statusCode = 200
    error = ''
    if error == '':
        targetNote = ValidateNoteAndUser(request, noteId)
        if type(targetNote) is str:
            error = targetNote
            statusCode = 400
    
    if error == '':
        noteModel, userModel = initModels()
        deleted = noteModel.DeleteNote(noteId)
        if deleted:
            message = 'Borrado correctamente'
        else:
            error = 'Hubo un error al borrar la nota'
            statusCode = 500
    
    success = error == ''
    if error != '':
        message = error
    response = {'success': success, 'message': message}
    return jsonify(response), statusCode


def ValidateNoteAndUser(request, noteId):
    '''
    Used to validate:
    the user is authenticated, the noteId exists and the note corresponds to user
    return the target note
    '''
    noteModel, userModel = initModels()
    error = ''

    if error == '':
        targetUser = userModel.GetUserByToken(request)
        if type(targetUser) is str:
            error = targetUser

    if error == '':
        targetNote = noteModel.GetNoteById(noteId)
        if targetNote is None:
            error = 'Nota no encontrada'
    
    if error == '':
        noteCorresponds = noteModel.NoteCorrespondsToUser(targetNote['id'], targetUser['id'])
        if noteCorresponds is None:
            error = 'Nota no correspondida'

    if error == '':
        result = targetNote
    else:
        result = error
    
    return result